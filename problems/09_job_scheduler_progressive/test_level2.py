from solution import JobScheduler


def make(*jobs):
    s = JobScheduler()
    for j in jobs:
        s.add_job(j, 1)
    return s


def test_example():
    s = make("a", "b", "c", "d")
    assert s.add_dependency("c", "b") is True
    assert s.add_dependency("b", "a") is True
    assert s.add_dependency("a", "c") is False
    assert s.get_dependencies("c") == ["a", "b"]
    assert s.get_dependencies("d") == []


def test_direct_cycle_rejected():
    s = make("a", "b")
    s.add_dependency("a", "b")
    assert s.add_dependency("b", "a") is False
    assert s.get_order() == ["b", "a"]


def test_rejected_cycle_not_added():
    s = make("a", "b", "c")
    s.add_dependency("b", "a")
    s.add_dependency("c", "b")
    assert s.add_dependency("a", "c") is False
    assert s.get_dependencies("a") == []
    assert s.get_order() == ["a", "b", "c"]


def test_diamond_is_not_a_cycle():
    s = make("a", "b", "c", "d")
    assert s.add_dependency("b", "a")
    assert s.add_dependency("c", "a")
    assert s.add_dependency("d", "b")
    assert s.add_dependency("d", "c") is True
    assert s.add_dependency("d", "a") is True   # redundant but not a cycle
    assert s.get_dependencies("d") == ["a", "b", "c"]


def test_get_dependencies_missing():
    assert make("a").get_dependencies("ghost") is None


def test_long_chain_cycle():
    s = make(*"abcdef")
    for x, y in zip("bcdef", "abcde"):
        assert s.add_dependency(x, y)
    assert s.add_dependency("a", "f") is False
    assert s.get_dependencies("f") == list("abcde")
