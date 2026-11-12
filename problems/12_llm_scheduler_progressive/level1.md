# Level 1 — Prefill then decode

A request's life: it waits in a queue, gets **prefilled** (its whole prompt is
processed in one pass), then **decodes** one output token per step until it has
generated `max_tokens` tokens, at which point it is finished.

Time moves in discrete steps. Each `step()` has a budget of `max_work` work units.

### `add(req) -> bool`
Append to the waiting queue. Return `False` (and ignore the request) if a
request with the same `req_id` was already added, if `prompt_len <= 0` or
`max_tokens <= 0`, or if `prompt_len > max_work` (it could never be prefilled).

### `step() -> dict`
Run one step, in this order:

1. **Decode.** Every admitted request decodes one token (`decode_one`, cost 1),
   in admission order. If the budget runs out, the rest wait for the next step.
   A request whose `generated` reaches `max_tokens` moves to `finished`.
2. **Prefill.** Spend what's left on waiting requests in arrival order
   (`prefill`, cost `prompt_len`). If the request at the head of the queue
   doesn't fit, **stop**. Never skip it to fit a smaller one behind it.
   Prefilled requests move to `admitted`.

A request prefilled this step does not decode until the next step (that falls
out of the ordering above).

Return `{"decode": [ids decoded, in order], "prefill": [ids prefilled, in order]}`.
Keep `self.waiting`, `self.admitted`, `self.finished` up to date: tests read them.

## Example (max_work = 4)
```
R0 = (prompt 2, max_tokens 2)  R1 = (3, 1)  R2 = (1, 1)
step 1  {"decode": [],     "prefill": [0]}  R1 needs 3, only 2 left: stop
step 2  {"decode": [0],    "prefill": [1]}  R2 needs 1, 0 left
step 3  {"decode": [0, 1], "prefill": [2]}  R0 and R1 finish
step 4  {"decode": [2],    "prefill": []}   R2 finishes
```
