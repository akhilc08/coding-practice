from solution import InMemoryDB


def test_example():
    db = InMemoryDB()
    db.set("A", "B", "E")
    db.set("A", "C", "F")
    assert db.get("A", "B") == "E"
    assert db.get("A", "D") is None
    assert db.delete("A", "B") is True
    assert db.delete("A", "D") is False
    assert db.get("A", "B") is None
    assert db.get("A", "C") == "F"


def test_get_missing_record():
    db = InMemoryDB()
    assert db.get("nope", "x") is None


def test_overwrite():
    db = InMemoryDB()
    db.set("k", "f", "1")
    db.set("k", "f", "2")
    assert db.get("k", "f") == "2"


def test_delete_missing_record():
    db = InMemoryDB()
    assert db.delete("nope", "x") is False


def test_delete_twice():
    db = InMemoryDB()
    db.set("k", "f", "v")
    assert db.delete("k", "f") is True
    assert db.delete("k", "f") is False


def test_records_are_independent():
    db = InMemoryDB()
    db.set("k1", "f", "a")
    db.set("k2", "f", "b")
    assert db.get("k1", "f") == "a"
    assert db.get("k2", "f") == "b"
    db.delete("k1", "f")
    assert db.get("k2", "f") == "b"


def test_record_recreated_after_emptied():
    db = InMemoryDB()
    db.set("k", "f", "v")
    db.delete("k", "f")
    db.set("k", "g", "w")
    assert db.get("k", "g") == "w"
    assert db.get("k", "f") is None
