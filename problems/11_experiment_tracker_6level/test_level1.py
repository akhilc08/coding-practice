from solution import ExperimentTracker


def test_example():
    t = ExperimentTracker()
    assert t.create_experiment(1, "e1") is True
    assert t.log_metric(2, "e1", "loss", 90) == 1
    assert t.log_metric(3, "e1", "loss", 70) == 2
    assert t.log_metric(4, "e1", "acc", 50) == 1
    assert t.get_latest(5, "e1", "loss") == 70
    assert t.get_latest(6, "e1", "f1") is None


def test_duplicate_create():
    t = ExperimentTracker()
    assert t.create_experiment(1, "e1") is True
    assert t.create_experiment(2, "e1") is False


def test_missing_experiment():
    t = ExperimentTracker()
    assert t.log_metric(1, "ghost", "loss", 1) is None
    assert t.get_latest(2, "ghost", "loss") is None


def test_experiments_independent():
    t = ExperimentTracker()
    t.create_experiment(1, "a")
    t.create_experiment(2, "b")
    t.log_metric(3, "a", "loss", 5)
    assert t.get_latest(4, "b", "loss") is None
    assert t.log_metric(5, "b", "loss", 7) == 1


def test_zero_and_negative_values():
    t = ExperimentTracker()
    t.create_experiment(1, "a")
    t.log_metric(2, "a", "delta", 0)
    assert t.get_latest(3, "a", "delta") == 0
    t.log_metric(4, "a", "delta", -3)
    assert t.get_latest(5, "a", "delta") == -3
