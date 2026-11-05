from solution import WorkerTracker


def test_example():
    t = WorkerTracker()
    assert t.add_worker("ann", "junior", 10) is True
    assert t.add_worker("ann", "senior", 99) is False
    assert t.register("ann", 100) == "registered"
    assert t.register("ann", 150) == "registered"
    assert t.register("ann", 200) == "registered"
    assert t.get("ann") == 50
    assert t.register("ann", 230) == "registered"
    assert t.get("ann") == 80
    assert t.register("bob", 1) == "invalid_request"


def test_get_missing_worker():
    assert WorkerTracker().get("nobody") is None


def test_new_worker_has_zero_time():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    assert t.get("a") == 0


def test_in_progress_session_not_counted():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    t.register("a", 5)
    assert t.get("a") == 0


def test_workers_tracked_independently():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    t.add_worker("b", "dev", 1)
    t.register("a", 0)
    t.register("b", 10)
    t.register("a", 20)
    t.register("b", 15)
    assert t.get("a") == 20
    assert t.get("b") == 5


def test_many_sessions():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    ts = 0
    for _ in range(10):
        t.register("a", ts)
        t.register("a", ts + 3)
        ts += 10
    assert t.get("a") == 30
