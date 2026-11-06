"""Bank system — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/02_bank_system_progressive/test_level1.py
"""

from __future__ import annotations

from argparse import _ActionsContainer
from collections import defaultdict
from time import time



class Bank:
    def __init__(self) -> None:
        self.DAY = 86_400_000
        self.accounts = {}
        self.outgoing = {}
        self.pay_counter = 1
        self.payments = {}
        self.history = defaultdict(list)

    # ---- Level 1 ----
    def create_account(self, timestamp: int, account_id: str) -> bool:
        self.process_cashback(timestamp)

        if account_id in self.accounts: return False
        self.accounts[account_id] = 0
        self.outgoing[account_id] = 0
        self.record(account_id, timestamp)
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self.process_cashback(timestamp)
        if account_id not in self.accounts: return None
        self.accounts[account_id]+=amount
        self.record(account_id, timestamp)
        return self.accounts[account_id]

    def transfer(
        self, timestamp: int, source_id: str, target_id: str, amount: int
    ) -> int | None:
        self.process_cashback(timestamp)
        if source_id not in self.accounts or target_id not in self.accounts or source_id == target_id or self.accounts[source_id] < amount: return None
        self.accounts[source_id] -= amount
        self.outgoing[source_id] += amount
        self.accounts[target_id] += amount
        self.record(source_id, timestamp)
        self.record(target_id, timestamp)
        return self.accounts[source_id]

    # ---- Level 2 ----
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        self.process_cashback(timestamp)
        accounts = sorted(self.outgoing.items(), key = lambda kv: (-kv[1], kv[0]))
        res = []
        for k1, k2 in accounts:
            if len(res) == n: break
            res.append(f"{k1}({k2})")

        return res
    # ---- Level 3 ----
    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        self.process_cashback(timestamp)
        if account_id not in self.accounts or self.accounts[account_id] < amount: return None
        self.accounts[account_id] -= amount
        self.outgoing[account_id] += amount
        id = "payment"+str(self.pay_counter)
        cashback = amount*2 // 100
        time = timestamp+self.DAY
        self.payments[id] = [account_id, cashback, time, False]
        self.pay_counter += 1
        self.record(account_id, timestamp)
        return id

    def process_cashback(self, timestamp):
        for id, payment in self.payments.items():
            if payment[2] <= timestamp and not payment[3]:
                self.accounts[payment[0]] += payment[1]
                payment[3] = True
                self.record(payment[0], payment[2])


    def get_payment_status(
        self, timestamp: int, account_id: str, payment: str
    ) -> str | None:
        self.process_cashback(timestamp)
        if payment not in self.payments: return None
        if self.payments[payment][3] and self.payments[payment][0] == account_id: return "CASHBACK_RECEIVED"
        if not self.payments[payment][3] and self.payments[payment][0] == account_id: return "IN_PROGRESS"

        return None


    # ---- Level 4 ----
    def merge_accounts(
        self, timestamp: int, account_id_1: str, account_id_2: str
    ) -> bool:
        self.process_cashback(timestamp)
        if account_id_1 not in self.accounts or account_id_2 not in self.accounts or account_id_1 == account_id_2: return False

        self.accounts[account_id_1] += self.accounts[account_id_2]
        self.outgoing[account_id_1] += self.outgoing[account_id_2]

        for id, payment in self.payments.items():
            if payment[0] == account_id_2:
                payment[0] = account_id_1

        self.accounts.pop(account_id_2)
        self.outgoing.pop(account_id_2)
        self.record(account_id_1, timestamp)
        self.record(account_id_2, timestamp)
        return True


    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        self.process_cashback(timestamp)

        if account_id not in self.history: return None
        history = self.history[account_id]
        for i in range(len(history)):
            if history[i][1] <= time_at and (i+1 == len(history) or history[i+1][1] >time_at):
                return history[i][0]
        return None


    def record(self, account_id, timestamp):
        bal = self.accounts.get(account_id, None)
        self.history[account_id].append((bal, timestamp))
