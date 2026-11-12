from engine import Request
from scheduler import Scheduler


def ids(reqs):
    return [r.req_id for r in reqs]


def test_example():
    s = Scheduler(4)
    for r in (Request(0, 2, 2), Request(1, 3, 1), Request(2, 1, 1)):
        assert s.add(r) is True
    out = s.step()
    assert out["decode"] == [] and out["prefill"] == [0]
    out = s.step()
    assert out["decode"] == [0] and out["prefill"] == [1]
    out = s.step()
    assert out["decode"] == [0, 1] and out["prefill"] == [2]
    assert ids(s.finished) == [0, 1]
    out = s.step()
    assert out["decode"] == [2] and out["prefill"] == []
    assert ids(s.finished) == [0, 1, 2]
    assert not s.waiting and not s.admitted


def test_head_of_line_blocking():
    s = Scheduler(5)
    s.add(Request(0, 4, 1))
    s.add(Request(1, 3, 1))
    s.add(Request(2, 1, 1))
    out = s.step()
    assert out["prefill"] == [0]  # R2 would fit but R1 blocks it
    assert ids(s.waiting) == [1, 2]
    out = s.step()
    assert out["decode"] == [0] and out["prefill"] == [1, 2]
    out = s.step()
    assert out["decode"] == [1, 2]
    assert ids(s.finished) == [0, 1, 2]


def test_multiple_prefills_per_step():
    s = Scheduler(5)
    for i in range(3):
        s.add(Request(i, 2, 1))
    assert s.step()["prefill"] == [0, 1]
    out = s.step()
    assert out["decode"] == [0, 1] and out["prefill"] == [2]
    assert s.step()["decode"] == [2]


def test_decode_starves_prefill():
    s = Scheduler(2)
    s.add(Request(0, 1, 5))
    s.add(Request(1, 1, 5))
    s.add(Request(2, 1, 1))
    assert s.step()["prefill"] == [0, 1]
    for _ in range(4):
        out = s.step()
        assert out["decode"] == [0, 1] and out["prefill"] == []
    out = s.step()  # step 6: both finish, budget gone
    assert out["decode"] == [0, 1] and out["prefill"] == []
    assert ids(s.finished) == [0, 1]
    assert s.step()["prefill"] == [2]
    assert s.step()["decode"] == [2]


def test_generated_counts():
    s = Scheduler(4)
    r = Request(7, 2, 3)
    s.add(r)
    s.step()
    assert r.generated == 0 and r.prefill_done
    s.step()
    s.step()
    assert r.generated == 2 and ids(s.admitted) == [7]
    s.step()
    assert r.generated == 3 and ids(s.finished) == [7]


def test_validation():
    s = Scheduler(4)
    assert s.add(Request(0, 4, 1)) is True
    assert s.add(Request(0, 1, 1)) is False
    assert s.add(Request(1, 5, 1)) is False
    assert s.add(Request(2, 0, 1)) is False
    assert s.add(Request(3, 1, 0)) is False
    assert ids(s.waiting) == [0]


def test_late_arrivals_and_idle_steps():
    s = Scheduler(3)
    out = s.step()
    assert out["decode"] == [] and out["prefill"] == []
    s.add(Request(0, 2, 2))
    s.step()
    s.add(Request(1, 2, 1))
    out = s.step()
    assert out["decode"] == [0] and out["prefill"] == [1]
    out = s.step()
    assert out["decode"] == [0, 1]
    assert ids(s.finished) == [0, 1]
