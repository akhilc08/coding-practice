# Level 3 — Sliding Windows

**Suggested time: 25 min.** Earlier tests must keep passing.

Fixed windows let a client burst: 2 requests at `999` and 2 more at `1000`
all pass a "2 per second" limit. Add a sliding mode.

### `set_limit(client_id, max_requests, window_ms, mode="fixed") -> None`
`mode` is `"fixed"` (Level 1 behavior, the default) or `"sliding"`.

In **sliding** mode, a request at time `t` is allowed if the client has made
fewer than `max_requests` allowed requests in the window `(t - window_ms, t]`.
A request exactly `window_ms` ago **no longer counts**.

`get_usage` in sliding mode returns the number of allowed requests in
`(t - window_ms, t]`.

## Example
```
rl.set_limit("a", 2, 1000, "sliding")
rl.allow(0, "a")      # True
rl.allow(500, "a")    # True
rl.allow(999, "a")    # False
rl.allow(1000, "a")   # True   (request at 0 has dropped out)
rl.allow(1001, "a")   # False  (500 and 1000 are in the window)
rl.get_usage(1500, "a")  # 1   (only 1000; 500 is exactly 1000 ago)
```
