"""API rate limiter — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/05_rate_limiter_progressive/test_level1.py
"""

from __future__ import annotations


class RateLimiter:
    def __init__(self) -> None:
        pass

    # ---- Level 1 ----
    def set_limit(
        self, client_id: str, max_requests: int, window_ms: int, mode: str = "fixed"
    ) -> None:
        raise NotImplementedError

    def allow(self, timestamp: int, client_id: str) -> bool:
        raise NotImplementedError

    # ---- Level 2 ----
    def get_usage(self, timestamp: int, client_id: str) -> int | None:
        raise NotImplementedError

    def top_blocked(self, n: int) -> list[str]:
        raise NotImplementedError

    # ---- Level 4 ----
    def set_global_limit(self, max_requests: int, window_ms: int) -> None:
        raise NotImplementedError
