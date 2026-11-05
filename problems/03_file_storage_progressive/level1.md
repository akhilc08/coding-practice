# Level 1 — Basic File Operations

**Suggested time: 10 min.** Only open `level2.md` after `pytest test_level1.py` passes.

You're building a simple cloud file storage service. Files are identified by
a unique `name` (a string like `"/dir/file.txt"`) and have an integer `size`.

### `add_file(name, size) -> bool`
Add a file. Return `False` if a file with that name already exists.

### `get_file_size(name) -> int | None`
Return the file's size, or `None` if it doesn't exist.

### `delete_file(name) -> int | None`
Delete the file and return its size, or `None` if it doesn't exist.

## Example
```
fs.add_file("/a.txt", 10)        # True
fs.add_file("/a.txt", 99)        # False
fs.get_file_size("/a.txt")       # 10
fs.delete_file("/a.txt")         # 10
fs.get_file_size("/a.txt")       # None
```
