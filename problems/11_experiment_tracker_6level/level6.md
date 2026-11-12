# Level 6 — Archiving Inactive Experiments

An experiment's **last activity** is the latest timestamp at which it was
created, forked into existence, had a metric logged, had a tag added, or was
restored. (Copied history from a fork does **not** count as activity for the
new experiment; the fork itself does.)

### `archive_inactive(timestamp, max_age) -> list[str]`
Archive every non-archived experiment whose last activity is at or before
`timestamp - max_age`. Return the newly archived IDs, sorted.

While archived, an experiment:
- still exists (`create_experiment` with its ID returns `False`),
- is **hidden** from `best_experiments` and `find_by_tags`,
- **rejects writes**: `log_metric` returns `None`, `add_tag` returns `False`,
- still answers reads: `get_latest`, `get_value_at`, and can be the **source**
  of a `fork` (the new experiment is not archived),
- can be deleted.

### `restore(timestamp, exp_id) -> bool`
Un-archive it (counts as activity). `False` if it doesn't exist or isn't archived.

## Example
```
t.create_experiment(0, "a")
t.create_experiment(5, "b")
t.log_metric(8, "a", "loss", 3)
t.archive_inactive(15, 10)          # ["b"]   (b last active at 5 <= 15-10)
t.log_metric(16, "b", "loss", 1)    # None
t.best_experiments(17, "loss", 5, "min")   # ["a(3)"]
t.restore(18, "b")                  # True
t.archive_inactive(27, 10)          # ["a"]   (a last active 8; b restored at 18)
```
