# Level 3 — Tags

### `add_tag(timestamp, exp_id, tag) -> bool`
`False` if the experiment doesn't exist or already has the tag.

### `find_by_tags(timestamp, tags) -> list[str]`
IDs of experiments that have **all** of `tags`, sorted ascending. An empty
`tags` list matches every experiment.

## Example
```
t.add_tag(1, "e1", "baseline"); t.add_tag(2, "e1", "lr=1e-3")
t.add_tag(3, "e2", "lr=1e-3")
t.find_by_tags(4, ["lr=1e-3"])               # ["e1", "e2"]
t.find_by_tags(5, ["lr=1e-3", "baseline"])   # ["e1"]
```
