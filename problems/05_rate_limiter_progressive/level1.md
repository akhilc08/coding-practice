# Level 1 — Fixed-Window Limits

**Suggested time: 15 min.** Only open `level2.md` after `pytest test_level1.py` passes.

You're building an API rate limiter. Every request has a `timestamp` (an `int`,
milliseconds). Timestamps across calls are **non-decreasing**.

### `set_limit(client_id, max_requests, window_ms) -> None`
Allow `client_id` at most `max_requests` requests per window. Windows are
**fixed** and aligned to multiples of `window_ms`: with `window_ms = 1000`, the
windows are `[0, 1000)`, `[1000, 2000)`, and so on.

Calling `set_limit` again for the same client **replaces** the rule and
**resets** the client's usage (earlier requests no longer count).

### `allow(timestamp, client_id) -> bool`
Return `True` if the request is allowed, `False` if it would exceed the limit.
- Clients with no limit set are always allowed.
- **Denied requests don't count** toward the limit.

## Example
```
rl.set_limit("a", 2, 1000)
rl.allow(0, "a")      # True
rl.allow(500, "a")    # True
rl.allow(999, "a")    # False  (2 already used in [0, 1000))
rl.allow(1000, "a")   # True   (new window)
rl.allow(5, "b")      # True   (no limit for b)
```
