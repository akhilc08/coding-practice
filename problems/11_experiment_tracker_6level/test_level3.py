from solution import ExperimentTracker


def setup():
    t = ExperimentTracker()
    t.create_experiment(0, "e1")
    t.create_experiment(1, "e2")
    t.create_experiment(2, "e3")
    return t


def test_example():
    t = setup()
    t.add_tag(3, "e1", "baseline")
    t.add_tag(4, "e1", "lr=1e-3")
    t.add_tag(5, "e2", "lr=1e-3")
    assert t.find_by_tags(6, ["lr=1e-3"]) == ["e1", "e2"]
    assert t.find_by_tags(7, ["lr=1e-3", "baseline"]) == ["e1"]


def test_add_tag_rejections():
    t = setup()
    assert t.add_tag(3, "ghost", "x") is False
    assert t.add_tag(4, "e1", "x") is True
    assert t.add_tag(5, "e1", "x") is False


def test_empty_tags_matches_all():
    assert setup().find_by_tags(3, []) == ["e1", "e2", "e3"]


def test_no_match():
    t = setup()
    t.add_tag(3, "e1", "a")
    assert t.find_by_tags(4, ["a", "b"]) == []
    assert t.find_by_tags(5, ["zzz"]) == []


def test_duplicate_tags_in_query():
    t = setup()
    t.add_tag(3, "e2", "a")
    assert t.find_by_tags(4, ["a", "a"]) == ["e2"]
