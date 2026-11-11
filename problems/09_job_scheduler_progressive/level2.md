# Level 2 — Cycles and Transitive Dependencies

**Suggested time: 20 min.** Earlier tests must keep passing.

### `add_dependency` now rejects cycles
Return `False` (and add nothing) if adding the dependency would create a
cycle, e.g. `a` depends on `b` and you try to make `b` depend on `a`, directly
or through a longer chain.

### `get_dependencies(job_id) -> list[str] | None`
Return **all** jobs that must finish before `job_id` can start (direct and
indirect), sorted by ID. Return `None` if the job doesn't exist.

## Example
```
add_job a, b, c, d
s.add_dependency("c", "b")      # True
s.add_dependency("b", "a")      # True
s.add_dependency("a", "c")      # False  (a -> c -> b -> a)
s.get_dependencies("c")         # ["a", "b"]
s.get_dependencies("d")         # []
```
