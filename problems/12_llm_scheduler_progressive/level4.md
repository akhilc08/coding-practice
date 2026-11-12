# Level 4 — KV memory and preemption

GPU memory is finite. Add `kv_capacity` to the constructor (`None` = unlimited).

- A request **reserves `prompt_len` units** the moment it receives its first
  prefill work (cached prefix tokens count, since the KV is copied in). Each
  generated token uses **1 more unit**. Finishing frees everything it held.
- `add` returns `False` if `prompt_len + max_tokens > kv_capacity`.
- **Prefill:** a request that hasn't started can only start if its
  `prompt_len` fits in free memory. If the head can't start, stop (as before).
- **Decode:** before a request decodes, if memory is full, **preempt** the
  request that most recently started prefill (it may be in `admitted` or be a
  partly prefilled head of `waiting`). Repeat until a unit is free. If the
  victim is the request about to decode, it doesn't decode; move on to the next.
- **Preemption:** free all its memory, `reset(req)`, put it at the **front** of
  `waiting`, set its `"first_token"` metric back to `None`, and bump its
  `"preemptions"` count. It starts from scratch later, including a fresh cache
  lookup. Budget already spent this step stays spent.
- `step()` also returns `"preempted": [ids preempted this step, in order]`.
- `metrics()` gains `"preemptions"` (0 if never preempted).

### `memory_used() -> int`

## Example (max_work = 10, kv_capacity = 10)
```
R0 = (4, 4)  R1 = (4, 4)
step 1  prefill [0, 1]                       mem 8
step 2  decode [0, 1]                        mem 10
step 3  memory full: preempt R1, R0 decodes; R1 restarts prefill
        decode [0]  prefill [1]  preempted [1]     mem 10
```
