# Level 4 — Global Limit

**Suggested time: 25 min.** Earlier tests must keep passing.

### `set_global_limit(max_requests, window_ms) -> None`
Add a **sliding-window** limit shared across **all** clients (including clients
with no limit of their own). Calling it again replaces the global rule.

A request is allowed only if it passes **both** its client's limit (if any)
and the global limit. Then:
- An allowed request counts toward both.
- A denied request counts toward **neither**, no matter which limit denied it.
- A request denied by the global limit counts as a denied request for
  `top_blocked`.
- The global window counts **every** allowed request, including ones made
  before `set_global_limit` was called.

`get_usage` still reports only the client's own usage.

## Example
```
rl.set_global_limit(3, 1000)
rl.allow(0, "a")      # True
rl.allow(1, "b")      # True
rl.allow(2, "c")      # True
rl.allow(3, "a")      # False  (global: 3 in the last 1000 ms)
rl.allow(1000, "a")   # True   (request at 0 dropped out)
rl.top_blocked(5)     # ["a(1)"]
```
