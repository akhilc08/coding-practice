"""Job scheduler with dependencies — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/09_job_scheduler_progressive/test_level1.py
"""

from __future__ import annotations


class JobScheduler:
    def __init__(self) -> None:
        pass

    # ---- Level 1 ----
    def add_job(self, job_id: str, duration: int) -> bool:
        raise NotImplementedError

    def add_dependency(self, job_id: str, depends_on: str) -> bool:
        raise NotImplementedError

    def get_order(self) -> list[str]:
        raise NotImplementedError

    # ---- Level 2 ----
    def get_dependencies(self, job_id: str) -> list[str] | None:
        raise NotImplementedError

    # ---- Level 3 ----
    def get_start_times(self, workers: int) -> dict[str, int]:
        raise NotImplementedError

    def total_time(self, workers: int) -> int:
        raise NotImplementedError

    # ---- Level 4 ----
    def set_failures(self, job_id: str, k: int) -> bool:
        raise NotImplementedError
