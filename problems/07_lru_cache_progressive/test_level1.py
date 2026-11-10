from solution import LRUCache


def test_example():
    c = LRUCache(2)
    assert c.put(1, "a", "1") is None
    assert c.put(2, "b", "2") is None
    assert c.get(3, "a") == "1"
    assert c.put(4, "c", "3") == "b"
    assert c.get(5, "b") is None
    assert c.put(6, "a", "x") is None
    assert c.put(7, "d", "4") == "c"
    assert c.get(8, "a") == "x"
    assert c.get(9, "d") == "4"


def test_get_missing():
    c = LRUCache(1)
    assert c.get(0, "nope") is None


def test_capacity_one():
    c = LRUCache(1)
    assert c.put(0, "a", "1") is None
    assert c.put(1, "b", "2") == "a"
    assert c.get(2, "a") is None
    assert c.get(3, "b") == "2"


def test_update_refreshes_recency_without_evicting():
    c = LRUCache(2)
    c.put(0, "a", "1")
    c.put(1, "b", "2")
    assert c.put(2, "a", "10") is None
    assert c.put(3, "c", "3") == "b"
    assert c.get(4, "a") == "10"


def test_miss_does_not_change_order():
    c = LRUCache(2)
    c.put(0, "a", "1")
    c.put(1, "b", "2")
    c.get(2, "zzz")
    assert c.put(3, "c", "3") == "a"


def test_eviction_order_many():
    c = LRUCache(3)
    for i, k in enumerate("abc"):
        c.put(i, k, k)
    c.get(3, "a")
    c.get(4, "b")
    assert [c.put(5 + i, k, k) for i, k in enumerate("xyz")] == ["c", "a", "b"]
