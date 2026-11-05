# Level 4 — Double-Paid Periods

**Suggested time: 30 min.** Earlier tests must keep passing.

### `set_double_paid(start, end) -> None`
Declare that office time during `[start, end)` is paid **double** for every
worker. This applies retroactively and to future sessions. Multiple periods
may overlap — overlapping time is still only doubled once (×2, never ×4).

`calc_salary` must now account for double-paid periods.

## Example
```
t.add_worker("a", "dev", 10)
t.register("a", 0); t.register("a", 100)
t.set_double_paid(20, 40)
t.set_double_paid(30, 60)            # union with the first: [20, 60)
t.calc_salary("a", 0, 100)           # 60*10 + 40*20 = 1400
t.calc_salary("a", 50, 100)          # 10*20 + 40*10 = 600
```
