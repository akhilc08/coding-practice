# Level 1 — Accounts, Deposits, Transfers

**Suggested time: 15 min.** Only open `level2.md` after `pytest test_level1.py` passes.

You're building a simple banking system. Every method takes a `timestamp`
(an `int`, milliseconds). Timestamps across calls are **strictly increasing**.
All amounts are positive integers.

### `create_account(timestamp, account_id) -> bool`
Create a new account with balance 0. Return `False` if it already exists.

### `deposit(timestamp, account_id, amount) -> int | None`
Add `amount` to the account. Return the new balance, or `None` if the account
doesn't exist.

### `transfer(timestamp, source_id, target_id, amount) -> int | None`
Move `amount` from `source_id` to `target_id`. Return the **source's** new
balance. Return `None` (and change nothing) if:
- either account doesn't exist,
- `source_id == target_id`, or
- the source has insufficient funds.

## Example
```
bank.create_account(1, "a")          # True
bank.create_account(2, "a")          # False
bank.create_account(3, "b")          # True
bank.deposit(4, "a", 500)            # 500
bank.transfer(5, "a", "b", 200)      # 300
bank.transfer(6, "a", "b", 1000)     # None (insufficient funds)
bank.deposit(7, "b", 1)              # 201
```
