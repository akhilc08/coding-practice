from solution import InMemoryDB


def test_example():
    db = InMemoryDB()
    db.set_at_with_ttl("A", "B", "C", 1, 10)
    assert db.backup(3) == 1
    db.set_at("A", "D", "E", 4)
    assert db.backup(5) == 1
    assert db.delete_at("A", "B", 8) is True
    assert db.backup(9) == 1
    db.restore(10, 7)
    assert db.scan_at("A", 15) == ["B(C)", "D(E)"]
    assert db.scan_at("A", 16) == ["D(E)"]


def test_backup_counts_only_live_records():
    db = InMemoryDB()
    db.set_at("a", "f", "1", 1)
    db.set_at_with_ttl("b", "f", "2", 2, 2)  # dies at 4
    db.set_at("c", "f", "3", 3)
    db.delete_at("c", "f", 4)
    assert db.backup(5) == 1


def test_backup_empty_db():
    db = InMemoryDB()
    assert db.backup(1) == 0


def test_restore_picks_latest_backup_at_or_before():
    db = InMemoryDB()
    db.set_at("k", "f", "v1", 1)
    db.backup(2)
    db.set_at("k", "f", "v2", 3)
    db.backup(4)
    db.set_at("k", "f", "v3", 5)
    db.restore(6, 4)  # exactly at a backup timestamp
    assert db.get_at("k", "f", 7) == "v2"
    db.restore(8, 3)
    assert db.get_at("k", "f", 9) == "v1"


def test_restore_removes_data_added_after_backup():
    db = InMemoryDB()
    db.set_at("k", "f", "v", 1)
    db.backup(2)
    db.set_at("k", "g", "w", 3)
    db.set_at("other", "x", "y", 4)
    db.restore(5, 2)
    assert db.scan_at("k", 6) == ["f(v)"]
    assert db.scan_at("other", 6) == []


def test_backup_is_a_snapshot_not_a_reference():
    db = InMemoryDB()
    db.set_at("k", "f", "v", 1)
    db.backup(2)
    db.set_at("k", "f", "changed", 3)
    db.delete_at("k", "f", 4)
    db.restore(5, 2)
    assert db.get_at("k", "f", 6) == "v"
    # mutating after restore must not corrupt the stored backup
    db.set_at("k", "f", "again", 7)
    db.restore(8, 2)
    assert db.get_at("k", "f", 9) == "v"


def test_restore_recalculates_ttl():
    db = InMemoryDB()
    db.set_at_with_ttl("k", "f", "v", 10, 20)  # expires 30
    db.backup(25)                              # 5 remaining
    db.restore(100, 25)                        # now expires 105
    assert db.get_at("k", "f", 104) == "v"
    assert db.get_at("k", "f", 105) is None


def test_expired_fields_not_in_backup():
    db = InMemoryDB()
    db.set_at_with_ttl("k", "f", "v", 1, 2)  # dies at 3
    db.set_at("k", "g", "w", 2)
    db.backup(5)
    db.restore(6, 5)
    assert db.scan_at("k", 7) == ["g(w)"]
