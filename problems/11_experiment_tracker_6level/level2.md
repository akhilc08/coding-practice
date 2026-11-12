# Level 2 — Leaderboard

### `best_experiments(timestamp, metric, n, mode="max") -> list[str]`
For each experiment that has logged `metric`, take its **best** value: the
maximum if `mode == "max"`, the minimum if `mode == "min"`. Return up to `n`
entries formatted `"exp_id(best)"`, best first (highest for `"max"`, lowest for
`"min"`), ties broken by `exp_id` ascending.

## Example
```
e1 loss: 90, 70      e2 loss: 60, 80      e3: no loss
t.best_experiments(10, "loss", 5, "min")   # ["e2(60)", "e1(70)"]
t.best_experiments(11, "loss", 1)          # ["e1(90)"]
```
