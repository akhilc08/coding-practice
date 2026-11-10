# Level 4 — Pinned Entries

**Suggested time: 25 min.** Earlier tests must keep passing.

### `pin(timestamp, key) -> bool` / `unpin(timestamp, key) -> bool`
Pin or unpin a live entry. Return `False` if the key doesn't exist or is
expired. Pinning or unpinning does **not** change recency. Updating a pinned key
with `put` keeps it pinned.

A pinned entry is **never evicted**, but it can still expire.

- `put` of a new key into a full cache: remove expired entries, then evict the
  least recently used **unpinned** entry. If every entry is pinned, the put is
  **rejected**: nothing is inserted or evicted, and it returns `None`.
- `resize`: if the live pinned entries alone exceed `new_capacity`, return
  `None` and change nothing (no expiry cleanup, no evictions, capacity unchanged).
  Otherwise evict least recently used **unpinned** entries until it fits.

## Example
```
c = LRUCache(2)
c.put(0, "a", "1"); c.put(1, "b", "2")
c.pin(2, "a")         # True
c.put(3, "c", "3")    # "b"  (a is older but pinned)
c.pin(4, "c")
c.put(5, "d", "4")    # None (rejected)
c.get(6, "d")         # None
c.resize(7, 1)        # None (2 pinned entries don't fit in 1)
```
