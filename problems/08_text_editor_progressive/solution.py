"""Text editor with undo/redo — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/08_text_editor_progressive/test_level1.py
"""

from __future__ import annotations


class TextEditor:
    def __init__(self) -> None:
        pass

    # ---- Level 1 ----
    def type(self, text: str) -> None:
        raise NotImplementedError

    def move_cursor(self, pos: int) -> None:
        raise NotImplementedError

    def delete(self, n: int) -> str:
        raise NotImplementedError

    def get_text(self) -> str:
        raise NotImplementedError

    def get_cursor(self) -> int:
        raise NotImplementedError

    # ---- Level 2 ----
    def select(self, start: int, end: int) -> None:
        raise NotImplementedError

    def copy(self) -> None:
        raise NotImplementedError

    def cut(self) -> None:
        raise NotImplementedError

    def paste(self) -> None:
        raise NotImplementedError

    # ---- Level 3 ----
    def undo(self) -> bool:
        raise NotImplementedError

    def redo(self) -> bool:
        raise NotImplementedError

    # ---- Level 4 ----
    def find(self, pattern: str) -> list[int]:
        raise NotImplementedError

    def replace_all(self, pattern: str, replacement: str) -> int:
        raise NotImplementedError
