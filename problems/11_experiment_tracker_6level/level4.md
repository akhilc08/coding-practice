# Level 4 — Forking

### `fork(timestamp, src_id, new_id) -> bool`
Create `new_id` as a copy of `src_id`: all of its metric history and tags.
After forking, the two experiments are **completely independent**: logging or
tagging one never affects the other. `False` if `src_id` doesn't exist or
`new_id` already exists.

## Example
```
t.log_metric(1, "e1", "loss", 50)
t.fork(2, "e1", "e1b")                # True
t.log_metric(3, "e1b", "loss", 40)    # 2   (history was copied)
t.get_latest(4, "e1", "loss")         # 50  (original untouched)
```
