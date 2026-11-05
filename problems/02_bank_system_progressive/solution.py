"""Bank system — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/02_bank_system_progressive/test_level1.py
"""

from __future__ import annotations


class Bank:
    def __init__(self) -> None:
        pass

    # ---- Level 1 ----
    def create_account(self, timestamp: int, account_id: str) -> bool:
        raise NotImplementedError

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        raise NotImplementedError

    def transfer(
        self, timestamp: int, source_id: str, target_id: str, amount: int
    ) -> int | None:
        raise NotImplementedError

    # ---- Level 2 ----
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        raise NotImplementedError

    # ---- Level 3 ----
    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        raise NotImplementedError

    def get_payment_status(
        self, timestamp: int, account_id: str, payment: str
    ) -> str | None:
        raise NotImplementedError

    # ---- Level 4 ----
    def merge_accounts(
        self, timestamp: int, account_id_1: str, account_id_2: str
    ) -> bool:
        raise NotImplementedError

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        raise NotImplementedError
