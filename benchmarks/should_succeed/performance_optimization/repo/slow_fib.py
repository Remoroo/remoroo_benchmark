"""Slow fibonacci implementation that needs optimization."""

import time

def fibonacci(n):
    """Calculate the nth fibonacci number.
    
    PROBLEM: This naive recursive implementation is extremely slow for large n.
    fib(35) takes several seconds to compute.
    
    GOAL: Optimize to run in under 1 second for n=35.
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def main():
    """Benchmark the fibonacci function."""
    n = 35
    print(f"Calculating fibonacci({n})...")
    
    start_time = time.time()
    result = fibonacci(n)
    execution_time = time.time() - start_time
    
    print(f"Result: {result}")
    print(f"execution_time: {execution_time:.3f}")
    
    if execution_time < 1.0:
        print("SUCCESS: Execution time is under 1 second!")
    else:
        print(f"FAILED: Execution time {execution_time:.3f}s exceeds 1 second")

if __name__ == "__main__":
    main()

