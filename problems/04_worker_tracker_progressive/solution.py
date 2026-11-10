"""Worker time tracker — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/04_worker_tracker_progressive/test_level1.py
"""


class WorkerTracker:
    def __init__(self) -> None:
        self.workers = {}
        self.promotions = {}
        self.double = []

    def process_promotions(self, worker_id, timestamp):
        if worker_id in self.promotions and timestamp >= self.promotions[worker_id][2] and worker_id in self.workers:
            _, _, log = self.workers[worker_id]
            newpos, newcomp, _ = self.promotions[worker_id]
            self.workers[worker_id] =  newpos, newcomp, log
            self.promotions.pop(worker_id)


    # ---- Level 1 ----
    def add_worker(self, worker_id: str, position: str, compensation: int) -> bool:
        if worker_id in self.workers: return False
        self.workers[worker_id] = [position, compensation, []]
        return True

    def register(self, worker_id: str, timestamp: int) -> str:
        self.process_promotions(worker_id, timestamp)
        if worker_id not in self.workers: return "invalid_request"
        pos, comp, log = self.workers[worker_id]
        log.append((timestamp, pos, comp))
        return "registered"

    def get(self, worker_id: str) -> int | None:
        if worker_id not in self.workers: return None
        _, _, log = self.workers[worker_id]

        time = 0

        for i in range(0, len(log), 2):
            if i+1 >= len(log): return time
            time += (log[i+1][0] - log[i][0])


        return time

    def get_pos(self, worker_id, position):
        if worker_id not in self.workers: return None
        _, _, log = self.workers[worker_id]

        time = 0

        for i in range(0, len(log), 2):
            if i+1 >= len(log): return time
            if log[i][1] == position:
                time += (log[i+1][0] - log[i][0])

        return time




    # ---- Level 2 ----
    def top_n_workers(self, n: int, position: str) -> list[str]:
        work_time = []
        for id, items in self.workers.items():
            pos, _, _ = items
            if pos == position:
                time = self.get_pos(id, position)
                work_time.append((id,time))

        work_time.sort(key=lambda kv: (-kv[1], kv[0]))
        res = []
        for worker in work_time:
            if len(res) == n: break
            id, time = worker
            res.append(f"{id}({time})")
        return res

    # ---- Level 3 ----
    def promote(
        self,
        worker_id: str,
        new_position: str,
        new_compensation: int,
        start_timestamp: int,
    ) -> str:

        if worker_id not in self.workers: return "invalid_request"
        if worker_id in self.promotions: return "invalid_request"

        self.promotions[worker_id] = (new_position, new_compensation, start_timestamp)
        return "success"

    def calc_salary(self, worker_id: str, start: int, end: int) -> int | None:
        if worker_id not in self.workers: return None
        _, _, log = self.workers[worker_id]

        comp = 0

        for i in range(0, len(log), 2):
            if i+1 >= len(log): return comp

            b = min(end,log[i+1][0])
            a = max(start, log[i][0])
            comp += max(0, (b - a)*log[i][2])
            for s,e in self.double:
                overlap = max(0, min(b,e) - max(a,s))
                comp += overlap*log[i][2]


        return comp

    # ---- Level 4 ----
    def set_double_paid(self, start: int, end: int) -> None:
        self.double.append([start,end])
        self.merge_intervals()

    def merge_intervals(self):
        self.double.sort()
        merged = []
        for s, e in self.double:
            if merged and s<= merged[-1][1]:
                merged[-1][1] = max(e, merged[-1][1])
            else:
                merged.append([s,e])
        self.double = merged
