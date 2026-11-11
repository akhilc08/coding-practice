# Bug Squash — Log Analyzer

**Suggested time: 40 min.**

A teammate wrote `solution.py` to analyze API access logs for the on-call
dashboard. The dashboard numbers look wrong. `test_logs.py` describes the **correct** behavior below.

**Your job:** find and fix the bugs. There are **9**. Use small, targeted fixes,
and write a one-line `# BUG:` comment above each fix explaining what was wrong.
Last time you also "fixed" code that wasn't broken, so this time **only change
a line if you can name the input that makes it misbehave**.

---

## Spec (correct behavior)

### Log line format
```
<timestamp> <METHOD> <path> <status> <latency>ms
```
Example: `1700000000 GET /api/users?page=2 200 123ms`, where the timestamp is
int seconds, the status is an int, and the latency is an int followed by `ms`.

### `ingest(line) -> bool`
Parse and store the line. Return `False` and count it as **invalid** if:
- it doesn't have exactly 5 whitespace-separated fields,
- the timestamp or status isn't an int, or
- the latency doesn't end with `ms`, or the part before `ms` isn't an int.

Invalid lines are not stored in any way.

**Path normalization** (applied before storing):
1. Drop the query string: everything from the first `?` onward.
2. Drop a trailing `/`, **except** when the path is just `/`.

So `/api/users/?x=1` becomes `/api/users`, and `/` stays `/`.

### `invalid_count() -> int`

### `count_by_status() -> dict[int, int]`
A new dict each call; mutating it doesn't affect the analyzer.

### `error_rate() -> float`
Fraction of **valid** requests with status `>= 500`. `0.0` if there are no valid
requests.

### `top_paths(n) -> list[str]`
Up to `n` normalized paths by request count, `"path(count)"`, count descending,
ties by path ascending.

### `p95_latency() -> int | None`
Nearest-rank 95th percentile: sort the latencies, then take the element at
index `ceil(0.95 * N) - 1`. `None` if there are no valid requests.

### `requests_in_window(start, end) -> int`
Number of valid requests with `start <= timestamp < end`.
