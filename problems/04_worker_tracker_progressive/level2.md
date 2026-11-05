# Level 2 — Top Workers by Position

**Suggested time: 15 min.** Earlier tests must keep passing.

### `top_n_workers(n, position) -> list[str]`
Return up to `n` workers whose **current** position is `position`, formatted
`"<worker_id>(<time>)"` where `time` is their completed office time. Sort by
time **descending**, ties by `worker_id` **ascending**. Workers with 0 time
are included. Return `[]` if nobody has that position.

## Example
```
t.add_worker("a", "dev", 1)
t.add_worker("b", "dev", 1)
t.add_worker("c", "pm", 1)
t.register("a", 0);  t.register("a", 10)
t.register("b", 0);  t.register("b", 30)
t.top_n_workers(5, "dev")    # ["b(30)", "a(10)"]
t.top_n_workers(5, "pm")     # ["c(0)"]
t.top_n_workers(5, "ceo")    # []
```
