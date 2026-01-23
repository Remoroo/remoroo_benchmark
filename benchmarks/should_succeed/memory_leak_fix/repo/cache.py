"""Cache implementation with memory leak."""

import time
from collections import OrderedDict

import torch

class Cache:
    """A simple cache that stores computed results.
    
    BUG: This cache grows unbounded! It never evicts old entries,
    causing memory to grow indefinitely with usage.
    
    GOAL: Implement LRU (Least Recently Used) eviction with max_size=100
    """
    
    def __init__(self, max_size=100):
        self.max_size = max_size
        self.cache = {}  # BUG: Using regular dict, not tracking access order
        self.hits = 0
        self.misses = 0
    
    def get(self, key):
        """Get a value from cache.
        
        BUG: Doesn't update access time for LRU tracking.
        """
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None
    
    def set(self, key, value):
        """Set a value in cache.
        
        BUG: Never checks max_size or evicts old entries!
        This causes unbounded memory growth.
        """
        self.cache[key] = value  # BUG: No eviction logic!
    
    def size(self):
        return len(self.cache)
    
    def stats(self):
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            "size": self.size(),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate
        }


def expensive_computation(n):
    """Simulate an expensive computation."""
    time.sleep(0.001)  # Simulate work
    return n * n + 2 * n + 1


def process_with_cache(cache, items):
    """Process items using cache."""
    results = []
    for item in items:
        # Try cache first
        result = cache.get(item)
        if result is None:
            # Cache miss - compute and store
            result = expensive_computation(item)
            cache.set(item, result)
        results.append(result)
    return results


def main():
    """Test the cache with many items."""
    cache = Cache(max_size=100)
    
    # Process 1000 different items
    num_items = 1000
    items = list(range(num_items))
    
    print(f"Processing {num_items} unique items with cache (max_size={cache.max_size})")
    
    start_time = time.time()
    results = process_with_cache(cache, items)
    elapsed = time.time() - start_time
    
    stats = cache.stats()
    print(f"\nCompleted in {elapsed:.2f} seconds")
    print(f"Cache stats: {stats}")
    
    # Check if memory is stable (cache respects max_size)
    memory_stable = cache.size() <= cache.max_size
    
    print(f"\nCache size: {cache.size()}")
    print(f"Max allowed: {cache.max_size}")
    print(f"memory_stable: {memory_stable}")
    
    if memory_stable:
        print("\nSUCCESS: Cache properly evicts old entries!")
    else:
        print(f"\nFAILED: Cache size ({cache.size()}) exceeds max_size ({cache.max_size})")
        print("Memory leak detected - cache grows unbounded!")


if __name__ == "__main__":
    main()

