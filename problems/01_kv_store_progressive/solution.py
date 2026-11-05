"""In-memory database — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/01_kv_store_progressive/test_level1.py
"""

from __future__ import annotations
from collections import defaultdict
import copy


class InMemoryDB:
    def __init__(self) -> None:
        #records -> listed by keys
        # each key is a hashmap, with field and value
        # nested hashmap?

        self.db = defaultdict(dict)
        self.exp = {}
        self.backups = []



    # ---- Level 1 ----
    def set(self, key: str, field: str, value: str) -> None:
        self.db[key][field] = value

    def get(self, key: str, field: str) -> str | None:

        return self.db.get(key, {}).get(field)

    def delete(self, key: str, field: str) -> bool:

        if self.db.get(key) is not None and field in self.db[key]:
            self.db[key].pop(field)
            if len(self.db[key]) == 0: self.db.pop(key)
            return True
        else: return False

    # ---- Level 2 ----
    def scan(self, key: str) -> list[str]:
        return self.scan_by_prefix(key, "")


    def scan_by_prefix(self, key: str, prefix: str) -> list[str]:
        fields = self.scan_prefix_help(key, prefix)
        return self.tup_to_str(fields)

    def scan_prefix_help(self, key, prefix):
        if self.db.get(key) is None: return []
        fields = []
        record = self.db[key]
        for field in sorted(record):
            if field.startswith(prefix):
                fields.append((field,record[field]))
        return fields

    def tup_to_str(self, lst):
        res = []
        for t1, t2 in lst:
            res.append(t1+"("+t2+")")
        return res

    # ---- Level 3 ----
    def set_at(self, key: str, field: str, value: str, timestamp: int) -> None:
        self.set(key, field, value)
        self.exp[(key, field)] = -1

    def set_at_with_ttl(
        self, key: str, field: str, value: str, timestamp: int, ttl: int
    ) -> None:
        self.set(key, field, value)
        self.exp[(key, field)] = timestamp + ttl

    def expired(self, key, field, timestamp):
        exp = self.exp.get((key, field))
        return not (exp == -1 or timestamp < exp)


    def get_at(self, key: str, field: str, timestamp: int) -> str | None:

        if not self.expired(key, field, timestamp): return self.get(key, field)
        return None

    def delete_at(self, key: str, field: str, timestamp: int) -> bool:
        if not self.expired(key, field, timestamp):
            return self.delete(key, field)
        else:
            self.delete(key, field)
            return False

    def scan_at(self, key: str, timestamp: int) -> list[str]:

        return self.scan_by_prefix_at(key, "", timestamp)

    def scan_by_prefix_at(self, key: str, prefix: str, timestamp: int) -> list[str]:
        lst = self.scan_prefix_help(key, prefix)
        res = []
        for e1,e2 in lst:
            if not self.expired(key, e1, timestamp):
                res.append((e1,e2))
        return self.tup_to_str(res)

    # ---- Level 4 ----
    def backup(self, timestamp: int) -> int:

        backup = defaultdict(dict)
        b_exp = {}
        for record, dic in self.db.items():
            for field, val in dic.items():
                if not self.expired(record, field, timestamp):
                    backup[record][field] = val
                    exp = self.exp[(record, field)]
                    if exp == -1: b_exp[(record,field)] = -1
                    else: b_exp[(record,field)] = exp - timestamp

        self.backups.append((timestamp, backup, b_exp))
        return len(backup)


    def restore(self, timestamp: int, timestamp_to_restore: int) -> None:
        for i in range(len(self.backups)):
            if i+1 == len(self.backups) or self.backups[i+1][0] > timestamp_to_restore:
                self.db = copy.deepcopy(self.backups[i][1])
                ttl = self.backups[i][2]
                self.new_exp = {}
                for record, dic in self.db.items():
                    for field in dic:
                        if ttl[(record, field)] == -1: self.new_exp[(record, field)] = -1
                        else: self.new_exp[(record, field)] = ttl[(record, field)] + timestamp

                self.exp = self.new_exp
                break
