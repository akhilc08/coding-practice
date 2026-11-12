"""Level 5: multi-replica load balancer. Don't open level5.md until Level 4 passes."""

from __future__ import annotations

from engine import Request
from scheduler import Scheduler


class Cluster:
    def __init__(self, num_replicas: int, max_work: int, **scheduler_kwargs) -> None:
        raise NotImplementedError

    def add(self, req: Request) -> int:
        raise NotImplementedError

    def step(self) -> list[dict[str, list[int]]]:
        raise NotImplementedError

    def replica_of(self, req_id: int) -> int | None:
        raise NotImplementedError

    def metrics(self, req_id: int) -> dict | None:
        raise NotImplementedError

    def drain(self, idx: int) -> list[int]:
        raise NotImplementedError
