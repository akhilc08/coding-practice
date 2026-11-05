# Level 1 — Workers and Office Time

**Suggested time: 15 min.** Only open `level2.md` after `pytest test_level1.py` passes.

You're building a system that tracks when workers enter and leave the office.

### `add_worker(worker_id, position, compensation) -> bool`
Add a worker with a job `position` (string) and `compensation` (int, pay per
unit of time). Return `False` if the worker already exists.

### `register(worker_id, timestamp) -> str`
Record the worker passing through the office door at `timestamp`. The first
call means they **entered**, the next means they **left**, then entered
again, and so on. Return `"registered"`, or `"invalid_request"` if the worker
doesn't exist. Timestamps are strictly increasing per worker.

### `get(worker_id) -> int | None`
Return the total time the worker has spent in the office across all
**completed** sessions (an enter followed by a leave). A session in progress
doesn't count. Return `None` if the worker doesn't exist.

## Example
```
t.add_worker("ann", "junior", 10)    # True
t.add_worker("ann", "senior", 99)    # False
t.register("ann", 100)               # "registered"  (enter)
t.register("ann", 150)               # "registered"  (leave)  -> 50
t.register("ann", 200)               # "registered"  (enter)
t.get("ann")                         # 50
t.register("ann", 230)               # "registered"  (leave)  -> 30
t.get("ann")                         # 80
t.register("bob", 1)                 # "invalid_request"
```
