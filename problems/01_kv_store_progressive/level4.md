# Level 4 — Backup and Restore

**Suggested time: 30 min.** Earlier levels' tests must keep passing.

### `backup(timestamp) -> int`
Save a snapshot of the database's current state at `timestamp` (ignoring
expired fields). Return the number of records that have at least one
non-expired field.

The snapshot must store each field's **remaining** TTL, not its absolute
expiry time.

### `restore(timestamp, timestamp_to_restore) -> None`
Replace the current state with the **latest** backup taken at or before
`timestamp_to_restore`. You may assume such a backup exists.

TTLs are recalculated relative to the restore time: a field that had
`r` time units left when the backup was taken now expires at
`timestamp + r`.

## Example
```
db.set_at_with_ttl("A", "B", "C", 1, 10)   # expires at 11
db.backup(3)                               # 1  (B has 8 left)
db.set_at("A", "D", "E", 4)
db.backup(5)                               # 1
db.delete_at("A", "B", 8)                  # True
db.backup(9)                               # 1  (only D left)
db.restore(10, 7)                          # restores backup from t=5:
                                           #   B had 6 left -> expires at 16
                                           #   D has no TTL
db.scan_at("A", 15)                        # ["B(C)", "D(E)"]
db.scan_at("A", 16)                        # ["D(E)"]
```
