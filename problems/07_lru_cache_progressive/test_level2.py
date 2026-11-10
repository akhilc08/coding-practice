from solution import LRUCache


def test_example():
    c = LRUCache(2)
    c.put_with_ttl(0, "a", "1", 10)
    c.put(1, "b", "2")
    assert c.get(9, "a") == "1"
    assert c.get(10, "a") is None
    assert c.size(10) == 1
    assert c.put(11, "c", "3") is None
    assert c.put(12, "d", "4") == "b"


def test_expired_removed_before_lru_eviction():
    c = LRUCache(2)
    c.put(0, "a", "1")                 # LRU, never expires
    c.put_with_ttl(1, "b", "2", 5)     # expires at 6
    assert c.put(10, "c", "3") is None
    assert c.get(11, "a") == "1"
    assert c.get(12, "b") is None


def test_size_counts_only_live():
    c = LRUCache(5)
    c.put_with_ttl(0, "a", "1", 5)
    c.put_with_ttl(0, "b", "2", 10)
    c.put(0, "c", "3")
    assert c.size(0) == 3
    assert c.size(5) == 2
    assert c.size(10) == 1


def test_put_clears_ttl():
    c = LRUCache(2)
    c.put_with_ttl(0, "a", "1", 5)
    c.put(1, "a", "2")
    assert c.get(100, "a") == "2"


def test_put_with_ttl_on_existing_resets_expiry():
    c = LRUCache(2)
    c.put(0, "a", "1")
    c.put_with_ttl(5, "a", "2", 10)
    assert c.get(14, "a") == "2"
    assert c.get(15, "a") is None


def test_reinsert_expired_key_is_new():
    c = LRUCache(2)
    c.put_with_ttl(0, "a", "1", 5)
    c.put(1, "b", "2")
    assert c.put(10, "a", "x") is None
    assert c.put(11, "c", "3") == "b"


def test_multiple_expired_all_removed():
    c = LRUCache(3)
    c.put_with_ttl(0, "a", "1", 5)
    c.put_with_ttl(0, "b", "2", 5)
    c.put(0, "c", "3")
    assert c.put(10, "d", "4") is None
    assert c.put(11, "e", "5") is None
    assert c.size(11) == 3
