from solution import ExperimentTracker


def test_example():
    t = ExperimentTracker()
    t.create_experiment(0, "e1")
    t.log_metric(10, "e1", "loss", 9)
    t.log_metric(20, "e1", "loss", 5)
    assert t.get_value_at(25, "e1", "loss", 15) == 9
    assert t.get_value_at(26, "e1", "loss", 5) is None
    assert t.delete_experiment(27, "e1") is True
    assert t.get_latest(28, "e1", "loss") is None


def test_value_at_exact_boundaries():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.log_metric(10, "a", "m", 1)
    t.log_metric(20, "a", "m", 2)
    assert t.get_value_at(30, "a", "m", 10) == 1
    assert t.get_value_at(31, "a", "m", 19) == 1
    assert t.get_value_at(32, "a", "m", 20) == 2
    assert t.get_value_at(33, "a", "m", 1000) == 2


def test_value_at_missing():
    t = ExperimentTracker()
    assert t.get_value_at(1, "ghost", "m", 1) is None
    t.create_experiment(2, "a")
    assert t.get_value_at(3, "a", "m", 3) is None


def test_fork_keeps_original_timestamps():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.log_metric(5, "a", "m", 1)
    t.fork(10, "a", "b")
    t.log_metric(15, "b", "m", 2)
    assert t.get_value_at(20, "b", "m", 7) == 1
    assert t.get_value_at(21, "b", "m", 14) == 1
    assert t.get_value_at(22, "b", "m", 15) == 2
    assert t.get_value_at(23, "a", "m", 15) == 1


def test_delete_and_reuse_id():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.log_metric(1, "a", "m", 1)
    t.add_tag(2, "a", "x")
    assert t.delete_experiment(3, "a") is True
    assert t.delete_experiment(4, "a") is False
    assert t.find_by_tags(5, ["x"]) == []
    assert t.best_experiments(6, "m", 5) == []
    assert t.create_experiment(7, "a") is True
    assert t.log_metric(8, "a", "m", 4) == 1
    assert t.get_value_at(9, "a", "m", 1) is None


def test_delete_source_does_not_affect_fork():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.log_metric(1, "a", "m", 7)
    t.fork(2, "a", "b")
    t.delete_experiment(3, "a")
    assert t.get_latest(4, "b", "m") == 7
    assert t.fork(5, "b", "a") is True
