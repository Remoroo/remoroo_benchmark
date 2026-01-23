"""Multi-threaded counter with a race condition bug."""

import threading
import time

class Counter:
    """A simple counter class.
    
    BUG: This class has a race condition when accessed from multiple threads.
    The increment operation is not atomic, causing lost updates.
    """
    
    def __init__(self):
        self.value = 0
    
    def increment(self):
        """Increment the counter by 1.
        
        BUG: This is not thread-safe!
        The read-modify-write sequence can be interleaved by other threads.
        """
        current = self.value
        # Simulate some processing time that makes the race condition more likely
        time.sleep(0.0001)
        self.value = current + 1
    
    def get_value(self):
        return self.value


def worker(counter, iterations):
    """Worker function that increments the counter."""
    for _ in range(iterations):
        counter.increment()


def main():
    """Test the counter with multiple threads."""
    counter = Counter()
    threads = []
    
    num_threads = 10
    iterations_per_thread = 1000
    expected_total = num_threads * iterations_per_thread
    
    print(f"Starting {num_threads} threads, each incrementing {iterations_per_thread} times")
    print(f"Expected final count: {expected_total}")
    
    # Create and start threads
    start_time = time.time()
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(counter, iterations_per_thread))
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    elapsed = time.time() - start_time
    final_count = counter.get_value()
    
    print(f"\nCompleted in {elapsed:.2f} seconds")
    print(f"final_count: {final_count}")
    print(f"Expected: {expected_total}")
    
    if final_count == expected_total:
        print("SUCCESS: Counter is thread-safe!")
    else:
        print(f"FAILED: Lost {expected_total - final_count} increments due to race condition")


if __name__ == "__main__":
    main()

