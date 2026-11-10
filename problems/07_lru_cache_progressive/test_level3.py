from solution import LRUCache


def test_example():
    c = LRUCache(3)
    c.put(0, "a", "1"); c.put(1, "b", "2"); c.put(2, "c", "3")
    c.get(3, "a")
    c.get(4, "zzz")
    assert c.resize(5, 1) == ["b", "c"]
    assert c.get_stats() == {"hits": 1, "misses": 1, "evictions": 2}
    assert c.get(6, "a") == "1"


def test_stats_start_at_zero():
    assert LRUCache(1).get_stats() == {"hits": 0, "misses": 0, "evictions": 0}


def test_expired_get_is_miss_and_not_eviction():
    c = LRUCache(2)
    c.put_with_ttl(0, "a", "1", 5)
    c.get(1, "a")
    c.get(5, "a")
    assert c.get_stats() == {"hits": 1, "misses": 1, "evictions": 0}


def test_put_evictions_counted_expiry_not():
    c = LRUCache(1)
    c.put(0, "a", "1")
    c.put(1, "b", "2")
    c.put_with_ttl(2, "c", "3", 1)
    c.put(10, "d", "4")
    assert c.get_stats()["evictions"] == 2


def test_grow_returns_empty_and_holds_more():
    c = LRUCache(1)
    c.put(0, "a", "1")
    assert c.resize(1, 3) == []
    assert c.put(2, "b", "2") is None
    assert c.put(3, "c", "3") is None
    assert c.put(4, "d", "4") == "a"


def test_shrink_removes_expired_first():
    c = LRUCache(3)
    c.put(0, "a", "1")
    c.put_with_ttl(1, "b", "2", 5)
    c.put(2, "c", "3")
    assert c.resize(10, 2) == []
    assert c.get(11, "a") == "1"
    assert c.get(12, "c") == "3"


def test_shrink_then_put_uses_new_capacity():
    c = LRUCache(3)
    for i, k in enumerate("abc"):
        c.put(i, k, k)
    c.resize(3, 2)
    assert c.put(4, "d", "d") == "b"
    assert c.size(5) == 2
