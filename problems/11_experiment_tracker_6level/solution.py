"""Experiment tracker — 6-level timed mock (90 min).

Read README.md, then level1.md. Only open the next level once the current
level's tests pass:  pytest problems/11_experiment_tracker_6level/test_level1.py
"""

from __future__ import annotations
from collections import defaultdict
from time import time
from copy import deepcopy

class ExperimentTracker:
    def __init__(self) -> None:
        self.exps = defaultdict(dict)
        self.tags = defaultdict(list)
        self.history = defaultdict(list)
        self.archive = set()

    # ---- Level 1 ----
    def record_history(self, timestamp, exp_id):

        self.history[exp_id].append([timestamp, deepcopy(self.exps[exp_id]), deepcopy(self.tags[exp_id])])

    def create_experiment(self, timestamp: int, exp_id: str) -> bool:
        if exp_id in self.exps: return False
        self.exps[exp_id] = {}
        self.record_history(timestamp, exp_id)
        return True

    def log_metric(self, timestamp: int, exp_id: str, metric: str, value: int) -> int | None:
        if exp_id not in self.exps or exp_id in self.archive: return None
        if metric not in self.exps[exp_id]: self.exps[exp_id][metric] = []
        self.exps[exp_id][metric].append(value)
        self.record_history(timestamp, exp_id)
        return len(self.exps[exp_id][metric])

    def get_latest(self, timestamp: int, exp_id: str, metric: str) -> int | None:
        if exp_id not in self.exps or metric not in self.exps[exp_id]: return None
        return self.exps[exp_id][metric][-1]

    # ---- Level 2 ----
    def best_experiments(self, timestamp: int, metric: str, n: int, mode: str = "max") -> list[str]:

        res = []
        for exp, metrics in self.exps.items():
            if exp in self.archive: continue
            for met, data in metrics.items():
                if met == metric:
                    if mode == "min":
                        res.append((exp, min(data)))
                    if mode == "max":
                        res.append((exp, max(data)))

        if mode == "min":
            res.sort(key=lambda tup: (tup[1], tup[0]))
        if mode == "max":
            res.sort(key=lambda tup: (-tup[1], tup[0]))

        ret = []
        for t1, t2 in res:
            if len(ret) == n: break
            ret.append(f"{t1}({t2})")

        return ret



    # ---- Level 3 ----
    def add_tag(self, timestamp: int, exp_id: str, tag: str) -> bool:
        if exp_id not in self.exps or tag in self.tags[exp_id] or exp_id in self.archive: return False
        self.tags[exp_id].append(tag)
        self.record_history(timestamp, exp_id)
        return True

    def find_by_tags(self, timestamp: int, tags: list[str]) -> list[str]:

        return sorted(exp for exp in (exp for exp in self.exps if exp not in self.archive) if all(tag in self.tags[exp] for tag in tags))

    # ---- Level 4 ----
    def fork(self, timestamp: int, src_id: str, new_id: str) -> bool:
        if src_id not in self.exps or new_id in self.exps: return False
        self.create_experiment(timestamp, new_id)

        for metric, values in self.exps[src_id].items():
            for value in values:
                self.log_metric(timestamp, new_id, metric, value)

        for tag in self.tags[src_id]:
            self.add_tag(timestamp, new_id, tag)

        self.history[new_id] = deepcopy(self.history[src_id])
        self.record_history(timestamp, new_id)
        return True


    # ---- Level 5 ----
    def get_value_at(self, timestamp: int, exp_id: str, metric: str, time_at: int) -> int | None:
        if exp_id not in self.exps: return None

        log = None

        for t, metrics, tags in self.history[exp_id]:
           if metric not in metrics or len(metrics[metric]) == 0: continue
           if t > time_at: return log
           log = metrics[metric][-1]
        return log

    def delete_experiment(self, timestamp: int, exp_id: str) -> bool:
        if exp_id not in self.exps: return False
        self.exps.pop(exp_id)
        self.tags.pop(exp_id)
        self.history.pop(exp_id)
        return True

    # ---- Level 6 ----
    def archive_inactive(self, timestamp: int, max_age: int) -> list[str]:
        rmv = []
        for exp, history in self.history.items():
            last_active = history[-1][0]
            if exp in self.archive: continue
            if last_active <= timestamp-max_age:
                self.archive.add(exp)
                rmv.append(exp)
        return sorted(rmv)


    def restore(self, timestamp: int, exp_id: str) -> bool:
        if exp_id not in self.exps or exp_id not in self.archive: return False
        self.archive.remove(exp_id)
        self.record_history(timestamp, exp_id)
        return True
