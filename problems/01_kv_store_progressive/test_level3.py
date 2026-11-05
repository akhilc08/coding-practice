from solution import InMemoryDB


def test_example():
    db = InMemoryDB()
    db.set_at_with_ttl("A", "BC", "E", 1, 9)
    db.set_at_with_ttl("A", "BC", "E", 5, 10)
    db.set_at("A", "BD", "F", 5)
    assert db.scan_by_prefix_at("A", "B", 14) == ["BC(E)", "BD(F)"]
    assert db.scan_by_prefix_at("A", "B", 15) == ["BD(F)"]


def test_expiry_boundary_is_exclusive():
    db = InMemoryDB()
    db.set_at_with_ttl("k", "f", "v", 10, 5)
    assert db.get_at("k", "f", 14) == "v"
    assert db.get_at("k", "f", 15) is None


def test_no_ttl_never_expires():
    db = InMemoryDB()
    db.set_at("k", "f", "v", 1)
    assert db.get_at("k", "f", 10**9) == "v"


def test_set_at_clears_ttl():
    db = InMemoryDB()
    db.set_at_with_ttl("k", "f", "v", 1, 5)
    db.set_at("k", "f", "w", 2)
    assert db.get_at("k", "f", 100) == "w"


def test_delete_expired_returns_false():
    db = InMemoryDB()
    db.set_at_with_ttl("k", "f", "v", 1, 5)
    assert db.delete_at("k", "f", 6) is False


def test_delete_live_with_ttl():
    db = InMemoryDB()
    db.set_at_with_ttl("k", "f", "v", 1, 5)
    assert db.delete_at("k", "f", 3) is True
    assert db.get_at("k", "f", 4) is None


def test_reset_after_expiry():
    db = InMemoryDB()
    db.set_at_with_ttl("k", "f", "v", 1, 2)
    assert db.get_at("k", "f", 5) is None
    db.set_at("k", "f", "new", 6)
    assert db.get_at("k", "f", 7) == "new"


def test_scan_at_filters_expired():
    db = InMemoryDB()
    db.set_at_with_ttl("k", "a", "1", 1, 3)   # dies at 4
    db.set_at_with_ttl("k", "b", "2", 2, 10)  # dies at 12
    db.set_at("k", "c", "3", 3)
    assert db.scan_at("k", 3) == ["a(1)", "b(2)", "c(3)"]
    assert db.scan_at("k", 4) == ["b(2)", "c(3)"]
    assert db.scan_at("k", 12) == ["c(3)"]


def test_scan_at_missing_or_all_expired():
    db = InMemoryDB()
    assert db.scan_at("nope", 1) == []
    db.set_at_with_ttl("k", "a", "1", 2, 1)
    assert db.scan_at("k", 3) == []
