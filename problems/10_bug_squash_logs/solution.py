"""Log analyzer — bug squash.

Read spec.md first. This code has 9 bugs. Fix them so that
`pytest problems/10_bug_squash_logs` passes.
"""

from __future__ import annotations

import math
from collections import Counter


class LogAnalyzer:
    def __init__(self) -> None:
        self.entries = []  # (timestamp, method, path, status, latency_ms)
        self.invalid = 0
        self.total = 0
        self.status_counts = Counter()

    def _normalize(self, path: str) -> str:
        path = path[: path.find("?")]
        return path.rstrip("/")

    def ingest(self, line: str) -> bool:
        self.total += 1
        parts = line.split(" ")
        if len(parts) != 5:
            return False
        ts, method, path, status, latency = parts
        try:
            ts = int(ts)
            status = int(status)
            self.status_counts[status] += 1
            if not latency.endswith("ms"):
                raise ValueError
            latency = int(latency[:-2])
        except ValueError:
            self.invalid += 1
            return False
        self.entries.append((ts, method, self._normalize(path), status, latency))
        return True

    def invalid_count(self) -> int:
        return self.invalid

    def count_by_status(self) -> dict[int, int]:
        return self.status_counts

    def error_rate(self) -> float:
        if not self.entries:
            return 0.0
        errors = sum(1 for e in self.entries if e[3] >= 500)
        return errors / self.total

    def top_paths(self, n: int) -> list[str]:
        counts = Counter(e[2] for e in self.entries)
        ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return [f"{p}({c})" for p, c in ranked[:n]]

    def p95_latency(self) -> int | None:
        if not self.entries:
            return None
        latencies = sorted(e[4] for e in self.entries)
        return latencies[int(0.95 * len(latencies))]

    def requests_in_window(self, start: int, end: int) -> int:
        return sum(1 for e in self.entries if start <= e[0] <= end)
