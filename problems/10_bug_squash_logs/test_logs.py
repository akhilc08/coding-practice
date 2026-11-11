from solution import LogAnalyzer


def make(*lines):
    a = LogAnalyzer()
    for line in lines:
        a.ingest(line)
    return a


def test_valid_line():
    a = LogAnalyzer()
    assert a.ingest("100 GET /api/users 200 15ms") is True
    assert a.invalid_count() == 0
    assert a.top_paths(1) == ["/api/users(1)"]


def test_extra_whitespace_is_fine():
    a = LogAnalyzer()
    assert a.ingest("100  GET   /a  200  15ms") is True
    assert a.ingest("  101 GET /a 200 15ms\n") is True
    assert a.invalid_count() == 0


def test_wrong_field_count_is_invalid():
    a = LogAnalyzer()
    assert a.ingest("100 GET /a 200") is False
    assert a.ingest("100 GET /a 200 15ms extra") is False
    assert a.ingest("") is False
    assert a.invalid_count() == 3


def test_bad_values_are_invalid_and_not_counted():
    a = LogAnalyzer()
    assert a.ingest("abc GET /a 200 15ms") is False
    assert a.ingest("100 GET /a OK 15ms") is False
    assert a.ingest("100 GET /a 500 15") is False
    assert a.ingest("100 GET /a 503 fastms") is False
    assert a.invalid_count() == 4
    assert a.count_by_status() == {}


def test_query_string_removed():
    a = make("1 GET /search?q=cats 200 1ms", "2 GET /search?q=dogs&x=1 200 1ms")
    assert a.top_paths(5) == ["/search(2)"]


def test_path_without_query_kept_whole():
    a = make("1 GET /api/users 200 1ms")
    assert a.top_paths(1) == ["/api/users(1)"]


def test_trailing_slash_and_root():
    a = make(
        "1 GET /api/users/ 200 1ms",
        "2 GET /api/users/?page=2 200 1ms",
        "3 GET / 200 1ms",
        "4 GET /?ref=home 200 1ms",
    )
    assert a.top_paths(5) == ["/(2)", "/api/users(2)"]


def test_count_by_status_returns_copy():
    a = make("1 GET /a 200 1ms", "2 GET /a 200 1ms", "3 GET /a 404 1ms")
    counts = a.count_by_status()
    assert counts == {200: 2, 404: 1}
    counts[200] = 999
    assert a.count_by_status() == {200: 2, 404: 1}


def test_error_rate_counts_only_valid():
    a = make("1 GET /a 500 1ms", "2 GET /a 200 1ms", "garbage", "3 GET /a 200 1ms", "4 GET /a 503 1ms")
    assert a.error_rate() == 0.5


def test_error_rate_empty():
    assert LogAnalyzer().error_rate() == 0.0
    assert make("junk").error_rate() == 0.0


def test_top_paths_ties_and_truncate():
    a = make("1 GET /b 200 1ms", "2 GET /a 200 1ms", "3 GET /c 200 1ms", "4 GET /c 200 1ms")
    assert a.top_paths(2) == ["/c(2)", "/a(1)"]


def test_p95_nearest_rank():
    a = make(*[f"{i} GET /a 200 {i}ms" for i in range(1, 21)])   # latencies 1..20
    assert a.p95_latency() == 19


def test_p95_small_and_empty():
    assert LogAnalyzer().p95_latency() is None
    assert make("1 GET /a 200 7ms").p95_latency() == 7
    a = make(*[f"{i} GET /a 200 {i * 10}ms" for i in range(1, 11)])  # 10..100
    assert a.p95_latency() == 100


def test_requests_in_window_half_open():
    a = make("10 GET /a 200 1ms", "20 GET /a 200 1ms", "30 GET /a 200 1ms")
    assert a.requests_in_window(10, 30) == 2
    assert a.requests_in_window(0, 10) == 0
    assert a.requests_in_window(10, 31) == 3
