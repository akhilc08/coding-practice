# Level 4 — Backup and Restore per User

**Suggested time: 30 min.** Earlier tests must keep passing.

### `backup_user(user_id) -> int | None`
Snapshot all files the user currently owns (names and sizes). This replaces
any previous backup for that user. Return the number of files backed up, or
`None` if the user doesn't exist.

### `restore_user(user_id) -> int | None`
1. Delete **all** files the user currently owns.
2. Re-add every file from the user's latest backup — **except** any file
   whose name is currently taken by another owner; skip those.

Return the number of files actually restored. If the user has never been
backed up, step 1 still happens and the result is `0`. Return `None` if the
user doesn't exist. Capacity limits are unchanged by backup/restore.

**Merging:** when user 2 is merged into user 1, user 2's backup is discarded;
user 1's backup is unchanged (it does not gain user 2's files).

## Example
```
fs.add_user("u", 100)
fs.add_file_by("u", "/a", 10)
fs.add_file_by("u", "/b", 20)
fs.backup_user("u")              # 2
fs.delete_file("/a")
fs.add_file_by("u", "/c", 5)
fs.add_file("/a", 1)             # admin now owns "/a"
fs.restore_user("u")             # 1  ("/b" restored; "/a" skipped; "/c" deleted)
fs.get_file_size("/c")           # None
fs.get_file_size("/a")           # 1  (still admin's)
```
