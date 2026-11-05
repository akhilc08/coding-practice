# Level 1 — Basic Operations

**Suggested time: 15 min.** Only open `level2.md` after `pytest test_level1.py` passes.

You are building an in-memory database. It stores **records**. Each record is
identified by a `key` and holds a set of `field -> value` pairs. All keys,
fields, and values are strings.

Implement these methods on `InMemoryDB` in `solution.py`:

### `set(key, field, value) -> None`
Insert `field` with `value` into the record `key`. Create the record if it
doesn't exist. If the field already exists, overwrite its value.

### `get(key, field) -> str | None`
Return the value of `field` in record `key`. Return `None` if the record or
field doesn't exist.

### `delete(key, field) -> bool`
Remove `field` from record `key`. Return `True` if the field existed and was
removed, otherwise `False`. If a record has no fields left, it should no
longer exist.

## Example
```
db.set("A", "B", "E")      # A = {B: E}
db.set("A", "C", "F")      # A = {B: E, C: F}
db.get("A", "B")           # "E"
db.get("A", "D")           # None
db.delete("A", "B")        # True
db.delete("A", "D")        # False
db.get("A", "B")           # None
```
