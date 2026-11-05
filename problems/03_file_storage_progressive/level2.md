# Level 2 — Largest Files

**Suggested time: 15 min.** Earlier tests must keep passing.

### `get_largest_n(prefix, n) -> list[str]`
Return up to `n` files whose names start with `prefix`, formatted
`"<name>(<size>)"`, sorted by size **descending**, ties broken by name
**ascending**. Return `[]` if nothing matches.

## Example
```
fs.add_file("/dir/a.txt", 5)
fs.add_file("/dir/b.txt", 20)
fs.add_file("/dir/c.txt", 5)
fs.add_file("/other.txt", 100)
fs.get_largest_n("/dir", 2)      # ["/dir/b.txt(20)", "/dir/a.txt(5)"]
fs.get_largest_n("/dir", 10)     # ["/dir/b.txt(20)", "/dir/a.txt(5)", "/dir/c.txt(5)"]
fs.get_largest_n("/nope", 3)     # []
```
