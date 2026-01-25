"""Main entry point for cache optimization benchmark."""

import json
import os
import time
import psutil
from cache import LRUCache

def measure_memory():
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def main():
    """Run cache optimization benchmark."""
    print("Starting cache optimization benchmark...")
    
    cache_size = 1000
    num_operations = 10000
    test_keys = [f"key_{i}" for i in range(2000)]
    test_values = [f"value_{i}" for i in range(2000)]
    
    cache = LRUCache(cache_size)
    
    start_time = time.time()
    peak_memory = measure_memory()
    
    hits = 0
    misses = 0
    access_times = []
    eviction_errors = 0
    
    print(f"Running {num_operations} cache operations...")
    
    for i in range(num_operations):
        if i < num_operations // 2:
            key_idx = i % 500
            key = test_keys[key_idx]
            value = test_values[key_idx]
            cache.set(key, value)
        else:
            if i % 2 == 0:
                key_idx = (i - num_operations // 2) % 500
            else:
                key_idx = 500 + (i - num_operations // 2) % 500
            
            key = test_keys[key_idx]
            
            access_start = time.time()
            result = cache.get(key)
            access_time = (time.time() - access_start) * 1000
            access_times.append(access_time)
            
            if result is not None:
                hits += 1
            else:
                misses += 1
    
    total_time = time.time() - start_time
    current_memory = measure_memory()
    peak_memory = max(peak_memory, current_memory)
    
    hit_rate = hits / (hits + misses) if (hits + misses) > 0 else 0.0
    avg_access_time = sum(access_times) / len(access_times) if access_times else float('inf')
    
    eviction_correct = True
    test_cache = LRUCache(cache_size)
    for i in range(cache_size + 100):
        key = test_keys[i % len(test_keys)]
        value = test_values[i % len(test_values)]
        test_cache.set(key, value)
    
    for i in range(100, cache_size + 100):
        key = test_keys[i % len(test_keys)]
        if test_cache.get(key) is None:
            eviction_correct = False
            eviction_errors += 1
            break
    
    metrics = {
        "hit_rate": float(hit_rate),
        "peak_memory_mb": float(peak_memory),
        "avg_access_time_ms": float(avg_access_time),
        "eviction_correct": bool(eviction_correct),
        "total_operations": int(num_operations),
        "hits": int(hits),
        "misses": int(misses),
        "eviction_errors": int(eviction_errors)
    }
    
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\nResults:")
    print(f"  hit_rate: {hit_rate:.4f}")
    print(f"  peak_memory_mb: {peak_memory:.2f}")
    print(f"  avg_access_time_ms: {avg_access_time:.2f}")
    print(f"  eviction_correct: {eviction_correct}")
    
    success = (
        hit_rate >= 0.80 and
        peak_memory <= 128 and
        avg_access_time <= 5 and
        eviction_correct == True
    )
    
    if success:
        print("\n✅ All requirements met!")
    else:
        print("\n❌ Requirements NOT met:")
        if hit_rate < 0.80:
            print(f"   - hit_rate {hit_rate:.4f} < 0.80")
        if peak_memory > 128:
            print(f"   - peak_memory_mb {peak_memory:.2f} > 128")
        if avg_access_time > 5:
            print(f"   - avg_access_time_ms {avg_access_time:.2f} > 5")
        if not eviction_correct:
            print(f"   - eviction_correct is False")

if __name__ == "__main__":
    main()

