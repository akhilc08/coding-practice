from solution import FileStorage


def test_example():
    fs = FileStorage()
    fs.add_file("/dir/a.txt", 5)
    fs.add_file("/dir/b.txt", 20)
    fs.add_file("/dir/c.txt", 5)
    fs.add_file("/other.txt", 100)
    assert fs.get_largest_n("/dir", 2) == ["/dir/b.txt(20)", "/dir/a.txt(5)"]
    assert fs.get_largest_n("/dir", 10) == [
        "/dir/b.txt(20)",
        "/dir/a.txt(5)",
        "/dir/c.txt(5)",
    ]
    assert fs.get_largest_n("/nope", 3) == []


def test_empty_storage():
    assert FileStorage().get_largest_n("", 5) == []


def test_empty_prefix_matches_all():
    fs = FileStorage()
    fs.add_file("/x", 1)
    fs.add_file("/y", 2)
    assert fs.get_largest_n("", 5) == ["/y(2)", "/x(1)"]


def test_ties_by_name_ascending():
    fs = FileStorage()
    for name in ["/c", "/a", "/b"]:
        fs.add_file(name, 7)
    assert fs.get_largest_n("/", 3) == ["/a(7)", "/b(7)", "/c(7)"]


def test_deleted_files_excluded():
    fs = FileStorage()
    fs.add_file("/a", 100)
    fs.add_file("/b", 1)
    fs.delete_file("/a")
    assert fs.get_largest_n("/", 5) == ["/b(1)"]


def test_n_zero():
    fs = FileStorage()
    fs.add_file("/a", 1)
    assert fs.get_largest_n("/", 0) == []
