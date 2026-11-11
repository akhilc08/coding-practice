# Level 1 — Typing, Cursor, Backspace

**Suggested time: 15 min.** Only open `level2.md` after `pytest test_level1.py` passes.

Build a minimal text editor. The document starts empty with the cursor at
position `0`. Cursor positions are between characters: `0` is before the first
character, `len(text)` is after the last.

### `type(text) -> None`
Insert `text` at the cursor. The cursor ends up right after the inserted text.

### `move_cursor(pos) -> None`
Move the cursor to `pos`, clamped to `[0, len(text)]`.

### `delete(n) -> str`
Backspace: remove up to `n` characters **before** the cursor (fewer if the
cursor is near the start). Return the removed string. The cursor moves left
by the number of characters removed.

### `get_text() -> str` / `get_cursor() -> int`

## Example
```
e.type("hello")        # "hello|"
e.move_cursor(2)       # "he|llo"
e.type("XY")           # "heXY|llo"
e.delete(3)            # returns "eXY"  -> "h|llo"
e.move_cursor(-5)      # "|hllo"
e.delete(1)            # returns ""
e.move_cursor(99)      # "hllo|"
```
