# Level 3 — Payments with Delayed Cashback

**Suggested time: 25 min.** Earlier tests must keep passing.

### `pay(timestamp, account_id, amount) -> str | None`
Withdraw `amount` from the account immediately. Return a payment ID string:
`"payment1"`, `"payment2"`, … — the counter is **global across all accounts**
and only increments on successful payments. Return `None` (change nothing) if
the account doesn't exist or has insufficient funds.

Payments count toward the account's outgoing total for `top_spenders`.

**Cashback:** each payment earns 2% cashback, rounded **down**
(`amount * 2 // 100`), deposited into the account exactly
`86_400_000` ms (24 hours) after the payment's timestamp.

Cashback must be applied **before** any other operation is processed at a
timestamp at or after it's due. For example, if cashback is due at `T` and the
next call is `deposit(T, ...)`, the cashback is applied first. Cashback does
**not** reduce the outgoing total.

### `get_payment_status(timestamp, account_id, payment) -> str | None`
Return `"IN_PROGRESS"` or `"CASHBACK_RECEIVED"`. Return `None` if the account
doesn't exist, the payment doesn't exist, or the payment belongs to a
different account.

## Example
```
DAY = 86_400_000
bank.create_account(1, "a")
bank.deposit(2, "a", 1000)
bank.pay(3, "a", 250)                         # "payment1"; balance 750
bank.get_payment_status(4, "a", "payment1")   # "IN_PROGRESS"
bank.deposit(3 + DAY, "a", 10)                # cashback 5 applied first: 750+5+10 = 765
bank.get_payment_status(3 + DAY + 1, "a", "payment1")   # "CASHBACK_RECEIVED"
```
