# Level 5 — History and Deletion

### `get_value_at(timestamp, exp_id, metric, time_at) -> int | None`
The value of `metric` as of `time_at`: the most recent value logged at a
timestamp `<= time_at`. `None` if the experiment doesn't exist or nothing was
logged by then.

A forked experiment's copied history keeps its **original** timestamps.

### `delete_experiment(timestamp, exp_id) -> bool`
Remove the experiment entirely (metrics, tags, everything). `False` if it
doesn't exist. Its ID can be reused by `create_experiment` or `fork` afterward,
starting fresh.

## Example
```
t.log_metric(10, "e1", "loss", 9)
t.log_metric(20, "e1", "loss", 5)
t.get_value_at(25, "e1", "loss", 15)   # 9
t.get_value_at(26, "e1", "loss", 5)    # None
t.delete_experiment(27, "e1")          # True
t.get_latest(28, "e1", "loss")         # None
```
