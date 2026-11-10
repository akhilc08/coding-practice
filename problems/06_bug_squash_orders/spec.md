# Bug Squash — Order System

**Suggested time: 45 min.**

A teammate wrote `solution.py` and shipped it. Customers are complaining. The
tests in `test_orders.py` describe the **correct** behavior below, and many of
them fail.

**Your job:** find and fix the bugs. There are **8**. Fix them with small,
targeted edits; don't rewrite the class. Don't change the tests.

How to work it like the real round:
1. Run `pytest -x` so you look at one failure at a time.
2. Before you change anything, explain to yourself *why* the code produces the
   wrong value. Guessing until a test passes is what interviewers mark you down for.
3. Some failures are caused by a bug somewhere other than the method being
   tested.

---

## Spec (correct behavior)

Prices are integers in cents.

### `OrderSystem(catalog=None)`
Optional starting catalog: `{sku: [price, stock]}`. Each `OrderSystem` has its
own independent state, and the caller's `catalog` dict is never modified.

### `add_product(sku, price, stock) -> bool`
`False` if the SKU already exists.

### `restock(sku, qty) -> int | None`
Add stock. Return the **new** stock level, or `None` if the SKU doesn't exist.

### `get_stock(sku) -> int | None`

### `create_order(order_id, items) -> int | None`
`items` is `{sku: qty}`. Deduct stock and return the order total. Return `None`
and change **nothing** if the order ID already exists, `items` is empty, any SKU
doesn't exist, or **any** item has insufficient stock. The order is stored as it
was at creation: if the caller later mutates their `items` dict, the order doesn't
change.

### `add_coupon(code, percent_off, min_total) -> bool`
`False` if the code already exists.

### `apply_coupon(order_id, code) -> int | None`
Apply a percentage discount and return the new total. The discount is rounded
**down**: `total - total * percent_off // 100`. Return `None` (change nothing)
if the order or coupon doesn't exist, the order is cancelled, the order already
has a coupon, or the order total is **less than** `min_total` (a total exactly
equal to `min_total` qualifies).

### `get_total(order_id) -> int | None`

### `cancel_order(order_id) -> bool`
Return stock to inventory. Return `False` if the order doesn't exist or was
already cancelled.

### `top_products(n) -> list[str]`
Up to `n` SKUs by units sold in **non-cancelled** orders, formatted
`"sku(units)"`, sorted by units descending, ties by SKU ascending.
