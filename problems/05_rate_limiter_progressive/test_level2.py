from solution import RateLimiter


def test_example():
    rl = RateLimiter()
    rl.set_limit("a", 1, 1000)
    rl.set_limit("b", 1, 1000)
    assert [rl.allow(0, "a"), rl.allow(1, "a"), rl.allow(2, "a")] == [True, False, False]
    assert [rl.allow(3, "b"), rl.allow(4, "b")] == [True, False]
    assert rl.get_usage(5, "a") == 1
    assert rl.get_usage(1000, "a") == 0
    assert rl.top_blocked(5) == ["a(2)", "b(1)"]


def test_get_usage_no_limit_is_none():
    rl = RateLimiter()
    rl.allow(0, "a")
    assert rl.get_usage(1, "a") is None
    assert rl.get_usage(1, "ghost") is None


def test_get_usage_ignores_denied():
    rl = RateLimiter()
    rl.set_limit("a", 2, 100)
    for t in range(10):
        rl.allow(t, "a")
    assert rl.get_usage(10, "a") == 2


def test_get_usage_current_window_only():
    rl = RateLimiter()
    rl.set_limit("a", 5, 100)
    rl.allow(10, "a")
    rl.allow(20, "a")
    rl.allow(150, "a")
    assert rl.get_usage(150, "a") == 1
    assert rl.get_usage(199, "a") == 1
    assert rl.get_usage(200, "a") == 0


def test_top_blocked_tie_breaks_by_id_and_truncates():
    rl = RateLimiter()
    for c in ["c", "a", "b"]:
        rl.set_limit(c, 1, 1000)
        rl.allow(0, c)
        rl.allow(0, c)
    rl.allow(1, "b")
    assert rl.top_blocked(2) == ["b(2)", "a(1)"]
    assert rl.top_blocked(10) == ["b(2)", "a(1)", "c(1)"]


def test_top_blocked_excludes_zero_and_unlimited():
    rl = RateLimiter()
    rl.set_limit("a", 5, 1000)
    rl.allow(0, "a")
    rl.allow(1, "free")
    assert rl.top_blocked(5) == []


def test_blocked_counts_survive_set_limit():
    rl = RateLimiter()
    rl.set_limit("a", 1, 1000)
    rl.allow(0, "a")
    rl.allow(1, "a")
    rl.set_limit("a", 10, 1000)
    assert rl.top_blocked(1) == ["a(1)"]
    assert rl.get_usage(2, "a") == 0
