# Level 4 — Flaky Jobs

**Suggested time: 25 min.** Earlier tests must keep passing.

### `set_failures(job_id, k) -> bool`
The job will **fail its first `k` attempts** in each simulation (`k >= 0`;
setting it again replaces the old value). Return `False` if the job doesn't
exist.

In the simulation, a failed attempt still occupies its worker for the full
`duration`. When it fails, the job goes back to being **ready** and competes
for a worker like any other ready job (smallest ID first, at that same moment).
Dependents are unblocked only by the **successful** attempt.

`get_start_times` now reports the start of each job's **successful** attempt.

`get_order` is unaffected.

## Example
```
add_job a 2, b 3;  b depends on a
s.set_failures("a", 2)
s.get_start_times(1)   # {"a": 4, "b": 6}   (a fails at 0..2 and 2..4)
s.total_time(1)        # 9
```
