"""Cloud file storage — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/03_file_storage_progressive/test_level1.py
"""

from __future__ import annotations


class FileStorage:
    def __init__(self) -> None:
        pass

    # ---- Level 1 ----
    def add_file(self, name: str, size: int) -> bool:
        raise NotImplementedError

    def get_file_size(self, name: str) -> int | None:
        raise NotImplementedError

    def delete_file(self, name: str) -> int | None:
        raise NotImplementedError

    # ---- Level 2 ----
    def get_largest_n(self, prefix: str, n: int) -> list[str]:
        raise NotImplementedError

    # ---- Level 3 ----
    def add_user(self, user_id: str, capacity: int) -> bool:
        raise NotImplementedError

    def add_file_by(self, user_id: str, name: str, size: int) -> int | None:
        raise NotImplementedError

    def merge_user(self, user_id_1: str, user_id_2: str) -> int | None:
        raise NotImplementedError

    # ---- Level 4 ----
    def backup_user(self, user_id: str) -> int | None:
        raise NotImplementedError

    def restore_user(self, user_id: str) -> int | None:
        raise NotImplementedError
