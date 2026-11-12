from solution import ExperimentTracker


def test_example():
    t = ExperimentTracker()
    t.create_experiment(0, "e1")
    t.log_metric(1, "e1", "loss", 50)
    assert t.fork(2, "e1", "e1b") is True
    assert t.log_metric(3, "e1b", "loss", 40) == 2
    assert t.get_latest(4, "e1", "loss") == 50
    assert t.get_latest(5, "e1b", "loss") == 40


def test_fork_rejections():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.create_experiment(1, "b")
    assert t.fork(2, "ghost", "c") is False
    assert t.fork(3, "a", "b") is False
    assert t.fork(4, "a", "a") is False


def test_fork_copies_tags_independently():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.add_tag(1, "a", "x")
    t.fork(2, "a", "b")
    assert t.find_by_tags(3, ["x"]) == ["a", "b"]
    t.add_tag(4, "b", "y")
    t.add_tag(5, "a", "z")
    assert t.find_by_tags(6, ["y"]) == ["b"]
    assert t.find_by_tags(7, ["z"]) == ["a"]


def test_original_changes_dont_leak_into_fork():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.log_metric(1, "a", "loss", 10)
    t.fork(2, "a", "b")
    t.log_metric(3, "a", "loss", 1)
    t.log_metric(4, "a", "acc", 99)
    assert t.get_latest(5, "b", "loss") == 10
    assert t.get_latest(6, "b", "acc") is None
    assert t.best_experiments(7, "loss", 5, "min") == ["a(1)", "b(10)"]


def test_fork_of_fork_and_duplicate_create():
    t = ExperimentTracker()
    t.create_experiment(0, "a")
    t.log_metric(1, "a", "loss", 3)
    t.fork(2, "a", "b")
    t.fork(3, "b", "c")
    assert t.log_metric(4, "c", "loss", 2) == 2
    assert t.create_experiment(5, "c") is False
