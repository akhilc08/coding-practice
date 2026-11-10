# Level 1 — LRU Cache

**Suggested time: 15 min.** Only open `level2.md` after `pytest test_level1.py` passes.

Build a fixed-capacity cache that evicts the **least recently used** entry.
Don't use `functools.lru_cache`. Every method takes a `timestamp` (an `int`,
**non-decreasing**); Level 1 doesn't need it yet.

### `LRUCache(capacity)`
`capacity >= 1`.

### `get(timestamp, key) -> str | None`
Return the value, or `None` if missing. A successful `get` makes the key the
**most** recently used.

### `put(timestamp, key, value) -> str | None`
Insert or update. Either way, the key becomes the most recently used.
If inserting a **new** key into a full cache, first evict the least recently
used key. Return the **evicted key**, or `None` if nothing was evicted.
Updating an existing key never evicts.

## Example
```
c = LRUCache(2)
c.put(1, "a", "1")    # None
c.put(2, "b", "2")    # None
c.get(3, "a")         # "1"   (now b is least recently used)
c.put(4, "c", "3")    # "b"
c.get(5, "b")         # None
c.put(6, "a", "x")    # None  (update)
c.put(7, "d", "4")    # "c"
```

Follow-up to think about: can you make `get` and `put` O(1)?
