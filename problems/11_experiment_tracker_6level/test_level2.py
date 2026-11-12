from solution import ExperimentTracker


def setup():
    t = ExperimentTracker()
    for i, e in enumerate(["e1", "e2", "e3"]):
        t.create_experiment(i, e)
    t.log_metric(3, "e1", "loss", 90)
    t.log_metric(4, "e1", "loss", 70)
    t.log_metric(5, "e2", "loss", 60)
    t.log_metric(6, "e2", "loss", 80)
    t.log_metric(7, "e3", "acc", 1)
    return t


def test_example():
    t = setup()
    assert t.best_experiments(10, "loss", 5, "min") == ["e2(60)", "e1(70)"]
    assert t.best_experiments(11, "loss", 1) == ["e1(90)"]


def test_default_mode_is_max():
    t = setup()
    assert t.best_experiments(10, "loss", 5) == ["e1(90)", "e2(80)"]


def test_unknown_metric():
    assert setup().best_experiments(10, "f1", 3) == []


def test_ties_by_id():
    t = ExperimentTracker()
    for i, e in enumerate(["c", "a", "b"]):
        t.create_experiment(i, e)
        t.log_metric(10 + i, e, "acc", 5)
    assert t.best_experiments(20, "acc", 2) == ["a(5)", "b(5)"]
    assert t.best_experiments(21, "acc", 5, "min") == ["a(5)", "b(5)", "c(5)"]


def test_zero_value_counts():
    t = ExperimentTracker()
    t.create_experiment(1, "a")
    t.log_metric(2, "a", "loss", 0)
    assert t.best_experiments(3, "loss", 1, "min") == ["a(0)"]
