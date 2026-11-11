from solution import JobScheduler


def test_example():
    s = JobScheduler()
    s.add_job("test", 5); s.add_job("build", 3); s.add_job("lint", 1)
    assert s.add_dependency("test", "build") is True
    assert s.get_order() == ["build", "lint", "test"]


def test_add_job_duplicate():
    s = JobScheduler()
    assert s.add_job("a", 1) is True
    assert s.add_job("a", 2) is False


def test_add_dependency_rejections():
    s = JobScheduler()
    s.add_job("a", 1); s.add_job("b", 1)
    assert s.add_dependency("a", "ghost") is False
    assert s.add_dependency("ghost", "a") is False
    assert s.add_dependency("a", "a") is False
    assert s.add_dependency("a", "b") is True
    assert s.add_dependency("a", "b") is False


def test_empty_and_no_deps():
    s = JobScheduler()
    assert s.get_order() == []
    for j in ["c", "a", "b"]:
        s.add_job(j, 1)
    assert s.get_order() == ["a", "b", "c"]


def test_smallest_ready_id_not_insertion_order():
    s = JobScheduler()
    for j in ["z", "y", "a"]:
        s.add_job(j, 1)
    s.add_dependency("a", "z")
    # ready at start: y, z -> y; then z; then a
    assert s.get_order() == ["y", "z", "a"]


def test_diamond():
    s = JobScheduler()
    for j in ["top", "left", "right", "bottom"]:
        s.add_job(j, 1)
    s.add_dependency("left", "top")
    s.add_dependency("right", "top")
    s.add_dependency("bottom", "left")
    s.add_dependency("bottom", "right")
    assert s.get_order() == ["top", "left", "right", "bottom"]


def test_newly_ready_job_competes_with_waiting_ones():
    s = JobScheduler()
    for j in ["a", "b", "m", "z"]:
        s.add_job(j, 1)
    s.add_dependency("b", "a")
    # start: a, m, z ready -> a; now b, m, z ready -> b
    assert s.get_order() == ["a", "b", "m", "z"]
