# Level 2 — Expiring Entries

**Suggested time: 20 min.** Earlier tests must keep passing.

### `put_with_ttl(timestamp, key, value, ttl) -> str | None`
Like `put`, but the entry expires: it's alive during `[timestamp, timestamp + ttl)`.
A plain `put` on a key removes any TTL it had (it never expires).

Expired entries behave as if they don't exist: `get` returns `None`, and a
`put`/`put_with_ttl` of that key counts as inserting a **new** key.

When inserting a new key into a full cache, **first remove every expired
entry**. Expired removals are *not* evictions and are never returned. Only if
the cache is still full, evict the least recently used entry and return its key.

### `size(timestamp) -> int`
Number of entries alive at `timestamp`.

## Example
```
c = LRUCache(2)
c.put_with_ttl(0, "a", "1", 10)   # alive for [0, 10)
c.put(1, "b", "2")
c.get(9, "a")                     # "1"
c.get(10, "a")                    # None (expired)
c.size(10)                        # 1
c.put(11, "c", "3")               # None (cache isn't full once "a" is gone)
c.put(12, "d", "4")               # "b"
```
