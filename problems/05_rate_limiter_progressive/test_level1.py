from solution import RateLimiter


def test_example():
    rl = RateLimiter()
    rl.set_limit("a", 2, 1000)
    assert rl.allow(0, "a") is True
    assert rl.allow(500, "a") is True
    assert rl.allow(999, "a") is False
    assert rl.allow(1000, "a") is True
    assert rl.allow(5000, "b") is True


def test_unlimited_client_always_allowed():
    rl = RateLimiter()
    assert all(rl.allow(t, "x") for t in range(100))


def test_clients_are_independent():
    rl = RateLimiter()
    rl.set_limit("a", 1, 1000)
    rl.set_limit("b", 1, 1000)
    assert rl.allow(0, "a") is True
    assert rl.allow(1, "b") is True
    assert rl.allow(2, "a") is False
    assert rl.allow(3, "b") is False


def test_denied_requests_dont_count():
    rl = RateLimiter()
    rl.set_limit("a", 2, 1000)
    assert rl.allow(0, "a") is True
    assert rl.allow(1, "a") is True
    for t in range(2, 50):
        assert rl.allow(t, "a") is False
    assert rl.allow(1000, "a") is True
    assert rl.allow(1001, "a") is True


def test_windows_aligned_to_multiples():
    rl = RateLimiter()
    rl.set_limit("a", 1, 1000)
    assert rl.allow(999, "a") is True
    assert rl.allow(1000, "a") is True
    assert rl.allow(1999, "a") is False
    assert rl.allow(2000, "a") is True


def test_same_timestamp_requests():
    rl = RateLimiter()
    rl.set_limit("a", 3, 100)
    assert [rl.allow(50, "a") for _ in range(5)] == [True, True, True, False, False]


def test_set_limit_resets_usage():
    rl = RateLimiter()
    rl.set_limit("a", 1, 1000)
    assert rl.allow(0, "a") is True
    assert rl.allow(1, "a") is False
    rl.set_limit("a", 1, 1000)
    assert rl.allow(2, "a") is True
    assert rl.allow(3, "a") is False


def test_set_limit_replaces_rule():
    rl = RateLimiter()
    rl.set_limit("a", 1, 1000)
    assert rl.allow(0, "a") is True
    rl.set_limit("a", 3, 1000)
    assert rl.allow(1, "a") is True
    assert rl.allow(2, "a") is True
    assert rl.allow(3, "a") is True
    assert rl.allow(4, "a") is False


def test_limit_set_after_unlimited_requests():
    rl = RateLimiter()
    for t in range(10):
        assert rl.allow(t, "a") is True
    rl.set_limit("a", 1, 1000)
    assert rl.allow(10, "a") is True
    assert rl.allow(11, "a") is False
