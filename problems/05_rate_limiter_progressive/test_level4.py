from solution import RateLimiter


def test_example():
    rl = RateLimiter()
    rl.set_global_limit(3, 1000)
    assert rl.allow(0, "a") is True
    assert rl.allow(1, "b") is True
    assert rl.allow(2, "c") is True
    assert rl.allow(3, "a") is False
    assert rl.allow(1000, "a") is True
    assert rl.top_blocked(5) == ["a(1)"]


def test_client_denial_does_not_consume_global():
    rl = RateLimiter()
    rl.set_limit("a", 1, 1000)
    rl.set_global_limit(2, 1000)
    assert rl.allow(0, "a") is True
    assert rl.allow(1, "a") is False
    assert rl.allow(2, "b") is True
    assert rl.allow(3, "c") is False


def test_global_denial_does_not_consume_client():
    rl = RateLimiter()
    rl.set_limit("a", 1, 1000, "sliding")
    rl.set_global_limit(1, 1000)
    assert rl.allow(0, "b") is True
    assert rl.allow(1, "a") is False
    assert rl.get_usage(1, "a") == 0
    assert rl.allow(1000, "a") is True
    assert rl.get_usage(1000, "a") == 1


def test_global_counts_requests_before_it_was_set():
    rl = RateLimiter()
    rl.allow(0, "a")
    rl.allow(1, "b")
    rl.set_global_limit(2, 1000)
    assert rl.allow(2, "c") is False
    assert rl.allow(1000, "c") is True


def test_global_replaced():
    rl = RateLimiter()
    rl.set_global_limit(1, 1000)
    assert rl.allow(0, "a") is True
    assert rl.allow(1, "a") is False
    rl.set_global_limit(3, 1000)
    assert rl.allow(2, "a") is True
    assert rl.allow(3, "b") is True
    assert rl.allow(4, "c") is False


def test_both_limits_and_top_blocked():
    rl = RateLimiter()
    rl.set_limit("a", 2, 1000)
    rl.set_global_limit(3, 1000)
    results = [rl.allow(t, c) for t, c in [(0, "a"), (1, "a"), (2, "a"), (3, "b"), (4, "b"), (5, "c")]]
    assert results == [True, True, False, True, False, False]
    assert rl.top_blocked(5) == ["a(1)", "b(1)", "c(1)"]
    assert rl.get_usage(6, "a") == 2


def test_global_sliding_boundary():
    rl = RateLimiter()
    rl.set_global_limit(2, 100)
    assert rl.allow(0, "a") and rl.allow(50, "b")
    assert rl.allow(99, "c") is False
    assert rl.allow(100, "c") is True
    assert rl.allow(149, "d") is False
    assert rl.allow(150, "d") is True
