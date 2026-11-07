"""Cloud file storage — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/03_file_storage_progressive/test_level1.py
"""

from __future__ import annotations
from collections import defaultdict
from copy import deepcopy
from encodings import normalize_encoding
import copy

class FileStorage:
    def __init__(self) -> None:
        self.files = {}
        self.users = {"admin":-1}
        self.backups = defaultdict(list)


    # ---- Level 1 ----
    def add_file_helper(self, name, size, user):

        if name in self.files: return False
        if user == "admin":
            self.files[name] = [size, user]
            return True
        if user not in self.users or (size > self.users[user]): return False

        self.files[name] = [size, user]
        return True

    def add_file(self, name: str, size: int) -> bool:
        return self.add_file_helper(name, size, "admin")

    def get_file_size(self, name: str) -> int | None:
        if name not in self.files: return None
        return self.files[name][0]

    def delete_file(self, name: str) -> int | None:
        if name in self.files:
            size = self.files[name][0]
            user = self.files[name][1]
            self.users[user] += size
            self.files.pop(name)
            return size
        return None

    # ---- Level 2 ----
    def get_largest_n(self, prefix: str, n: int) -> list[str]:

        res = []
        for file, size in sorted(self.files.items(), key=lambda kv: ([-kv[1][0]], kv[0])):
            if len(res) == n: break
            if file.startswith(prefix):
                res.append(f"{file}({size[0]})")
        return res


    # ---- Level 3 ----
    def add_user(self, user_id: str, capacity: int) -> bool:
        if user_id in self.users: return False
        self.users[user_id] = capacity
        return True

    def add_file_by(self, user_id: str, name: str, size: int) -> int | None:
        if not self.add_file_helper(name, size, user_id): return None
        self.users[user_id] -= size
        return self.users[user_id]

    def merge_user(self, user_id_1: str, user_id_2: str) -> int | None:
        if user_id_1 not in self.users or user_id_2 not in self.users or user_id_1 == user_id_2: return None
        for items in self.files.values():
            if items[1] == user_id_2:
                items[1] = user_id_1
        self.users[user_id_1] += self.users[user_id_2]
        self.users.pop(user_id_2)
        self.backups.pop(user_id_2)
        return self.users[user_id_1]



    # ---- Level 4 ----
    def backup_user(self, user_id: str) -> int | None:
        if user_id not in self.users: return None
        if user_id in self.backups: self.backups.pop(user_id)
        for file, items in self.files.items():
            if items[1] == user_id:
                self.backups[user_id].append((file,items))

        return len(self.backups[user_id])

    def restore_user(self, user_id: str) -> int | None:
        if user_id not in self.users: return None

        files = list(self.files.keys())
        for file in files:
            if self.files[file][1] == user_id:
                self.users[user_id] += self.files[file][0]
                self.files.pop(file)


        restored = 0
        for file, items in self.backups[user_id]:
            if file not in self.files:
                self.files[file] = list(items)
                self.users[user_id] -= items[0]
                restored += 1
        return restored
