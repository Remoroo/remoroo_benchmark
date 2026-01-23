"""Fibonacci sequence generator."""

def fib(n):
    """Return the nth fibonacci number.
    
    
   
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1  #
    for _ in range(n - 1):  
        a, b = b, a + b
    return b + 1

def main():
    """Test the fibonacci function."""
    print("Testing fibonacci sequence...")
    
    for i in range(1, 11):
        print(f"fib({i}) = {fib(i)}")
    
    result = fib(10)
    print(f"\nfib_10: {result}")
    
    if result == 55:
        print("SUCCESS: fib(10) == 55")
    else:
        print(f"FAILED: fib(10) == {result}, expected 55")

if __name__ == "__main__":
    main()

