"""Worker time tracker — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/04_worker_tracker_progressive/test_level1.py
"""

from __future__ import annotations


class WorkerTracker:
    def __init__(self) -> None:
        pass

    # ---- Level 1 ----
    def add_worker(self, worker_id: str, position: str, compensation: int) -> bool:
        raise NotImplementedError

    def register(self, worker_id: str, timestamp: int) -> str:
        raise NotImplementedError

    def get(self, worker_id: str) -> int | None:
        raise NotImplementedError

    # ---- Level 2 ----
    def top_n_workers(self, n: int, position: str) -> list[str]:
        raise NotImplementedError

    # ---- Level 3 ----
    def promote(
        self,
        worker_id: str,
        new_position: str,
        new_compensation: int,
        start_timestamp: int,
    ) -> str:
        raise NotImplementedError

    def calc_salary(self, worker_id: str, start: int, end: int) -> int | None:
        raise NotImplementedError

    # ---- Level 4 ----
    def set_double_paid(self, start: int, end: int) -> None:
        raise NotImplementedError
