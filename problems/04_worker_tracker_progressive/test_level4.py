from solution import WorkerTracker


def test_example():
    t = WorkerTracker()
    t.add_worker("a", "dev", 10)
    t.register("a", 0)
    t.register("a", 100)
    t.set_double_paid(20, 40)
    t.set_double_paid(30, 60)
    assert t.calc_salary("a", 0, 100) == 1400
    assert t.calc_salary("a", 50, 100) == 600


def test_no_double_periods_unchanged():
    t = WorkerTracker()
    t.add_worker("a", "dev", 10)
    t.register("a", 0)
    t.register("a", 10)
    assert t.calc_salary("a", 0, 10) == 100


def test_double_period_outside_sessions():
    t = WorkerTracker()
    t.add_worker("a", "dev", 10)
    t.register("a", 0)
    t.register("a", 10)
    t.set_double_paid(50, 100)
    assert t.calc_salary("a", 0, 100) == 100


def test_disjoint_periods():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    t.register("a", 0)
    t.register("a", 100)
    t.set_double_paid(10, 20)
    t.set_double_paid(50, 55)
    assert t.calc_salary("a", 0, 100) == 100 + 10 + 5


def test_nested_and_duplicate_periods_not_stacked():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    t.register("a", 0)
    t.register("a", 100)
    t.set_double_paid(10, 50)
    t.set_double_paid(20, 30)   # fully inside
    t.set_double_paid(10, 50)   # duplicate
    assert t.calc_salary("a", 0, 100) == 100 + 40


def test_adjacent_periods():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    t.register("a", 0)
    t.register("a", 100)
    t.set_double_paid(10, 20)
    t.set_double_paid(20, 30)
    assert t.calc_salary("a", 0, 100) == 100 + 20


def test_double_pay_uses_session_compensation():
    t = WorkerTracker()
    t.add_worker("a", "dev", 10)
    t.register("a", 0)
    t.register("a", 10)              # @10
    t.promote("a", "lead", 30, 0)
    t.register("a", 20)
    t.register("a", 30)              # @30
    t.set_double_paid(5, 25)
    # dev: 5 normal + 5 double = 50 + 100 ; lead: 5 double + 5 normal = 300 + 150
    assert t.calc_salary("a", 0, 100) == 150 + 450


def test_double_pay_clipped_to_query_window():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    t.register("a", 0)
    t.register("a", 100)
    t.set_double_paid(0, 100)
    assert t.calc_salary("a", 40, 60) == 40


def test_period_added_after_query_window_applies_retroactively():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    t.register("a", 0)
    t.register("a", 10)
    assert t.calc_salary("a", 0, 10) == 10
    t.set_double_paid(0, 10)
    assert t.calc_salary("a", 0, 10) == 20
