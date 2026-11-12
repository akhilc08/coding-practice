"""LLM inference request scheduler. This is the file you edit.

Read README.md, then level1.md. Only open the next level once the current
level's tests pass:  pytest problems/12_llm_scheduler_progressive/test_level1.py

engine.py is system code: import from it, never modify it.
"""

from __future__ import annotations

from collections import deque

from engine import Request, decode_one, load_prefix, prefill, reset  # noqa: F401


class Scheduler:
    def __init__(
        self,
        max_work: int,
        chunked_prefill: bool = False,      # Level 2
        prefix_cache_size: int = 0,         # Level 3
        kv_capacity: int | None = None,     # Level 4
    ) -> None:
        self.max_work = max_work
        self.waiting: deque[Request] = deque()
        self.admitted: deque[Request] = deque()
        self.finished: list[Request] = []

    # ---- Level 1 ----
    def add(self, req: Request) -> bool:
        # TODO: validation (see level1.md)
        self.waiting.append(req)
        return True

    def step(self) -> dict[str, list[int]]:
        raise NotImplementedError

    # ---- Level 2 ----
    def metrics(self, req_id: int) -> dict | None:
        raise NotImplementedError

    # ---- Level 3 ----
    def cache_stats(self) -> dict[str, int]:
        raise NotImplementedError

    # ---- Level 4 ----
    def memory_used(self) -> int:
        raise NotImplementedError
