from solution import TextEditor


def state(e):
    return e.get_text(), e.get_cursor()


def test_example():
    e = TextEditor()
    e.type("aaaa")
    assert e.find("aa") == [0, 1, 2]
    assert e.replace_all("aa", "b") == 2
    assert state(e) == ("bb", 2)
    assert e.undo() is True
    assert state(e) == ("aaaa", 4)
    assert e.replace_all("z", "y") == 0
    assert e.undo() is True
    assert state(e) == ("", 0)


def test_find_none_and_longer_than_text():
    e = TextEditor()
    e.type("abc")
    assert e.find("x") == []
    assert e.find("abcd") == []
    assert e.find("abc") == [0]


def test_find_overlapping():
    e = TextEditor()
    e.type("abababa")
    assert e.find("aba") == [0, 2, 4]


def test_replace_non_overlapping_left_to_right():
    e = TextEditor()
    e.type("abababa")
    assert e.replace_all("aba", "X") == 2
    assert e.get_text() == "XbX"


def test_replace_moves_cursor_to_end_and_clears_selection():
    e = TextEditor()
    e.type("cat dog cat")
    e.select(0, 3)
    assert e.replace_all("cat", "bird") == 2
    assert state(e) == ("bird dog bird", 13)
    e.type("!")
    assert e.get_text() == "bird dog bird!"


def test_replace_with_empty_and_redo():
    e = TextEditor()
    e.type("a-b-c")
    e.move_cursor(1)
    assert e.replace_all("-", "") == 2
    assert state(e) == ("abc", 3)
    e.undo()
    assert state(e) == ("a-b-c", 1)
    e.redo()
    assert state(e) == ("abc", 3)


def test_replacement_containing_pattern():
    e = TextEditor()
    e.type("aXa")
    assert e.replace_all("a", "aa") == 2
    assert e.get_text() == "aaXaa"


def test_failed_replace_keeps_redo():
    e = TextEditor()
    e.type("abc")
    e.undo()
    assert e.replace_all("q", "r") == 0
    assert e.redo() is True
    assert e.get_text() == "abc"
