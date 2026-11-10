from solution import LRUCache


def test_example():
    c = LRUCache(2)
    c.put(0, "a", "1"); c.put(1, "b", "2")
    assert c.pin(2, "a") is True
    assert c.put(3, "c", "3") == "b"
    assert c.pin(4, "c") is True
    assert c.put(5, "d", "4") is None
    assert c.get(6, "d") is None
    assert c.resize(7, 1) is None
    assert c.get(8, "a") == "1"
    assert c.get(9, "c") == "3"


def test_pin_missing_or_expired():
    c = LRUCache(2)
    assert c.pin(0, "x") is False
    c.put_with_ttl(0, "a", "1", 5)
    assert c.pin(5, "a") is False
    assert c.unpin(5, "a") is False
    assert c.unpin(6, "ghost") is False


def test_pin_does_not_change_recency():
    c = LRUCache(3)
    c.put(0, "a", "1"); c.put(1, "b", "2"); c.put(2, "c", "3")
    c.pin(3, "a")
    c.unpin(4, "a")
    assert c.put(5, "d", "4") == "a"


def test_unpin_makes_evictable():
    c = LRUCache(1)
    c.put(0, "a", "1")
    c.pin(1, "a")
    assert c.put(2, "b", "2") is None
    c.unpin(3, "a")
    assert c.put(4, "b", "2") == "a"


def test_pinned_entries_still_expire():
    c = LRUCache(1)
    c.put_with_ttl(0, "a", "1", 5)
    c.pin(1, "a")
    assert c.put(10, "b", "2") is None
    assert c.get(11, "b") == "2"
    assert c.get_stats()["evictions"] == 0


def test_update_keeps_pin():
    c = LRUCache(2)
    c.put(0, "a", "1")
    c.pin(1, "a")
    c.put(2, "a", "new")
    c.put(3, "b", "2")
    assert c.put(4, "c", "3") == "b"
    assert c.get(5, "a") == "new"


def test_rejected_put_changes_nothing():
    c = LRUCache(1)
    c.put(0, "a", "1")
    c.pin(1, "a")
    assert c.put(2, "b", "2") is None
    assert c.size(3) == 1
    assert c.get_stats()["evictions"] == 0
    assert c.put(4, "a", "x") is None
    assert c.get(5, "a") == "x"


def test_resize_skips_pinned():
    c = LRUCache(4)
    for i, k in enumerate("abcd"):
        c.put(i, k, k)
    c.pin(4, "a")
    c.pin(5, "c")
    assert c.resize(6, 2) == ["b", "d"]
    assert c.size(7) == 2


def test_failed_resize_keeps_capacity():
    c = LRUCache(3)
    c.put(0, "a", "1"); c.put(1, "b", "2")
    c.pin(2, "a"); c.pin(3, "b")
    assert c.resize(4, 1) is None
    assert c.put(5, "c", "3") is None
    assert c.get(6, "c") == "3"


def test_expired_pins_dont_block_resize():
    c = LRUCache(2)
    c.put_with_ttl(0, "a", "1", 5)
    c.put(1, "b", "2")
    c.pin(2, "a"); c.pin(3, "b")
    assert c.resize(10, 1) == []
    assert c.get(11, "b") == "2"
