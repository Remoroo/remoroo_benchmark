"""LRU Cache implementation."""

import time
from collections import OrderedDict

class LRUCache:
    """Least Recently Used cache with size limit."""
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key: str):
        """Get value from cache."""
        time.sleep(0.001)
        
        if key not in self.cache:
            return None
        
        value = self.cache.pop(key)
        self.cache[key] = value
        return value
    
    def set(self, key: str, value: str):
        """Set value in cache."""
        time.sleep(0.001)
        
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        
        self.cache[key] = value

