from solution import WorkerTracker


def test_example():
    t = WorkerTracker()
    t.add_worker("a", "dev", 10)
    t.register("a", 0)
    t.register("a", 100)
    assert t.promote("a", "lead", 20, 150) == "success"
    assert t.promote("a", "cto", 99, 150) == "invalid_request"
    t.register("a", 120)
    t.register("a", 140)
    t.register("a", 200)
    t.register("a", 250)
    assert t.get("a") == 170
    assert t.top_n_workers(5, "lead") == ["a(50)"]
    assert t.top_n_workers(5, "dev") == []
    assert t.calc_salary("a", 50, 225) == 1200


def test_promote_missing_worker():
    assert WorkerTracker().promote("x", "lead", 1, 0) == "invalid_request"


def test_calc_salary_missing_worker():
    assert WorkerTracker().calc_salary("x", 0, 10) is None


def test_promotion_not_effective_before_entry():
    t = WorkerTracker()
    t.add_worker("a", "dev", 10)
    t.promote("a", "lead", 20, 0)
    # no entry yet: still a dev
    assert t.top_n_workers(5, "dev") == ["a(0)"]
    assert t.top_n_workers(5, "lead") == []
    t.register("a", 5)
    assert t.top_n_workers(5, "lead") == ["a(0)"]


def test_session_in_progress_keeps_old_pay():
    t = WorkerTracker()
    t.add_worker("a", "dev", 10)
    t.register("a", 0)                 # enter as dev
    t.promote("a", "lead", 20, 5)
    t.register("a", 10)                # leave: whole session at dev pay
    assert t.calc_salary("a", 0, 10) == 100
    t.register("a", 20)                # enter: promotion applies
    t.register("a", 30)
    assert t.calc_salary("a", 0, 100) == 100 + 200


def test_can_promote_again_after_effective():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    t.promote("a", "lead", 2, 0)
    t.register("a", 1)
    t.register("a", 2)
    assert t.promote("a", "cto", 3, 0) == "success"


def test_ranking_counts_only_time_in_current_position():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    t.add_worker("b", "lead", 1)
    t.register("a", 0)
    t.register("a", 1000)              # 1000 as dev
    t.register("b", 0)
    t.register("b", 50)                # 50 as lead
    t.promote("a", "lead", 2, 0)
    t.register("a", 2000)
    t.register("a", 2010)              # 10 as lead
    assert t.top_n_workers(5, "lead") == ["b(50)", "a(10)"]
    assert t.get("a") == 1010


def test_calc_salary_partial_overlap_and_outside():
    t = WorkerTracker()
    t.add_worker("a", "dev", 3)
    t.register("a", 10)
    t.register("a", 20)
    assert t.calc_salary("a", 0, 10) == 0
    assert t.calc_salary("a", 20, 30) == 0
    assert t.calc_salary("a", 15, 100) == 15
    assert t.calc_salary("a", 12, 13) == 3


def test_calc_salary_ignores_in_progress():
    t = WorkerTracker()
    t.add_worker("a", "dev", 5)
    t.register("a", 0)
    assert t.calc_salary("a", 0, 100) == 0
