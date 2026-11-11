from solution import TextEditor


def state(e):
    return e.get_text(), e.get_cursor()


def test_example():
    e = TextEditor()
    e.type("abc")
    e.type("def")
    e.move_cursor(1)
    assert e.undo() is True
    assert state(e) == ("abc", 3)
    assert e.undo() is True
    assert state(e) == ("", 0)
    assert e.undo() is False
    assert e.redo() is True
    assert state(e) == ("abc", 3)
    e.type("X")
    assert e.redo() is False
    assert state(e) == ("abcX", 4)


def test_undo_delete_restores_cursor():
    e = TextEditor()
    e.type("hello")
    e.move_cursor(3)
    e.delete(2)
    assert state(e) == ("hlo", 1)
    e.undo()
    assert state(e) == ("hello", 3)
    e.redo()
    assert state(e) == ("hlo", 1)


def test_noop_operations_not_recorded():
    e = TextEditor()
    e.type("ab")
    e.move_cursor(0)
    e.delete(3)
    e.type("")
    e.cut()
    e.paste()
    e.select(0, 2)
    e.copy()
    assert e.undo() is True
    assert state(e) == ("", 0)
    assert e.undo() is False


def test_undo_cut_and_paste():
    e = TextEditor()
    e.type("abcdef")
    e.select(1, 3)
    e.cut()
    e.move_cursor(4)
    e.paste()
    assert e.get_text() == "adefbc"
    e.undo()
    assert state(e) == ("adef", 4)
    e.undo()
    assert state(e) == ("abcdef", 3)


def test_undo_replace_selection_is_one_step():
    e = TextEditor()
    e.type("abc")
    e.select(0, 3)
    e.type("Z")
    e.undo()
    assert state(e) == ("abc", 3)


def test_undo_clears_selection():
    e = TextEditor()
    e.type("abc")
    e.type("def")
    e.select(0, 2)
    e.undo()
    e.type("X")
    assert e.get_text() == "abcX"


def test_multiple_redo_then_new_op_clears():
    e = TextEditor()
    for ch in "abc":
        e.type(ch)
    e.undo(); e.undo(); e.undo()
    assert e.redo() and e.redo()
    assert state(e) == ("ab", 2)
    e.delete(1)
    assert e.redo() is False
    assert e.undo() is True
    assert state(e) == ("ab", 2)
