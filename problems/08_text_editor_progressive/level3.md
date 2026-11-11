# Level 3 — Undo / Redo

**Suggested time: 25 min.** Earlier tests must keep passing.

### `undo() -> bool` / `redo() -> bool`
Undo or redo the last **text-changing** operation. Return `False` if there's
nothing to undo/redo.

- Text-changing operations: `type`, `delete`, `cut`, `paste`. An operation
  that doesn't actually change the text (e.g. `delete` at position 0, typing
  `""`, cutting with no selection) is **not** recorded.
- `move_cursor`, `select`, and `copy` are not undoable and don't affect the
  history.
- `undo` restores the text **and cursor** to what they were right before the
  operation. `redo` restores the text and cursor to what they were right
  after it. Both clear any selection.
- Any new text-changing operation clears the redo history.

## Example
```
e.type("abc")
e.type("def")          # "abcdef|"
e.move_cursor(1)
e.undo()               # "abc|"   (cursor restored to before "def")
e.undo()               # "|"
e.undo()               # False
e.redo()               # "abc|"
e.type("X")            # "abcX|"  (redo history cleared)
e.redo()               # False
```
