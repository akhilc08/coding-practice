from engine import Request
from scheduler import Scheduler


def test_example_and_thrash():
    s = Scheduler(10, kv_capacity=10)
    s.add(Request(0, 4, 4))
    s.add(Request(1, 4, 4))
    out = s.step()
    assert out["prefill"] == [0, 1] and out["preempted"] == []
    assert s.memory_used() == 8
    assert s.step()["decode"] == [0, 1]
    assert s.memory_used() == 10
    out = s.step()
    assert out == {"decode": [0], "prefill": [1], "preempted": [1]}
    assert s.memory_used() == 10
    out = s.step()  # full again: R1 preempted, can't restart (7 + 4 > 10)
    assert out == {"decode": [0], "prefill": [], "preempted": [1]}
    assert s.memory_used() == 7
    out = s.step()  # R0 finishes, frees 8, R1 starts
    assert out["decode"] == [0] and out["prefill"] == [1]
    assert s.memory_used() == 4
    for _ in range(4):
        s.step()
    m = s.metrics(1)
    assert (m["first_token"], m["finished"], m["preemptions"]) == (6, 9, 2)
    assert s.metrics(0)["preemptions"] == 0
    assert s.memory_used() == 0


def test_memory_blocks_prefill_head():
    s = Scheduler(10, kv_capacity=10)
    s.add(Request(0, 6, 4))
    s.add(Request(1, 5, 1))
    s.add(Request(2, 1, 1))  # would fit, but R1 is the head
    assert s.step()["prefill"] == [0]
    for _ in range(3):
        out = s.step()
        assert out["prefill"] == [] and out["preempted"] == []
    out = s.step()
    assert out["decode"] == [0] and out["prefill"] == [1, 2]
    assert s.memory_used() == 6


def test_self_preemption():
    s = Scheduler(10, kv_capacity=8)
    s.add(Request(0, 3, 3))
    s.add(Request(1, 4, 4))
    s.step()  # mem 7
    out = s.step()
    # R0 -> 8. R1 finds memory full; it is the newest holder, so it preempts
    # itself and doesn't decode. Prefill then restarts it (4 + 4 <= 8).
    assert out == {"decode": [0], "prefill": [1], "preempted": [1]}
    assert s.memory_used() == 8
    out = s.step()  # full again: R1 preempted, R0 decodes, R1 can't restart
    assert out == {"decode": [0], "prefill": [], "preempted": [1]}
    assert s.memory_used() == 5
    out = s.step()  # R0 finishes, R1 restarts
    assert out == {"decode": [0], "prefill": [1], "preempted": []}
    assert s.metrics(1)["preemptions"] == 2


def test_preempted_goes_to_front_and_resets():
    s = Scheduler(10, kv_capacity=10)
    r1 = Request(1, 4, 4)
    s.add(Request(0, 4, 4))
    s.add(r1)
    s.step()
    s.step()
    s.step()  # R1 preempted and restarted
    s.add(Request(2, 1, 1))
    out = s.step()  # R1 preempted again, can't restart
    assert out["preempted"] == [1]
    assert [r.req_id for r in s.waiting] == [1, 2]
    assert r1.generated == 0 and r1.prefilled == 0
    assert s.metrics(1)["first_token"] is None


def test_preempts_partial_prefill():
    s = Scheduler(4, chunked_prefill=True, kv_capacity=10)
    r1 = Request(1, 8, 1)
    s.add(Request(0, 2, 4))
    s.add(r1)
    out = s.step()  # R0 prefilled (mem 2), R1 starts: reserves 8, gets 2/8
    assert out["prefill"] == [0, 1] and s.memory_used() == 10
    out = s.step()  # full: newest holder is the half-prefilled R1
    assert out == {"decode": [0], "prefill": [], "preempted": [1]}
    assert r1.prefilled == 0 and s.memory_used() == 3
    s.step()
    s.step()
    out = s.step()  # R0 finishes, R1 restarts from scratch
    assert out["decode"] == [0] and out["prefill"] == [1]
    assert r1.prefilled == 3 and s.memory_used() == 8


def test_capacity_validation_and_unlimited():
    s = Scheduler(10, kv_capacity=10)
    assert s.add(Request(0, 6, 5)) is False
    assert s.add(Request(1, 6, 4)) is True
    u = Scheduler(10)
    u.add(Request(0, 5, 100))
    u.step()
    u.step()
    assert u.memory_used() == 6


def test_cache_hit_still_reserves_full_prompt():
    s = Scheduler(10, prefix_cache_size=1, kv_capacity=20)
    s.add(Request(0, 6, 1, "p", 5))
    s.add(Request(1, 6, 1, "p", 5))
    s.step()
    assert s.memory_used() == 12
    assert s.cache_stats() == {"hits": 1, "misses": 1}
