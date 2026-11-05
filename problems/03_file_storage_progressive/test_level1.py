from solution import FileStorage


def test_example():
    fs = FileStorage()
    assert fs.add_file("/a.txt", 10) is True
    assert fs.add_file("/a.txt", 99) is False
    assert fs.get_file_size("/a.txt") == 10
    assert fs.delete_file("/a.txt") == 10
    assert fs.get_file_size("/a.txt") is None


def test_missing_file():
    fs = FileStorage()
    assert fs.get_file_size("/x") is None
    assert fs.delete_file("/x") is None


def test_duplicate_add_keeps_original_size():
    fs = FileStorage()
    fs.add_file("/a", 1)
    fs.add_file("/a", 2)
    assert fs.get_file_size("/a") == 1


def test_readd_after_delete():
    fs = FileStorage()
    fs.add_file("/a", 1)
    fs.delete_file("/a")
    assert fs.add_file("/a", 5) is True
    assert fs.get_file_size("/a") == 5


def test_zero_size_file():
    fs = FileStorage()
    assert fs.add_file("/empty", 0) is True
    assert fs.get_file_size("/empty") == 0
    assert fs.delete_file("/empty") == 0
