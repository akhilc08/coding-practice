"""API rate limiter — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/05_rate_limiter_progressive/test_level1.py
"""



from asyncio.events import get_running_loop
from collections import defaultdict
from pydoc import cli
from time import time
from webbrowser import get


class RateLimiter:
    def __init__(self) -> None:
        self.clients = {}
        self.denied = defaultdict(int)
        self.global_limit = None
        self.global_log = []

    # ---- Level 1 ----
    def set_limit(
        self, client_id: str, max_requests: int, window_ms: int, mode: str = "fixed"
    ) -> None:
        self.clients[client_id] = [max_requests, window_ms, [], mode]

    def allow_global(self, timestamp):
        if not self.global_limit: return True
        max, window = self.global_limit

        start = timestamp - window + 1
        end = timestamp+1

        calls = 0
        print(self.global_log)
        print(start,end)
        for call in self.global_log:
            print(call)
            if call>= start and call<end:
                calls+=1
        print(calls, max)
        return calls < max

    def allow(self, timestamp: int, client_id: str) -> bool:
        if not self.allow_global(timestamp):
            self.denied[client_id] += 1
            return False
        if client_id not in self.clients:
            self.global_log.append(timestamp)
            return True

        max, window, log, mode = self.clients[client_id]
        if mode == "sliding":
            start = timestamp - window + 1
            end = timestamp+1

        else:
            interval = timestamp // window
            start = interval * window
            end = start + window

        calls = 0
        for call in log:
            if call>= start and call<end:
                calls+=1
        if calls < max:
            log.append(timestamp)
            self.global_log.append(timestamp)
            return True
        self.denied[client_id] += 1
        return False

    # ---- Level 2 ----
    def get_usage(self, timestamp: int, client_id: str) -> int | None:
        if client_id not in self.clients: return None
        max, window, log, mode = self.clients[client_id]

        if mode == "sliding":
            start = timestamp - window + 1
            end = timestamp+1
        else:
            interval = timestamp // window
            start = interval * window
            end = start + window

        usage = 0
        for call in log:
            if call>= start and call<end:
                usage += 1
        return usage


    def top_blocked(self, n: int) -> list[str]:

        denied = sorted(self.denied.items(), key = lambda kv: (-kv[1], kv[0]))
        res = []
        for i in range(n):
            if i == len(denied): break
            res.append(f"{denied[i][0]}({denied[i][1]})")
        return res

    # ---- Level 4 ----
    def set_global_limit(self, max_requests: int, window_ms: int) -> None:
        self.global_limit = (max_requests, window_ms)
