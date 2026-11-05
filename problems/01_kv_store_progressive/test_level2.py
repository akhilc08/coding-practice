from solution import InMemoryDB


def test_example():
    db = InMemoryDB()
    db.set("A", "BC", "E")
    db.set("A", "BD", "F")
    db.set("A", "C", "G")
    assert db.scan_by_prefix("A", "B") == ["BC(E)", "BD(F)"]
    assert db.scan("A") == ["BC(E)", "BD(F)", "C(G)"]
    assert db.scan_by_prefix("B", "B") == []


def test_scan_missing_record():
    db = InMemoryDB()
    assert db.scan("nope") == []


def test_scan_sorted_regardless_of_insert_order():
    db = InMemoryDB()
    for f in ["z", "a", "m", "b"]:
        db.set("k", f, f.upper())
    assert db.scan("k") == ["a(A)", "b(B)", "m(M)", "z(Z)"]


def test_scan_reflects_updates_and_deletes():
    db = InMemoryDB()
    db.set("k", "a", "1")
    db.set("k", "b", "2")
    db.set("k", "a", "3")
    db.delete("k", "b")
    assert db.scan("k") == ["a(3)"]
    db.delete("k", "a")
    assert db.scan("k") == []


def test_prefix_no_match():
    db = InMemoryDB()
    db.set("k", "apple", "1")
    assert db.scan_by_prefix("k", "b") == []


def test_empty_prefix_matches_all():
    db = InMemoryDB()
    db.set("k", "b", "2")
    db.set("k", "a", "1")
    assert db.scan_by_prefix("k", "") == ["a(1)", "b(2)"]


def test_prefix_is_prefix_not_substring():
    db = InMemoryDB()
    db.set("k", "xab", "1")
    db.set("k", "ab", "2")
    db.set("k", "abc", "3")
    assert db.scan_by_prefix("k", "ab") == ["ab(2)", "abc(3)"]
