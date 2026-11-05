# Level 3 — Timestamps and TTL

**Suggested time: 25 min.** Earlier levels' tests must keep passing. This is the
level where a weak Level 1 design starts to hurt — refactor if you need to.

Every operation now gets a timestamped variant. `timestamp` is an `int`.
Within a single test, timestamped calls are made with **strictly increasing**
timestamps. Timestamped and non-timestamped calls won't be mixed on the same
`InMemoryDB` instance.

A field may have a **TTL** (time-to-live). A field set at `timestamp` with
`ttl` is visible during `[timestamp, timestamp + ttl)` — i.e. it is expired at
exactly `timestamp + ttl`. Fields with no TTL never expire. Expired fields
behave exactly as if they don't exist.

### `set_at(key, field, value, timestamp) -> None`
Like `set`. The field has no TTL (this clears any previous TTL on it).

### `set_at_with_ttl(key, field, value, timestamp, ttl) -> None`
Like `set`, but the field expires at `timestamp + ttl`.

### `get_at(key, field, timestamp) -> str | None`
### `delete_at(key, field, timestamp) -> bool`
Deleting an already-expired field returns `False`.
### `scan_at(key, timestamp) -> list[str]`
### `scan_by_prefix_at(key, prefix, timestamp) -> list[str]`

## Example
```
db.set_at_with_ttl("A", "BC", "E", 1, 9)    # BC lives in [1, 10)
db.set_at_with_ttl("A", "BC", "E", 5, 10)   # overwritten: lives in [5, 15)
db.set_at("A", "BD", "F", 5)                # no TTL
db.scan_by_prefix_at("A", "B", 14)          # ["BC(E)", "BD(F)"]
db.scan_by_prefix_at("A", "B", 15)          # ["BD(F)"]
```
