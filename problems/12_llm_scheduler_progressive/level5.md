# Level 5 — Load balancing across replicas

Implement `Cluster` in `cluster.py`: `num_replicas` independent `Scheduler`s,
all built with the same `max_work` and `**scheduler_kwargs`. You'll likely
need to add a few small helpers to `Scheduler`.

### Load
A replica's load = number of admitted requests + sum over its waiting requests
of (`prompt_len - prefilled`).

### `add(req) -> int`
Route the request and return the replica index, or `-1` if rejected (duplicate
`req_id` anywhere in the cluster, or the replica's own `add` rejects it).
1. Only non-draining replicas are candidates. None left: `-1`.
2. If `req.prefix_id` is in some candidates' prefix caches, narrow to those.
3. Pick the least loaded; ties go to the lowest index.

### `step() -> list[dict]`
Step every replica (draining ones too) and return their results, by index.

### `replica_of(req_id)`, `metrics(req_id)`
Where it currently lives / its metrics there. `None` if unknown.

### `drain(idx) -> list[int]`
Stop routing to replica `idx`. Move its waiting requests that **haven't
started prefill** to other replicas, one at a time in queue order, using the
same routing rule. Moved requests keep their metrics (arrival etc.). Admitted
and partly prefilled requests stay and finish where they are. Return the moved
ids in order. Return `[]` for a bad index or a replica already draining; if no
other replica is accepting work, it still becomes draining but nothing moves.
