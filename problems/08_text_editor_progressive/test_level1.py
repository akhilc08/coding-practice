from solution import TextEditor


def state(e):
    return e.get_text(), e.get_cursor()


def test_example():
    e = TextEditor()
    e.type("hello")
    e.move_cursor(2)
    e.type("XY")
    assert state(e) == ("heXYllo", 4)
    assert e.delete(3) == "eXY"
    assert state(e) == ("hllo", 1)
    e.move_cursor(-5)
    assert e.delete(1) == ""
    assert state(e) == ("hllo", 0)
    e.move_cursor(99)
    assert state(e) == ("hllo", 4)


def test_starts_empty():
    e = TextEditor()
    assert state(e) == ("", 0)
    assert e.delete(5) == ""


def test_delete_more_than_available():
    e = TextEditor()
    e.type("abc")
    e.move_cursor(2)
    assert e.delete(10) == "ab"
    assert state(e) == ("c", 0)


def test_delete_zero():
    e = TextEditor()
    e.type("abc")
    assert e.delete(0) == ""
    assert state(e) == ("abc", 3)


def test_type_in_middle_multiple_times():
    e = TextEditor()
    e.type("ad")
    e.move_cursor(1)
    e.type("b")
    e.type("c")
    assert state(e) == ("abcd", 3)


def test_type_empty_string():
    e = TextEditor()
    e.type("x")
    e.type("")
    assert state(e) == ("x", 1)
