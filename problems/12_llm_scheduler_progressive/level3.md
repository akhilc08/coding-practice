# Level 3 — Prefix cache

Many requests share a system prompt. A request may carry `prefix_id` and
`prefix_len`: its first `prefix_len` prompt tokens are that shared prefix.

Add `prefix_cache_size` to the constructor (0 = no caching).

- `add` returns `False` if `prefix_id` is set and not `0 < prefix_len < prompt_len`.
- **Lookup** happens when a request is about to receive its first prefill work.
  On a hit, call `load_prefix(req)` (free) and the request's prefill cost
  becomes `prompt_len - prefix_len`. While deciding whether the head request
  fits, use the cost it would have *right now* (hit or miss).
- Once a request has started prefill its cost is fixed; later cache changes don't affect it.
- **Insert** `prefix_id` when a request carrying it finishes prefill.
- The cache is LRU over `prefix_id`s with capacity `prefix_cache_size`. A hit
  and an insert both make that id most recently used.
- `prompt_len > max_work` is still rejected without chunked prefill, hits or not.

### `cache_stats() -> {"hits": int, "misses": int}`
Counted once per lookup, only for requests that have a `prefix_id`.

## Example (max_work = 10, prefix_cache_size = 2)
```
R0 = (8, 1, prefix "sys", 6)   R1 = (8, 1, prefix "sys", 6)
step 1  prefill [0, 1]   R0 misses (8 units) and inserts "sys"; R1 hits (2 units)
cache_stats() -> {"hits": 1, "misses": 1}
```
