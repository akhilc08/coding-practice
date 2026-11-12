from engine import Request
from scheduler import Scheduler


def test_example():
    s = Scheduler(4, chunked_prefill=True)
    r0, r1 = Request(0, 10, 2), Request(1, 3, 1)
    assert s.add(r0) and s.add(r1)
    assert s.step()["prefill"] == [0]
    assert r0.prefilled == 4
    assert s.step()["prefill"] == [0]
    out = s.step()
    assert out["prefill"] == [0, 1]
    assert r0.prefill_done and r1.prefilled == 2
    out = s.step()
    assert out["decode"] == [0] and out["prefill"] == [1]
    out = s.step()
    assert out["decode"] == [0, 1]
    m = s.metrics(0)
    assert (m["arrival"], m["first_token"], m["finished"]) == (0, 4, 5)
    m = s.metrics(1)
    assert (m["arrival"], m["first_token"], m["finished"]) == (0, 5, 5)


def test_unchunked_unchanged_and_metrics():
    s = Scheduler(4)
    for r in (Request(0, 2, 2), Request(1, 3, 1), Request(2, 1, 1)):
        s.add(r)
    for _ in range(4):
        s.step()
    m = s.metrics(0)
    assert (m["first_token"], m["finished"]) == (2, 3)
    m = s.metrics(2)
    assert (m["arrival"], m["first_token"], m["finished"]) == (0, 4, 4)
    assert s.add(Request(9, 5, 1)) is False  # still rejected without chunking


def test_metrics_pending_and_unknown():
    s = Scheduler(4)
    s.step()
    s.step()
    s.add(Request(0, 3, 2))
    m = s.metrics(0)
    assert (m["arrival"], m["first_token"], m["finished"]) == (2, None, None)
    s.step()
    s.step()
    m = s.metrics(0)
    assert (m["first_token"], m["finished"]) == (4, None)
    assert s.metrics(99) is None


def test_chunk_exact_fit_then_next():
    s = Scheduler(5, chunked_prefill=True)
    s.add(Request(0, 5, 1))
    s.add(Request(1, 7, 1))
    assert s.step()["prefill"] == [0]
    out = s.step()  # decode R0 (1), R1 gets 4
    assert out["decode"] == [0] and out["prefill"] == [1]
    out = s.step()  # R1 needs 3, done; leftover 2 unused
    assert out["decode"] == [] and out["prefill"] == [1]
    assert s.step()["decode"] == [1]
    assert s.metrics(1)["finished"] == 4


def test_long_prompt_does_not_block_forever():
    s = Scheduler(3, chunked_prefill=True)
    assert s.add(Request(0, 8, 1)) is True
    s.add(Request(1, 1, 1))
    outs = [s.step() for _ in range(4)]
    assert [o["prefill"] for o in outs] == [[0], [0], [0, 1], []]
    assert outs[3]["decode"] == [0, 1]
