# Level 4 — Merging Accounts and Balance History

**Suggested time: 30 min.** Earlier tests must keep passing.

### `merge_accounts(timestamp, account_id_1, account_id_2) -> bool`
Merge `account_id_2` **into** `account_id_1`. Return `False` if the IDs are
equal or either account doesn't exist.

After a merge:
- account 1's balance increases by account 2's balance,
- account 1's outgoing total increases by account 2's outgoing total,
- account 2's pending cashbacks are paid to account 1 when due,
- account 2's payments can be queried with `get_payment_status` via
  account 1,
- account 2 no longer exists (operations on it fail; it may be re-created
  later as a brand-new account with balance 0).

### `get_balance(timestamp, account_id, time_at) -> int | None`
Return the account's balance at time `time_at` (`time_at <= timestamp`),
reflecting everything that happened at or before `time_at`, including
cashback that came due at or before `time_at`. Return `None` if the account
did not exist at `time_at`.

An account merged away stops existing at the merge timestamp, but queries for
earlier times still return its historical balance. If it's re-created later,
queries for times after re-creation see the new account.

## Example
```
bank.create_account(1, "a")
bank.create_account(2, "b")
bank.deposit(3, "a", 100)
bank.deposit(4, "b", 50)
bank.merge_accounts(5, "a", "b")      # True
bank.deposit(6, "a", 1)               # 151
bank.get_balance(7, "b", 4)           # 50
bank.get_balance(8, "b", 5)           # None (merged away at 5)
bank.get_balance(9, "a", 4)           # 100
bank.get_balance(10, "a", 5)          # 150
```
