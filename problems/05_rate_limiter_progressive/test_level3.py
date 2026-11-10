from solution import RateLimiter


def test_example():
    rl = RateLimiter()
    rl.set_limit("a", 2, 1000, "sliding")
    assert rl.allow(0, "a") is True
    assert rl.allow(500, "a") is True
    assert rl.allow(999, "a") is False
    assert rl.allow(1000, "a") is True
    assert rl.allow(1001, "a") is False
    assert rl.get_usage(1500, "a") == 1


def test_fixed_allows_boundary_burst_sliding_does_not():
    fixed = RateLimiter()
    fixed.set_limit("a", 2, 1000)
    assert [fixed.allow(t, "a") for t in (900, 950, 1000, 1050)] == [True] * 4

    sliding = RateLimiter()
    sliding.set_limit("a", 2, 1000, "sliding")
    assert [sliding.allow(t, "a") for t in (900, 950, 1000, 1050)] == [True, True, False, False]
    assert sliding.allow(1900, "a") is True   # 900 dropped out, 950 still in
    assert sliding.allow(1949, "a") is False
    assert sliding.allow(1950, "a") is True


def test_default_mode_is_fixed():
    rl = RateLimiter()
    rl.set_limit("a", 1, 1000)
    assert rl.allow(999, "a") is True
    assert rl.allow(1000, "a") is True


def test_sliding_get_usage():
    rl = RateLimiter()
    rl.set_limit("a", 10, 100, "sliding")
    for t in (0, 10, 50, 99):
        rl.allow(t, "a")
    assert rl.get_usage(99, "a") == 4
    assert rl.get_usage(100, "a") == 3
    assert rl.get_usage(149, "a") == 2
    assert rl.get_usage(199, "a") == 0


def test_switching_mode_resets_usage():
    rl = RateLimiter()
    rl.set_limit("a", 1, 1000)
    rl.allow(0, "a")
    rl.set_limit("a", 1, 1000, "sliding")
    assert rl.allow(1, "a") is True
    assert rl.allow(2, "a") is False


def test_sliding_denied_dont_extend_window():
    rl = RateLimiter()
    rl.set_limit("a", 1, 100, "sliding")
    assert rl.allow(0, "a") is True
    for t in range(1, 100):
        assert rl.allow(t, "a") is False
    assert rl.allow(100, "a") is True
    assert rl.top_blocked(1) == ["a(99)"]


def test_mixed_modes_independent():
    rl = RateLimiter()
    rl.set_limit("f", 1, 100)
    rl.set_limit("s", 1, 100, "sliding")
    assert rl.allow(99, "f") and rl.allow(99, "s")
    assert rl.allow(100, "f") is True
    assert rl.allow(100, "s") is False
