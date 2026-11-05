from solution import WorkerTracker


def test_example():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    t.add_worker("b", "dev", 1)
    t.add_worker("c", "pm", 1)
    t.register("a", 0)
    t.register("a", 10)
    t.register("b", 0)
    t.register("b", 30)
    assert t.top_n_workers(5, "dev") == ["b(30)", "a(10)"]
    assert t.top_n_workers(5, "pm") == ["c(0)"]
    assert t.top_n_workers(5, "ceo") == []


def test_ties_by_id():
    t = WorkerTracker()
    for w in ["zed", "amy", "kim"]:
        t.add_worker(w, "dev", 1)
    assert t.top_n_workers(3, "dev") == ["amy(0)", "kim(0)", "zed(0)"]


def test_limit_n():
    t = WorkerTracker()
    for i, w in enumerate(["a", "b", "c"]):
        t.add_worker(w, "dev", 1)
        t.register(w, 0)
        t.register(w, (i + 1) * 10)
    assert t.top_n_workers(2, "dev") == ["c(30)", "b(20)"]
    assert t.top_n_workers(0, "dev") == []


def test_in_progress_not_counted_in_ranking():
    t = WorkerTracker()
    t.add_worker("a", "dev", 1)
    t.add_worker("b", "dev", 1)
    t.register("a", 0)
    t.register("a", 5)
    t.register("b", 0)  # still inside
    assert t.top_n_workers(2, "dev") == ["a(5)", "b(0)"]
