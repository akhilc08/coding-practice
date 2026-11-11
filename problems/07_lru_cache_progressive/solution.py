"""LRU cache with TTL — progressive problem.

Start with level1.md. Only open the next level once the current level's tests
pass:  pytest problems/07_lru_cache_progressive/test_level1.py
"""

from __future__ import annotations
from time import time
from xxlimited import new

class Node:
    def __init__(self, key, val, exp = -1):
        self.value = val
        self.key = key
        self.exp = exp
        self.pinned = False
        self.left: None | Node = None
        self.right : None | Node = None

class LRUCache:

    def __init__(self, capacity: int) -> None:
        self.l, self.r = Node("",""), Node("","")
        self.l.right, self.r.left = self.r, self.l
        self.stats = {"hits": 0, "misses": 0, "evictions" : 0}
        self.cap = capacity
        self.nodes = {}

    def remove_expired(self, timestamp):
        curr = self.l
        while curr.right is not None:
            if curr.exp != -1 and curr.exp <= timestamp:
                self.remove(curr)
            curr = curr.right


    def remove(self, node):
        temp = node.left
        node.left.right = node.right
        node.right.left = temp
        self.nodes.pop(node.key)
        return node

    def insert(self, node, timestamp):

        second = self.l.right
        self.l.right = node
        node.left = self.l
        node.right = second
        second.left = node
        self.nodes[node.key] = node

    # ---- Level 1 ----
    def get(self, timestamp: int, key: str) -> str | None:
        self.remove_expired(timestamp)
        if key not in self.nodes:
            self.stats["misses"] += 1
            return None
        self.insert(self.remove(self.nodes[key]), timestamp)
        self.stats["hits"]+=1
        return self.nodes[key].value

    def put(self, timestamp: int, key: str, value: str) -> str | None:
        return self.put_with_ttl(timestamp, key, value, -1)


    # ---- Level 2 ----
    def put_with_ttl(self, timestamp: int, key: str, value: str, ttl: int) -> str | None:
        expcount = self.exp_count(timestamp)
        ret = None
        if len(self.nodes)-expcount > self.cap-1 and key not in self.nodes:
            ret = self.evict()
            if ret == None: return ret
        self.remove_expired(timestamp)
        if key in self.nodes:
            self.nodes[key].value = value
            self.nodes[key].exp = timestamp + ttl if ttl != -1 else -1
            self.insert(self.remove(self.nodes[key]), timestamp)
        else:
            self.insert(Node(key, value, timestamp + ttl if ttl != -1 else -1), timestamp)

        return ret

    def evict(self):

        curr = self.r.left
        while curr.left is not None:
            if not curr.pinned:
                self.stats["evictions"]+=1
                return self.remove(curr).key
            curr = curr.left
        return None

    def size(self, timestamp: int) -> int:
        curr = self.l
        res = -1
        while curr.right is not None:
            if curr.exp == -1 or curr.exp > timestamp:
                res += 1
            curr = curr.right
        return res

    # ---- Level 3 ----
    def get_stats(self) -> dict:
        return self.stats

    def exp_count(self, timestamp):
        curr = self.l
        count = 0
        while curr.right is not None:
            if curr.exp != -1 and curr.exp <= timestamp:
                count+=1
            curr = curr.right
        return count

    def resize(self, timestamp: int, new_capacity: int) -> list[str] | None:
        expcount = self.exp_count(timestamp)
        evicted = []

        while len(self.nodes)-expcount > new_capacity:
            evict = self.evict()
            if evict == None:
                return None
            evicted.append(evict)

        self.cap = new_capacity
        self.remove_expired(timestamp)
        return evicted



    # ---- Level 4 ----
    def pin(self, timestamp: int, key: str) -> bool:
        self.remove_expired(timestamp)
        if key not in self.nodes: return False
        self.nodes[key].pinned = True
        return True

    def unpin(self, timestamp: int, key: str) -> bool:
        self.remove_expired(timestamp)
        if key not in self.nodes: return False
        self.nodes[key].pinned = False
        return True
