# Level 2 — Selection and Clipboard

**Suggested time: 20 min.** Earlier tests must keep passing.

### `select(start, end) -> None`
Select the characters in `[start, end)`. Both positions are clamped to
`[0, len(text)]`; if `start > end`, swap them. The cursor moves to `end` (after
swapping). Selecting an empty range (`start == end`) means **no selection**.

While a selection is active:
- `type(text)` **replaces** the selection. The cursor ends after the new text.
- `delete(n)` removes the **selection** (ignoring `n`) and returns it. The
  cursor goes to where the selection started.
- `move_cursor(pos)` clears the selection.

Any operation that changes the text clears the selection.

### `copy() -> None`
Copy the selection to the clipboard. With no selection, do nothing (the
clipboard keeps its old contents). The selection stays active.

### `cut() -> None`
Copy, then delete the selection. With no selection, do nothing.

### `paste() -> None`
Same as `type(clipboard)`, including replacing an active selection. The
clipboard starts as `""`.

## Example
```
e.type("hello world")
e.select(6, 11)        # "world" selected, cursor 11
e.copy()
e.select(0, 5)         # "hello" selected
e.paste()              # "world world", cursor 5
e.select(5, 0)         # same as select(0, 5)
e.cut()                # " world", cursor 0, clipboard "world"
```
