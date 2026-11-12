"""Experiment tracker — 6-level timed mock (90 min).

Read README.md, then level1.md. Only open the next level once the current
level's tests pass:  pytest problems/11_experiment_tracker_6level/test_level1.py
"""

from __future__ import annotations


class ExperimentTracker:
    def __init__(self) -> None:
        pass

    # ---- Level 1 ----
    def create_experiment(self, timestamp: int, exp_id: str) -> bool:
        raise NotImplementedError

    def log_metric(self, timestamp: int, exp_id: str, metric: str, value: int) -> int | None:
        raise NotImplementedError

    def get_latest(self, timestamp: int, exp_id: str, metric: str) -> int | None:
        raise NotImplementedError

    # ---- Level 2 ----
    def best_experiments(self, timestamp: int, metric: str, n: int, mode: str = "max") -> list[str]:
        raise NotImplementedError

    # ---- Level 3 ----
    def add_tag(self, timestamp: int, exp_id: str, tag: str) -> bool:
        raise NotImplementedError

    def find_by_tags(self, timestamp: int, tags: list[str]) -> list[str]:
        raise NotImplementedError

    # ---- Level 4 ----
    def fork(self, timestamp: int, src_id: str, new_id: str) -> bool:
        raise NotImplementedError

    # ---- Level 5 ----
    def get_value_at(self, timestamp: int, exp_id: str, metric: str, time_at: int) -> int | None:
        raise NotImplementedError

    def delete_experiment(self, timestamp: int, exp_id: str) -> bool:
        raise NotImplementedError

    # ---- Level 6 ----
    def archive_inactive(self, timestamp: int, max_age: int) -> list[str]:
        raise NotImplementedError

    def restore(self, timestamp: int, exp_id: str) -> bool:
        raise NotImplementedError
