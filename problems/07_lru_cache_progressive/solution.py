"""LRU cache with TTL — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/07_lru_cache_progressive/test_level1.py
"""

from __future__ import annotations


class LRUCache:
    def __init__(self, capacity: int) -> None:
        pass

    # ---- Level 1 ----
    def get(self, timestamp: int, key: str) -> str | None:
        raise NotImplementedError

    def put(self, timestamp: int, key: str, value: str) -> str | None:
        raise NotImplementedError

    # ---- Level 2 ----
    def put_with_ttl(self, timestamp: int, key: str, value: str, ttl: int) -> str | None:
        raise NotImplementedError

    def size(self, timestamp: int) -> int:
        raise NotImplementedError

    # ---- Level 3 ----
    def get_stats(self) -> dict:
        raise NotImplementedError

    def resize(self, timestamp: int, new_capacity: int) -> list[str] | None:
        raise NotImplementedError

    # ---- Level 4 ----
    def pin(self, timestamp: int, key: str) -> bool:
        raise NotImplementedError

    def unpin(self, timestamp: int, key: str) -> bool:
        raise NotImplementedError
