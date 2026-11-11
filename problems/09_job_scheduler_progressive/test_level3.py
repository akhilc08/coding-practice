from solution import JobScheduler


def test_example():
    s = JobScheduler()
    for j, d in [("a", 3), ("b", 2), ("c", 4), ("d", 1)]:
        s.add_job(j, d)
    s.add_dependency("d", "a")
    s.add_dependency("d", "b")
    assert s.get_start_times(2) == {"a": 0, "b": 0, "c": 2, "d": 3}
    assert s.total_time(2) == 6
    assert s.total_time(1) == 10


def test_empty():
    s = JobScheduler()
    assert s.total_time(3) == 0
    assert s.get_start_times(3) == {}


def test_chain_ignores_extra_workers():
    s = JobScheduler()
    s.add_job("a", 2); s.add_job("b", 3); s.add_job("c", 4)
    s.add_dependency("b", "a")
    s.add_dependency("c", "b")
    assert s.get_start_times(10) == {"a": 0, "b": 2, "c": 5}
    assert s.total_time(10) == 9


def test_independent_jobs_many_workers():
    s = JobScheduler()
    for j, d in [("a", 5), ("b", 1), ("c", 3)]:
        s.add_job(j, d)
    assert s.total_time(3) == 5
    assert s.total_time(1) == 9
    assert s.get_start_times(1) == {"a": 0, "b": 5, "c": 6}


def test_finish_unblocks_at_same_time():
    s = JobScheduler()
    s.add_job("a", 2); s.add_job("b", 2); s.add_job("z", 10)
    s.add_dependency("b", "a")
    # 2 workers: a and z start at 0; a ends at 2 and b starts at 2
    assert s.get_start_times(2) == {"a": 0, "z": 0, "b": 2}
    assert s.total_time(2) == 10


def test_smallest_ready_id_gets_worker():
    s = JobScheduler()
    for j, d in [("x", 1), ("c", 1), ("b", 5), ("a", 1)]:
        s.add_job(j, d)
    s.add_dependency("c", "a")
    # 1 worker: t0 ready {a,b,x} -> a; t1 ready {b,c,x} -> b; t6 -> c; t7 -> x
    assert s.get_start_times(1) == {"a": 0, "b": 1, "c": 6, "x": 7}


def test_queries_do_not_change_state():
    s = JobScheduler()
    s.add_job("a", 1); s.add_job("b", 1)
    s.add_dependency("b", "a")
    assert s.total_time(1) == 2
    assert s.total_time(1) == 2
    assert s.get_order() == ["a", "b"]
