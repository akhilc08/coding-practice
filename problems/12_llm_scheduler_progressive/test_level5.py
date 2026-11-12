from engine import Request
from cluster import Cluster


def test_least_loaded_routing():
    c = Cluster(2, 10)
    assert c.add(Request(0, 5, 3)) == 0
    assert c.add(Request(1, 3, 3)) == 1   # loads 5 vs 0
    assert c.add(Request(2, 1, 3)) == 1   # loads 5 vs 3
    res = c.step()
    assert len(res) == 2
    assert res[0]["prefill"] == [0] and res[1]["prefill"] == [1, 2]
    assert c.add(Request(3, 2, 1)) == 0   # loads 1 vs 2
    assert c.replica_of(2) == 1 and c.replica_of(99) is None


def test_tie_goes_to_lowest_index():
    c = Cluster(3, 10)
    assert [c.add(Request(i, 4, 1)) for i in range(4)] == [0, 1, 2, 0]


def test_prefix_affinity():
    c = Cluster(2, 10, prefix_cache_size=4)
    assert c.add(Request(0, 6, 9, "sys", 5)) == 0
    c.step()                              # replica 0 now caches "sys"
    assert c.add(Request(1, 9, 1)) == 1   # loads 1 vs 0
    assert c.add(Request(2, 8, 1)) == 0   # 1 vs 9
    assert c.add(Request(3, 5, 1)) == 0   # 9 vs 9, tie -> 0
    # loads now 14 vs 9, but replica 0 has "sys": affinity beats load
    assert c.add(Request(4, 6, 1, "sys", 5)) == 0
    # no replica has "other": plain least-loaded
    assert c.add(Request(5, 6, 1, "other", 5)) == 1


def test_rejections():
    c = Cluster(2, 4)
    assert c.add(Request(0, 4, 1)) == 0
    assert c.add(Request(0, 1, 1)) == -1  # duplicate even though replica 1 is empty
    assert c.add(Request(1, 5, 1)) == -1
    assert c.replica_of(1) is None


def test_drain_moves_unstarted_requests():
    c = Cluster(3, 4)
    assert [c.add(Request(i, 4, 5)) for i in range(3)] == [0, 1, 2]
    assert c.add(Request(3, 4, 1)) == 0
    assert c.add(Request(4, 4, 1)) == 1
    c.step()  # each replica prefills its head; loads 5, 5, 1
    assert c.drain(0) == [3]
    assert c.replica_of(3) == 2
    assert c.metrics(3)["arrival"] == 0
    assert c.drain(0) == []
    assert c.drain(7) == []
    assert c.add(Request(5, 1, 1)) != 0
    # R0 keeps running on the drained replica
    for _ in range(5):
        c.step()
    assert c.replica_of(0) == 0 and c.metrics(0)["finished"] == 6


def test_drain_keeps_partial_prefill_and_routes_in_order():
    c = Cluster(2, 4, chunked_prefill=True)
    c.add(Request(0, 10, 1))   # 0
    c.add(Request(1, 1, 1))    # 1
    c.add(Request(2, 3, 1))    # 1 (load 1 vs 10)
    c.add(Request(3, 2, 1))    # 1 (4 vs 10)
    c.add(Request(4, 2, 1))    # 1 (6 vs 10)
    c.add(Request(5, 2, 1))    # 1 (10 vs 8)
    assert [c.replica_of(i) for i in range(6)] == [0, 1, 1, 1, 1, 1]
    c.add(Request(6, 3, 1))    # loads 10 vs 10 -> 0
    c.add(Request(7, 3, 1))    # 13 vs 10 -> 1
    c.step()  # r0: R0 4/10; r1: R1, R2 prefilled
    assert c.drain(0) == [6]   # R0 has started, stays
    assert c.replica_of(0) == 0 and c.replica_of(6) == 1
    assert c.drain(1) == []    # nowhere left to go, but now draining
    assert c.add(Request(8, 1, 1)) == -1
