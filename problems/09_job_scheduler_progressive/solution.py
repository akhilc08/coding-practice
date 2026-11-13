"""Job scheduler with dependencies — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/09_job_scheduler_progressive/test_level1.py
"""

from __future__ import annotations
from collections import defaultdict

from this import d


class JobScheduler:
    def __init__(self) -> None:

        self.jobs = {}
        self.deps = defaultdict(list)



    # ---- Level 1 ----
    def add_job(self, job_id: str, duration: int) -> bool:
        if job_id in self.jobs: return False
        self.jobs[job_id] = duration
        self.deps[job_id] = []
        return True

    def add_dependency(self, job_id: str, depends_on: str) -> bool:
        if job_id not in self.jobs or depends_on not in self.jobs or job_id == depends_on or depends_on in self.deps[job_id]:
            return False

        self.deps[job_id].append(depends_on)
        return True


    def get_order(self) -> list[str]:


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
