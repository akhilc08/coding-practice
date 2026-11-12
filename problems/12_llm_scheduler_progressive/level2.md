# Level 2 — Chunked prefill + latency metrics

Long prompts block the queue. Add `chunked_prefill=True` to the constructor.

### Chunked prefill (only when `chunked_prefill=True`)
- `add` no longer rejects `prompt_len > max_work`.
- In the prefill phase, if the head request's remaining prompt fits in the
  budget, prefill all of it and keep going. If it doesn't fit, prefill as much
  as the budget allows (`prefill(req, n)`), leave it at the head of the queue,
  and stop.
- A request appears in the step's `"prefill"` list if it received **any**
  prefill work that step.
- It is admitted only once its whole prompt is prefilled, and decodes starting
  the next step.

With `chunked_prefill=False`, everything behaves exactly as in Level 1.

### `metrics(req_id) -> dict | None`
`None` for an unknown id. Otherwise a dict containing:
- `"arrival"`: number of steps that had completed when the request was added (0 before the first step)
- `"first_token"`: the step number (1-based) in which it decoded its first token, else `None`
- `"finished"`: the step number in which it finished, else `None`

## Example (max_work = 4, chunked)
```
R0 = (10, 2)  R1 = (3, 1)
step 1  prefill [0]       R0 4/10
step 2  prefill [0]       R0 8/10
step 3  prefill [0, 1]    R0 done (2 units), R1 gets 2/3
step 4  decode [0]  prefill [1]   R1 done
step 5  decode [0, 1]     both finish
metrics(0) -> {"arrival": 0, "first_token": 4, "finished": 5, ...}
```
