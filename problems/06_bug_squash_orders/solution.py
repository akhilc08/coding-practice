"""Order system — bug squash.

Read spec.md first. This code has 8 bugs. Fix them so that
`pytest problems/06_bug_squash_orders` passes.
"""

from __future__ import annotations

from collections import defaultdict


class OrderSystem:
    def __init__(self, catalog: dict = {}) -> None:
        self.products = catalog  # sku -> [price, stock]
        self.coupons = {}  # code -> (percent_off, min_total)
        self.orders = {}  # order_id -> {"items", "total", "coupon", "cancelled"}

    def add_product(self, sku: str, price: int, stock: int) -> bool:
        if sku in self.products:
            return False
        self.products[sku] = [price, stock]
        return True

    def restock(self, sku: str, qty: int) -> int | None:
        if sku not in self.products:
            return None
        current = self.products[sku][1]
        self.products[sku][1] += qty
        return current

    def get_stock(self, sku: str) -> int | None:
        return self.products[sku][1] if sku in self.products else None

    def create_order(self, order_id: str, items: dict[str, int]) -> int | None:
        if order_id in self.orders or not items:
            return None
        total = 0
        for sku, qty in items.items():
            if sku not in self.products or self.products[sku][1] < qty:
                return None
            self.products[sku][1] -= qty
            total += self.products[sku][0] * qty
        self.orders[order_id] = {"items": items, "total": total, "coupon": None, "cancelled": False}
        return total

    def add_coupon(self, code: str, percent_off: int, min_total: int) -> bool:
        if code in self.coupons:
            return False
        self.coupons[code] = (percent_off, min_total)
        return True

    def apply_coupon(self, order_id: str, code: str) -> int | None:
        order = self.orders.get(order_id)
        if order is None or code not in self.coupons:
            return None
        if order["cancelled"] or order["coupon"] is not None:
            return None
        pct, min_total = self.coupons[code]
        if order["total"] <= min_total:
            return None
        order["total"] -= round(order["total"] * pct / 100)
        order["coupon"] = code
        return order["total"]

    def get_total(self, order_id: str) -> int | None:
        return self.orders[order_id]["total"] if order_id in self.orders else None

    def cancel_order(self, order_id: str) -> bool:
        order = self.orders.get(order_id)
        if order is None or order["cancelled"]:
            return False
        for sku, qty in order["items"].items():
            self.products[sku][1] += qty
        return True

    def top_products(self, n: int) -> list[str]:
        sold = defaultdict(int)
        for order in self.orders.values():
            if not order["cancelled"]:
                for sku, qty in order["items"].items():
                    sold[sku] += qty
        ranked = sorted(sold.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        return [f"{sku}({units})" for sku, units in ranked[:n]]
