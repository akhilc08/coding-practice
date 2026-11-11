# Level 3 — Parallel Workers

**Suggested time: 25 min.** Earlier tests must keep passing.

Simulate running every job with `workers` parallel workers (`workers >= 1`),
starting at time `0`:
- A job is **ready** once all its dependencies have **finished**. A job that
  finishes at time `t` unblocks dependents that can start at time `t`.
- Whenever workers are free, they take ready jobs **smallest ID first**.
- A job runs for `duration` time units without interruption.

### `get_start_times(workers) -> dict[str, int]`
Map each job to its start time.

### `total_time(workers) -> int`
Time when the last job finishes (`0` if there are no jobs).

These are queries: they don't change the scheduler's state.

## Example
```
add_job a 3, b 2, c 4, d 1;  d depends on a and b
s.get_start_times(2)   # {"a": 0, "b": 0, "c": 2, "d": 3}
s.total_time(2)        # 6   (c runs 2..6)
s.total_time(1)        # 10
```
At `t=0`, `a` and `b` start. At `t=2`, `b` finishes; `c` is ready (`d` still
waits on `a`), so `c` starts. At `t=3`, `a` finishes and `d` starts.
