from solution import Bank

DAY = 86_400_000


def test_example():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "a", 100)
    bank.deposit(4, "b", 50)
    assert bank.merge_accounts(5, "a", "b") is True
    assert bank.deposit(6, "a", 1) == 151
    assert bank.get_balance(7, "b", 4) == 50
    assert bank.get_balance(8, "b", 5) is None
    assert bank.get_balance(9, "a", 4) == 100
    assert bank.get_balance(10, "a", 5) == 150


def test_merge_invalid():
    bank = Bank()
    bank.create_account(1, "a")
    assert bank.merge_accounts(2, "a", "a") is False
    assert bank.merge_accounts(3, "a", "nope") is False
    assert bank.merge_accounts(4, "nope", "a") is False


def test_merged_account_is_gone_and_can_be_recreated():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "b", 70)
    bank.merge_accounts(4, "a", "b")
    assert bank.deposit(5, "b", 1) is None
    assert bank.transfer(6, "a", "b", 1) is None
    assert bank.create_account(7, "b") is True
    assert bank.deposit(8, "b", 5) == 5
    assert bank.get_balance(9, "b", 3) == 70
    assert bank.get_balance(10, "b", 6) is None
    assert bank.get_balance(11, "b", 8) == 5


def test_merge_combines_outgoing():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.create_account(3, "c")
    bank.deposit(4, "a", 100)
    bank.deposit(5, "b", 100)
    bank.transfer(6, "a", "c", 30)
    bank.transfer(7, "b", "c", 50)
    bank.merge_accounts(8, "c", "a")
    assert bank.top_spenders(9, 5) == ["b(50)", "c(30)"]


def test_pending_cashback_goes_to_merged_account():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "b", 1000)
    bank.pay(4, "b", 1000)                        # b: 0, cashback 20 pending
    bank.merge_accounts(5, "a", "b")
    assert bank.get_payment_status(6, "a", "payment1") == "IN_PROGRESS"
    assert bank.deposit(4 + DAY, "a", 0 + 1) == 21
    assert bank.get_payment_status(4 + DAY + 1, "a", "payment1") == "CASHBACK_RECEIVED"
    assert bank.get_payment_status(4 + DAY + 2, "b", "payment1") is None


def test_balance_history_basic():
    bank = Bank()
    bank.create_account(10, "a")
    bank.deposit(20, "a", 5)
    bank.deposit(30, "a", 7)
    assert bank.get_balance(40, "a", 9) is None
    assert bank.get_balance(41, "a", 10) == 0
    assert bank.get_balance(42, "a", 25) == 5
    assert bank.get_balance(43, "a", 30) == 12
    assert bank.get_balance(44, "a", 44) == 12
    assert bank.get_balance(45, "nope", 1) is None


def test_balance_history_includes_cashback_at_due_time():
    bank = Bank()
    bank.create_account(1, "a")
    bank.deposit(2, "a", 100)
    bank.pay(3, "a", 100)  # cashback 2 due at 3 + DAY
    # no operations happen at the due time; query later
    assert bank.get_balance(3 + DAY + 100, "a", 3 + DAY - 1) == 0
    assert bank.get_balance(3 + DAY + 101, "a", 3 + DAY) == 2


def test_balance_history_after_transfers():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "a", 100)
    bank.transfer(4, "a", "b", 40)
    assert bank.get_balance(5, "a", 3) == 100
    assert bank.get_balance(6, "a", 4) == 60
    assert bank.get_balance(7, "b", 3) == 0
    assert bank.get_balance(8, "b", 4) == 40
