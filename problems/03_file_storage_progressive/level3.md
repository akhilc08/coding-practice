# Level 3 — Users and Capacity

**Suggested time: 25 min.** Earlier tests must keep passing.

The system now has users, each with a storage `capacity` (total bytes they may
own). Files added through the Level 1 `add_file` belong to a built-in admin
with **unlimited** capacity (no test will create a user named `"admin"`).

### `add_user(user_id, capacity) -> bool`
Create a user. Return `False` if the user already exists.

### `add_file_by(user_id, name, size) -> int | None`
Add a file owned by `user_id`. Return the user's **remaining** capacity after
adding. Return `None` (add nothing) if the user doesn't exist, the file name
already exists, or the file would exceed the user's remaining capacity.

### `merge_user(user_id_1, user_id_2) -> int | None`
Merge user 2 **into** user 1: all of user 2's files become user 1's, and
user 1's total capacity increases by user 2's total capacity. User 2 is
deleted. Return user 1's remaining capacity. Return `None` if the IDs are
equal or either user doesn't exist.

`delete_file` (Level 1) still works on any file and frees capacity for that
file's owner.

## Example
```
fs.add_user("u1", 100)                    # True
fs.add_file_by("u1", "/u1/a", 60)         # 40
fs.add_file_by("u1", "/u1/b", 50)         # None (over capacity)
fs.add_user("u2", 30)
fs.add_file_by("u2", "/u2/a", 25)         # 5
fs.merge_user("u1", "u2")                 # 130 - 85 = 45
fs.delete_file("/u2/a")                   # 25
fs.add_file_by("u1", "/u1/b", 50)         # 45 + 25 - 50 = 20
```
