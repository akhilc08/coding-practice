# Level 3 — Stats and Resizing

**Suggested time: 20 min.** Earlier tests must keep passing.

### `get_stats() -> dict`
Return `{"hits": int, "misses": int, "evictions": int}`.
- A `get` that returns a value is a hit, and one that returns `None` is a miss
  (including for expired keys).
- `evictions` counts LRU evictions only (from `put` or `resize`). Removing an
  expired entry is not an eviction.

### `resize(timestamp, new_capacity) -> list[str]`
Change the capacity (`new_capacity >= 1`). If the cache now holds more live
entries than fit, remove expired entries first, then evict least recently used
entries until it fits. Return the evicted keys **in eviction order** (oldest
first). Growing the cache returns `[]`.

## Example
```
c = LRUCache(3)
c.put(0, "a", "1"); c.put(1, "b", "2"); c.put(2, "c", "3")
c.get(3, "a")
c.get(4, "zzz")
c.resize(5, 1)       # ["b", "c"]
c.get_stats()        # {"hits": 1, "misses": 1, "evictions": 2}
```
