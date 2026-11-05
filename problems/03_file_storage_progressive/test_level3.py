from solution import FileStorage


def test_example():
    fs = FileStorage()
    assert fs.add_user("u1", 100) is True
    assert fs.add_file_by("u1", "/u1/a", 60) == 40
    assert fs.add_file_by("u1", "/u1/b", 50) is None
    fs.add_user("u2", 30)
    assert fs.add_file_by("u2", "/u2/a", 25) == 5
    assert fs.merge_user("u1", "u2") == 45
    assert fs.delete_file("/u2/a") == 25
    assert fs.add_file_by("u1", "/u1/b", 50) == 20


def test_add_user_duplicate():
    fs = FileStorage()
    assert fs.add_user("u", 10) is True
    assert fs.add_user("u", 99) is False
    assert fs.add_file_by("u", "/a", 10) == 0  # original capacity kept


def test_add_file_by_failures():
    fs = FileStorage()
    assert fs.add_file_by("ghost", "/a", 1) is None
    fs.add_user("u", 10)
    fs.add_file("/taken", 1)
    assert fs.add_file_by("u", "/taken", 1) is None
    assert fs.add_file_by("u", "/big", 11) is None
    assert fs.get_file_size("/big") is None
    assert fs.add_file_by("u", "/ok", 10) == 0


def test_name_conflict_across_users():
    fs = FileStorage()
    fs.add_user("a", 10)
    fs.add_user("b", 10)
    fs.add_file_by("a", "/f", 3)
    assert fs.add_file_by("b", "/f", 3) is None
    assert fs.add_file("/f", 3) is False


def test_delete_frees_capacity():
    fs = FileStorage()
    fs.add_user("u", 10)
    fs.add_file_by("u", "/a", 8)
    assert fs.delete_file("/a") == 8
    assert fs.add_file_by("u", "/b", 10) == 0


def test_admin_files_unlimited_and_visible():
    fs = FileStorage()
    assert fs.add_file("/huge", 10**12) is True
    fs.add_user("u", 5)
    fs.add_file_by("u", "/small", 5)
    assert fs.get_largest_n("/", 5) == ["/huge(1000000000000)", "/small(5)"]


def test_merge_invalid():
    fs = FileStorage()
    fs.add_user("a", 10)
    assert fs.merge_user("a", "a") is None
    assert fs.merge_user("a", "ghost") is None
    assert fs.merge_user("ghost", "a") is None


def test_merged_user_is_gone():
    fs = FileStorage()
    fs.add_user("a", 10)
    fs.add_user("b", 10)
    fs.add_file_by("b", "/b1", 4)
    fs.merge_user("a", "b")
    assert fs.add_file_by("b", "/x", 1) is None
    assert fs.add_user("b", 3) is True          # can be re-created fresh
    assert fs.add_file_by("b", "/y", 3) == 0
    assert fs.get_file_size("/b1") == 4         # file survived, now a's
    assert fs.add_file_by("a", "/z", 16) == 0   # a: 20 capacity - 4 - 16
