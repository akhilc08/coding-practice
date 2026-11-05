# Level 3 — Promotions and Salary

**Suggested time: 25 min.** Earlier tests must keep passing.

### `promote(worker_id, new_position, new_compensation, start_timestamp) -> str`
Schedule a promotion. It takes effect the **next time the worker enters** the
office at a timestamp `>= start_timestamp` (a session already in progress
keeps the old position and pay). Return `"success"`, or `"invalid_request"`
if the worker doesn't exist or already has a promotion pending.

After a promotion takes effect:
- `get(worker_id)` still returns **all-time** completed office time.
- `top_n_workers` ranks the worker under the new position, counting only
  completed sessions that started **at or after** the promotion took effect.

### `calc_salary(worker_id, start, end) -> int | None`
Return the worker's pay for the period `[start, end)`: for every completed
session, take the part that overlaps `[start, end)` and multiply its length by
the compensation that applied to **that session**. Return `None` if the
worker doesn't exist.

## Example
```
t.add_worker("a", "dev", 10)
t.register("a", 0);   t.register("a", 100)        # 100 time @ 10
t.promote("a", "lead", 20, 150)                   # "success"
t.promote("a", "cto", 99, 150)                    # "invalid_request" (pending)
t.register("a", 120); t.register("a", 140)        # enter at 120 < 150: still dev
t.register("a", 200); t.register("a", 250)        # enter at 200: now lead @ 20
t.get("a")                                        # 170
t.top_n_workers(5, "lead")                        # ["a(50)"]
t.top_n_workers(5, "dev")                         # []
t.calc_salary("a", 50, 225)                       # 50*10 + 20*10 + 25*20 = 1200
```
