from solution import ExperimentTracker


def test_example():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.create_experiment(5, "b")
    t.log_metric(8, "a", "loss", 3)
    assert t.archive_inactive(15, 10) == ["b"]
    assert t.log_metric(16, "b", "loss", 1) is None
    assert t.best_experiments(17, "loss", 5, "min") == ["a(3)"]
    assert t.restore(18, "b") is True
    assert t.archive_inactive(27, 10) == ["a"]


def test_boundary_is_inclusive():
    t = ExperimentTracker()
    t.create_experiment(10, "a")
    assert t.archive_inactive(19, 10) == []
    assert t.archive_inactive(20, 10) == ["a"]
    assert t.archive_inactive(100, 10) == []   # already archived


def test_archived_still_exists_and_readable():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.log_metric(1, "a", "m", 5)
    t.archive_inactive(100, 10)
    assert t.create_experiment(101, "a") is False
    assert t.get_latest(102, "a", "m") == 5
    assert t.get_value_at(103, "a", "m", 1) == 5
    assert t.add_tag(104, "a", "x") is False


def test_archived_hidden_from_queries():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.add_tag(1, "a", "x")
    t.log_metric(2, "a", "m", 1)
    t.create_experiment(50, "b")
    t.add_tag(51, "b", "x")
    t.archive_inactive(55, 10)
    assert t.find_by_tags(56, ["x"]) == ["b"]
    assert t.find_by_tags(57, []) == ["b"]
    assert t.best_experiments(58, "m", 5) == []


def test_activity_types():
    t = ExperimentTracker()
    t.create_experiment(0, "logged")
    t.create_experiment(1, "tagged")
    t.create_experiment(2, "idle")
    t.log_metric(20, "logged", "m", 1)
    t.add_tag(21, "tagged", "x")
    assert t.archive_inactive(25, 10) == ["idle"]


def test_fork_from_archived_and_fork_activity():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.log_metric(1, "a", "m", 3)
    t.archive_inactive(50, 10)
    assert t.fork(60, "a", "b") is True
    assert t.log_metric(61, "b", "m", 2) == 2
    assert t.find_by_tags(62, []) == ["b"]
    t.create_experiment(63, "c")
    # b's last activity is 61 (its copied log at 1 doesn't count); c is 63
    assert t.archive_inactive(71, 10) == ["b"]


def test_fork_creation_counts_as_activity():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.fork(30, "a", "b")
    assert t.archive_inactive(35, 10) == ["a"]


def test_restore_rules_and_delete_archived():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    assert t.restore(1, "a") is False
    assert t.restore(2, "ghost") is False
    t.archive_inactive(20, 10)
    assert t.restore(21, "a") is True
    assert t.restore(22, "a") is False
    assert t.log_metric(23, "a", "m", 1) == 1
    t.archive_inactive(40, 10)
    assert t.delete_experiment(41, "a") is True
    assert t.create_experiment(42, "a") is True
