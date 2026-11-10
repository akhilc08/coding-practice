# Level 2 — Usage and Abuse Report

**Suggested time: 15 min.** Earlier tests must keep passing.

### `get_usage(timestamp, client_id) -> int | None`
Return how many **allowed** requests the client has made in its current window
(the window containing `timestamp`). Return `None` if the client has no limit.

### `top_blocked(n) -> list[str]`
Return up to `n` clients with the most **denied** requests, formatted as
`"client(count)"`, sorted by count descending, ties broken by client ID
ascending. Clients with 0 denied requests are not included.

Denied counts are **lifetime totals**: `set_limit` does not reset them.

## Example
```
rl.set_limit("a", 1, 1000)
rl.set_limit("b", 1, 1000)
rl.allow(0, "a"); rl.allow(1, "a"); rl.allow(2, "a")   # True, False, False
rl.allow(3, "b"); rl.allow(4, "b")                     # True, False
rl.get_usage(5, "a")     # 1
rl.get_usage(1000, "a")  # 0   (new window)
rl.top_blocked(5)        # ["a(2)", "b(1)"]
```
