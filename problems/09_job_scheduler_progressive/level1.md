# Level 1 — Jobs and Dependencies

**Suggested time: 15 min.** Only open `level2.md` after `pytest test_level1.py` passes.

You're building a build/CI job scheduler. Jobs can depend on other jobs.

### `add_job(job_id, duration) -> bool`
`duration` is a positive int. Return `False` if the job already exists.

### `add_dependency(job_id, depends_on) -> bool`
`job_id` can't start until `depends_on` finishes. Return `False` (and add
nothing) if either job doesn't exist, `job_id == depends_on`, or this exact
dependency already exists.

### `get_order() -> list[str]`
Return every job in an order where each job comes after all its dependencies.
When several jobs are ready at once, pick the one with the **smallest ID**
(alphabetically) first. Assume no cycles at this level.

## Example
```
s.add_job("test", 5); s.add_job("build", 3); s.add_job("lint", 1)
s.add_dependency("test", "build")
s.get_order()        # ["build", "lint", "test"]
```
`build` and `lint` are both ready at the start, and `build` < `lint`. After
`build`, both `lint` and `test` are ready, and `lint` < `test`.
