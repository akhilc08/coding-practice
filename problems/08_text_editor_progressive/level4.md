# Level 4 — Find and Replace

**Suggested time: 25 min.** Earlier tests must keep passing.

### `find(pattern) -> list[int]`
Return the start index of **every** occurrence of `pattern` (a non-empty
string), **including overlapping** ones, in increasing order.

### `replace_all(pattern, replacement) -> int`
Replace **non-overlapping** occurrences of `pattern`, scanning left to right
(after a match, continue scanning after the end of that match). Return the
number of replacements.

- If at least one replacement happened: it's a single undoable operation, the
  selection is cleared, and the cursor moves to the **end** of the text.
- If nothing matched: return `0` and change nothing (not recorded in history).

## Example
```
e.type("aaaa")
e.find("aa")                 # [0, 1, 2]
e.replace_all("aa", "b")     # 2   -> "bb|"
e.undo()                     # "aaaa", cursor 4
e.replace_all("z", "y")      # 0
e.undo()                     # True  -> undoes the original type("aaaa")
```
