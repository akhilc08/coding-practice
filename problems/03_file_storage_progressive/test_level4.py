from solution import FileStorage


def test_example():
    fs = FileStorage()
    fs.add_user("u", 100)
    fs.add_file_by("u", "/a", 10)
    fs.add_file_by("u", "/b", 20)
    assert fs.backup_user("u") == 2
    fs.delete_file("/a")
    fs.add_file_by("u", "/c", 5)
    fs.add_file("/a", 1)
    assert fs.restore_user("u") == 1
    assert fs.get_file_size("/c") is None
    assert fs.get_file_size("/a") == 1
    assert fs.get_file_size("/b") == 20


def test_missing_user():
    fs = FileStorage()
    assert fs.backup_user("ghost") is None
    assert fs.restore_user("ghost") is None


def test_backup_empty_user():
    fs = FileStorage()
    fs.add_user("u", 10)
    assert fs.backup_user("u") == 0


def test_restore_without_backup_deletes_everything():
    fs = FileStorage()
    fs.add_user("u", 10)
    fs.add_file_by("u", "/a", 5)
    assert fs.restore_user("u") == 0
    assert fs.get_file_size("/a") is None
    assert fs.add_file_by("u", "/b", 10) == 0  # capacity fully freed


def test_backup_replaces_previous():
    fs = FileStorage()
    fs.add_user("u", 100)
    fs.add_file_by("u", "/a", 1)
    fs.backup_user("u")
    fs.add_file_by("u", "/b", 2)
    assert fs.backup_user("u") == 2
    fs.delete_file("/a")
    fs.delete_file("/b")
    assert fs.restore_user("u") == 2
    assert fs.get_file_size("/a") == 1
    assert fs.get_file_size("/b") == 2


def test_backup_is_snapshot():
    fs = FileStorage()
    fs.add_user("u", 100)
    fs.add_file_by("u", "/a", 10)
    fs.backup_user("u")
    fs.delete_file("/a")
    fs.add_file_by("u", "/a", 50)   # same name, different size
    assert fs.restore_user("u") == 1
    assert fs.get_file_size("/a") == 10


def test_restore_updates_capacity_correctly():
    fs = FileStorage()
    fs.add_user("u", 30)
    fs.add_file_by("u", "/a", 10)
    fs.backup_user("u")
    fs.add_file_by("u", "/b", 20)    # remaining 0
    fs.restore_user("u")             # only /a again -> remaining 20
    assert fs.add_file_by("u", "/c", 20) == 0


def test_restore_twice_from_same_backup():
    fs = FileStorage()
    fs.add_user("u", 100)
    fs.add_file_by("u", "/a", 10)
    fs.backup_user("u")
    fs.restore_user("u")
    fs.delete_file("/a")
    assert fs.restore_user("u") == 1
    assert fs.get_file_size("/a") == 10


def test_merge_discards_second_users_backup():
    fs = FileStorage()
    fs.add_user("a", 100)
    fs.add_user("b", 100)
    fs.add_file_by("a", "/a1", 1)
    fs.add_file_by("b", "/b1", 2)
    fs.backup_user("a")
    fs.backup_user("b")
    fs.merge_user("a", "b")
    # a's backup only has /a1; restoring a deletes /b1 (now a's) and restores /a1
    assert fs.restore_user("a") == 1
    assert fs.get_file_size("/a1") == 1
    assert fs.get_file_size("/b1") is None
    # re-created b has no backup
    fs.add_user("b", 10)
    fs.add_file_by("b", "/new", 1)
    assert fs.restore_user("b") == 0
    assert fs.get_file_size("/new") is None
