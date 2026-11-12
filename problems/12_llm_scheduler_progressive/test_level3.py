from engine import Request
from scheduler import Scheduler


def test_example():
    s = Scheduler(10, prefix_cache_size=2)
    s.add(Request(0, 8, 1, "sys", 6))
    s.add(Request(1, 8, 1, "sys", 6))
    assert s.step()["prefill"] == [0, 1]
    assert s.cache_stats() == {"hits": 1, "misses": 1}


def test_hit_makes_head_fit():
    s = Scheduler(5, prefix_cache_size=1)
    s.add(Request(0, 5, 2, "p", 4))
    s.add(Request(1, 5, 1, "p", 4))
    assert s.step()["prefill"] == [0]  # 0 left
    out = s.step()  # decode R0 (1), R1 costs 1 on a hit
    assert out["decode"] == [0] and out["prefill"] == [1]


def test_no_prefix_not_counted_and_cache_disabled():
    s = Scheduler(10)
    s.add(Request(0, 4, 1, "a", 2))
    s.add(Request(1, 4, 1, "a", 2))
    s.add(Request(2, 2, 1))
    assert s.step()["prefill"] == [0, 1, 2]  # cache off: both miss
    assert s.cache_stats() == {"hits": 0, "misses": 2}


def test_lru_eviction_and_refresh():
    s = Scheduler(10, prefix_cache_size=2)
    rid = iter(range(100))

    def run(pid):
        s.add(Request(next(rid), 10, 1, pid, 9))
        s.step()
        s.step()

    run("A")  # miss
    run("B")  # miss
    run("A")  # hit, A now MRU
    run("C")  # miss, evicts B
    assert s.cache_stats() == {"hits": 1, "misses": 3}
    run("A")  # hit
    run("B")  # miss
    assert s.cache_stats() == {"hits": 2, "misses": 4}


def test_capacity_one():
    s = Scheduler(10, prefix_cache_size=1)
    for i, pid in enumerate(["x", "y", "x"]):
        s.add(Request(i, 10, 1, pid, 5))
        s.step()
        s.step()
    assert s.cache_stats() == {"hits": 0, "misses": 3}


def test_chunked_with_hit():
    s = Scheduler(4, chunked_prefill=True, prefix_cache_size=1)
    r0, r1 = Request(0, 10, 1, "X", 8), Request(1, 10, 1, "X", 8)
    s.add(r0)
    s.add(r1)
    s.step()
    s.step()
    out = s.step()  # R0 finishes prefill (2), R1 hits: needs 2 more
    assert out["prefill"] == [0, 1]
    assert r1.prefill_done
    assert s.cache_stats() == {"hits": 1, "misses": 1}


def test_prefix_validation():
    s = Scheduler(10, prefix_cache_size=1)
    assert s.add(Request(0, 5, 1, "p", 5)) is False
    assert s.add(Request(1, 5, 1, "p", 0)) is False
    assert s.add(Request(2, 11, 1, "p", 9)) is False
    assert s.add(Request(3, 5, 1, "p", 4)) is True
