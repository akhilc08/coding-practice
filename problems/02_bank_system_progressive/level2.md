# Level 2 — Top Spenders

**Suggested time: 15 min.** Earlier tests must keep passing.

### `top_spenders(timestamp, n) -> list[str]`
Return the top `n` accounts ranked by **total outgoing money**, formatted
`"<account_id>(<total_outgoing>)"`.

- Outgoing money = the sum of all **successful** outgoing transfers (and, from
  Level 3 on, payments).
- Sort by total outgoing **descending**; break ties by `account_id`
  **ascending**.
- Accounts with 0 outgoing are included.
- If there are fewer than `n` accounts, return all of them.

## Example
```
bank.create_account(1, "c")
bank.create_account(2, "a")
bank.create_account(3, "b")
bank.deposit(4, "a", 1000)
bank.deposit(5, "b", 1000)
bank.transfer(6, "a", "c", 300)
bank.transfer(7, "b", "c", 300)
bank.transfer(8, "a", "b", 100)
bank.top_spenders(9, 2)     # ["a(400)", "b(300)"]
bank.top_spenders(10, 5)    # ["a(400)", "b(300)", "c(0)"]
```
