from solution import Bank

DAY = 86_400_000


def test_example():
    bank = Bank()
    bank.create_account(1, "a")
    bank.deposit(2, "a", 1000)
    assert bank.pay(3, "a", 250) == "payment1"
    assert bank.get_payment_status(4, "a", "payment1") == "IN_PROGRESS"
    assert bank.deposit(3 + DAY, "a", 10) == 765
    assert bank.get_payment_status(3 + DAY + 1, "a", "payment1") == "CASHBACK_RECEIVED"


def test_pay_failures():
    bank = Bank()
    assert bank.pay(1, "nope", 10) is None
    bank.create_account(2, "a")
    bank.deposit(3, "a", 5)
    assert bank.pay(4, "a", 6) is None
    assert bank.deposit(5, "a", 0 + 1) == 6


def test_payment_ids_global_and_only_on_success():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "a", 100)
    bank.deposit(4, "b", 100)
    assert bank.pay(5, "a", 10) == "payment1"
    assert bank.pay(6, "b", 1000) is None
    assert bank.pay(7, "b", 10) == "payment2"
    assert bank.pay(8, "a", 10) == "payment3"


def test_cashback_rounds_down():
    bank = Bank()
    bank.create_account(1, "a")
    bank.deposit(2, "a", 100)
    bank.pay(3, "a", 49)  # 2% of 49 = 0.98 -> 0
    bank.pay(4, "a", 51)  # 2% of 51 = 1.02 -> 1
    assert bank.deposit(4 + DAY, "a", 0 + 1) == 0 + 0 + 1 + 1


def test_cashback_not_before_due():
    bank = Bank()
    bank.create_account(1, "a")
    bank.deposit(2, "a", 1000)
    bank.pay(10, "a", 1000)
    assert bank.deposit(10 + DAY - 1, "a", 1) == 1
    assert bank.get_payment_status(10 + DAY - 1 + 1, "a", "payment1") == "CASHBACK_RECEIVED"
    assert bank.deposit(10 + DAY + 5, "a", 1) == 1 + 20 + 1


def test_cashback_applied_on_any_operation():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "a", 100)
    bank.pay(4, "a", 100)                       # balance 0, cashback 2 due later
    # transfer at due time must see the cashback first
    assert bank.transfer(4 + DAY, "a", "b", 2) == 0


def test_status_wrong_account_or_unknown():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "a", 100)
    bank.pay(4, "a", 10)
    assert bank.get_payment_status(5, "b", "payment1") is None
    assert bank.get_payment_status(6, "a", "payment99") is None
    assert bank.get_payment_status(7, "zzz", "payment1") is None


def test_payments_count_as_spending_and_cashback_doesnt_reduce():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "a", 1000)
    bank.deposit(4, "b", 1000)
    bank.pay(5, "a", 500)
    bank.transfer(6, "b", "a", 400)
    assert bank.top_spenders(7, 2) == ["a(500)", "b(400)"]
    assert bank.top_spenders(5 + DAY, 2) == ["a(500)", "b(400)"]
