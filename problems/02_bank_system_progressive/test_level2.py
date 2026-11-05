from solution import Bank


def test_example():
    bank = Bank()
    bank.create_account(1, "c")
    bank.create_account(2, "a")
    bank.create_account(3, "b")
    bank.deposit(4, "a", 1000)
    bank.deposit(5, "b", 1000)
    bank.transfer(6, "a", "c", 300)
    bank.transfer(7, "b", "c", 300)
    bank.transfer(8, "a", "b", 100)
    assert bank.top_spenders(9, 2) == ["a(400)", "b(300)"]
    assert bank.top_spenders(10, 5) == ["a(400)", "b(300)", "c(0)"]


def test_empty_bank():
    assert Bank().top_spenders(1, 3) == []


def test_ties_broken_by_id():
    bank = Bank()
    for i, acc in enumerate(["z", "m", "a"]):
        bank.create_account(i + 1, acc)
    assert bank.top_spenders(10, 3) == ["a(0)", "m(0)", "z(0)"]


def test_failed_transfers_dont_count():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "a", 10)
    bank.transfer(4, "a", "b", 100)   # fails
    bank.transfer(5, "a", "a", 5)     # fails
    assert bank.top_spenders(6, 2) == ["a(0)", "b(0)"]


def test_incoming_money_is_not_spending():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "a", 100)
    bank.transfer(4, "a", "b", 60)
    bank.deposit(5, "b", 1000)
    assert bank.top_spenders(6, 2) == ["a(60)", "b(0)"]


def test_n_smaller_than_accounts():
    bank = Bank()
    bank.create_account(1, "a")
    bank.create_account(2, "b")
    bank.deposit(3, "b", 10)
    bank.transfer(4, "b", "a", 10)
    assert bank.top_spenders(5, 1) == ["b(10)"]
