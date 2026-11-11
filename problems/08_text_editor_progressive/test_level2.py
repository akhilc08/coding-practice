from solution import TextEditor


def state(e):
    return e.get_text(), e.get_cursor()


def test_example():
    e = TextEditor()
    e.type("hello world")
    e.select(6, 11)
    assert e.get_cursor() == 11
    e.copy()
    e.select(0, 5)
    e.paste()
    assert state(e) == ("world world", 5)
    e.select(5, 0)
    e.cut()
    assert state(e) == (" world", 0)
    e.paste()
    assert state(e) == ("world world", 5)


def test_type_replaces_selection():
    e = TextEditor()
    e.type("abcdef")
    e.select(1, 4)
    e.type("Z")
    assert state(e) == ("aZef", 2)
    e.type("Q")
    assert state(e) == ("aZQef", 3)   # selection was cleared by the first type


def test_delete_removes_selection_ignoring_n():
    e = TextEditor()
    e.type("abcdef")
    e.select(2, 4)
    assert e.delete(100) == "cd"
    assert state(e) == ("abef", 2)
    assert e.delete(1) == "b"


def test_move_cursor_clears_selection():
    e = TextEditor()
    e.type("abcdef")
    e.select(0, 3)
    e.move_cursor(6)
    assert e.delete(1) == "f"


def test_select_clamps_and_empty_means_none():
    e = TextEditor()
    e.type("abc")
    e.select(-10, 100)
    assert e.get_cursor() == 3
    e.copy()
    e.move_cursor(3)
    e.paste()
    assert e.get_text() == "abcabc"
    e.select(2, 2)
    assert e.get_cursor() == 2
    assert e.delete(1) == "b"


def test_copy_without_selection_keeps_clipboard():
    e = TextEditor()
    e.type("abc")
    e.select(0, 1)
    e.copy()
    e.move_cursor(3)
    e.copy()
    e.paste()
    assert e.get_text() == "abca"


def test_copy_keeps_selection():
    e = TextEditor()
    e.type("abcd")
    e.select(1, 3)
    e.copy()
    e.type("X")
    assert state(e) == ("aXd", 2)


def test_cut_without_selection_does_nothing():
    e = TextEditor()
    e.type("abc")
    e.cut()
    assert state(e) == ("abc", 3)
    e.paste()
    assert e.get_text() == "abc"


def test_paste_empty_clipboard():
    e = TextEditor()
    e.type("ab")
    e.paste()
    assert state(e) == ("ab", 2)
