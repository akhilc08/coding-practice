from solution import Bank


def test_example():
    bank = Bank()
    assert bank.create_account(1, "a") is True
    assert bank.create_account(2, "a") is False
    assert bank.create_account(3, "b") is True
    assert bank.deposit(4, "a", 500) == 500
    assert bank.transfer(5, "a", "b", 200) == 300
    assert bank.transfer(6, "a", "b", 1000) is None
    assert bank.deposit(7, "b", 1) == 201


def test_deposit_missing_account():
    bank = Bank()
    assert bank.deposit(1, "x", 10) is None


def test_deposits_accumulate():
    bank = Bank()
    bank.create_account(1, "a")
    assert bank.deposit(2, "a", 10) == 10
    assert bank.deposit(3, "a", 15) == 25


def test_transfer_missing_accounts():
    bank = Bank()
    bank.create_account(1, "a")
    bank.deposit(2, "a", 100)
    assert bank.transfer(3, "a", "nope", 10) is None
    assert bank.transfer(4, "nope", "a", 10) is None
    assert bank.deposit(5, "a", 0 + 1) == 101  # unchanged by failed transfers


def test_transfer_to_self_fails():
    bank = Bank()
    bank.create_account(1, "a")
    bank.deposit(2, "a", 100)
    assert bank.transfer(3, "a", "a", 10) is None
    assert bank.deposit(4, "a", 1) == 101


def test_transfer_exact_balance():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "a", 100)
    assert bank.transfer(4, "a", "b", 100) == 0
    assert bank.deposit(5, "b", 1) == 101


def test_insufficient_funds_changes_nothing():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "a", 50)
    assert bank.transfer(4, "a", "b", 51) is None
    assert bank.deposit(5, "a", 1) == 51
    assert bank.deposit(6, "b", 1) == 1
