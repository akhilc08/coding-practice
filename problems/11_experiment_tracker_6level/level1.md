# Level 1 — Experiments and Metrics

You're building a tracker for ML experiments. Every method takes a `timestamp`
(int). Timestamps across calls are **strictly increasing**. Metric values are ints.

### `create_experiment(timestamp, exp_id) -> bool`
`False` if an experiment with that ID already exists.

### `log_metric(timestamp, exp_id, metric, value) -> int | None`
Record `value` for `metric` on the experiment. Return how many values have now
been logged for that metric on that experiment. `None` if the experiment
doesn't exist.

### `get_latest(timestamp, exp_id, metric) -> int | None`
The most recently logged value. `None` if the experiment or metric doesn't exist.

## Example
```
t.create_experiment(1, "e1")          # True
t.log_metric(2, "e1", "loss", 90)     # 1
t.log_metric(3, "e1", "loss", 70)     # 2
t.log_metric(4, "e1", "acc", 50)      # 1
t.get_latest(5, "e1", "loss")         # 70
t.get_latest(6, "e1", "f1")           # None
```
