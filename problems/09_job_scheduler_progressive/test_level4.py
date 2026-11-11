from solution import JobScheduler


def test_example():
    s = JobScheduler()
    s.add_job("a", 2); s.add_job("b", 3)
    s.add_dependency("b", "a")
    assert s.set_failures("a", 2) is True
    assert s.get_start_times(1) == {"a": 4, "b": 6}
    assert s.total_time(1) == 9


def test_set_failures_missing_job():
    assert JobScheduler().set_failures("ghost", 1) is False


def test_failures_reset_each_simulation():
    s = JobScheduler()
    s.add_job("a", 5)
    s.set_failures("a", 1)
    assert s.total_time(1) == 10
    assert s.total_time(1) == 10


def test_set_failures_replaces():
    s = JobScheduler()
    s.add_job("a", 5)
    s.set_failures("a", 3)
    s.set_failures("a", 0)
    assert s.total_time(1) == 5


def test_failed_job_competes_with_ready_jobs():
    s = JobScheduler()
    s.add_job("a", 2); s.add_job("b", 2)
    s.set_failures("b", 1)
    # 1 worker: a 0..2, b fails 2..4, b retries 4..6
    assert s.get_start_times(1) == {"a": 0, "b": 4}
    s2 = JobScheduler()
    s2.add_job("a", 2); s2.add_job("b", 2)
    s2.set_failures("a", 1)
    # a fails 0..2; at t=2 ready {a, b} -> a again; b at 4
    assert s2.get_start_times(1) == {"a": 2, "b": 4}


def test_failure_does_not_unblock_dependents():
    s = JobScheduler()
    s.add_job("a", 3); s.add_job("b", 1); s.add_job("c", 10)
    s.add_dependency("b", "a")
    s.set_failures("a", 1)
    # 2 workers: a 0..3 fails, c 0..10; a 3..6 ok; b 6..7
    assert s.get_start_times(2) == {"a": 3, "c": 0, "b": 6}
    assert s.total_time(2) == 10


def test_retry_frees_worker_for_others():
    s = JobScheduler()
    s.add_job("a", 4); s.add_job("b", 1); s.add_job("c", 1)
    s.set_failures("a", 1)
    # 2 workers: t0 a,b; t1 b done -> c 1..2; t4 a fails -> a 4..8
    assert s.get_start_times(2) == {"a": 4, "b": 0, "c": 1}
    assert s.total_time(2) == 8


def test_order_unaffected():
    s = JobScheduler()
    s.add_job("b", 1); s.add_job("a", 1)
    s.set_failures("a", 5)
    assert s.get_order() == ["a", "b"]
