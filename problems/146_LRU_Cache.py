# Accepted. Better optimization exists, with doubly linked lists, I was too lazy to implement
from collections import deque
class LRUCache:

    def __init__(self, capacity: int):
        self.queue = deque()
        self.capacity = capacity
        self.hashmap = {}

    def get(self, key: int) -> int:
        if key in self.hashmap:
            self.queue.remove(key)
            self.queue.append(key)
            return self.hashmap[key]
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        if key in self.hashmap:
            self.hashmap[key] = value
            self.queue.remove(key)
            self.queue.append(key)
        else:
            self.queue.append(key)
            self.hashmap[key] = value
            if len(self.queue) > self.capacity:
                self.hashmap.pop(self.queue.popleft()) 

  


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)