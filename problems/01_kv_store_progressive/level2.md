# Level 2 — Scanning

**Suggested time: 15 min.** Your Level 1 tests must keep passing.

Add support for displaying a record's fields.

### `scan(key) -> list[str]`
Return all fields of record `key` as strings formatted `"<field>(<value>)"`,
sorted lexicographically by field. Return `[]` if the record doesn't exist.

### `scan_by_prefix(key, prefix) -> list[str]`
Same as `scan`, but only include fields whose name starts with `prefix`.
Return `[]` if the record doesn't exist or nothing matches.

## Example
```
db.set("A", "BC", "E")
db.set("A", "BD", "F")
db.set("A", "C", "G")
db.scan_by_prefix("A", "B")   # ["BC(E)", "BD(F)"]
db.scan("A")                  # ["BC(E)", "BD(F)", "C(G)"]
db.scan_by_prefix("B", "B")   # []
```
