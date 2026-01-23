"""Calculator module with bugs and low test coverage.

BUGS TO FIX:
1. divide() doesn't handle division by zero
2. power() has wrong implementation for negative exponents
3. factorial() doesn't handle edge cases (0, negative)
4. sqrt() doesn't handle negative numbers

COVERAGE ISSUES:
- Many branches not covered by existing tests
- Error handling paths not tested
- Edge cases not tested

REQUIREMENTS:
- All tests must pass
- Coverage must be >= 80%
"""

import math
from typing import Union, Optional

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """Add two numbers."""
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Subtract b from a."""
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """Multiply two numbers."""
    return a * b


def divide(a: Number, b: Number) -> Optional[float]:
    """Divide a by b.
    
    BUG: No handling for division by zero!
    Should return None or raise ValueError.
    """
    # BUG: Will crash on b=0
    return a / b


def power(base: Number, exponent: int) -> Number:
    """Raise base to the power of exponent.
    
    BUG: Wrong implementation for negative exponents!
    power(2, -2) should return 0.25, not -4
    """
    # BUG: Multiplies instead of using actual power
    if exponent < 0:
        return base * exponent  # BUG: Wrong calculation!
    
    result = 1
    for _ in range(exponent):
        result *= base
    return result


def factorial(n: int) -> int:
    """Calculate factorial of n.
    
    BUG: Doesn't handle n=0 or negative n!
    factorial(0) should return 1
    factorial(-5) should raise ValueError
    """
    # BUG: No check for n < 0
    # BUG: No special case for n = 0
    result = 1
    for i in range(1, n + 1):  # BUG: range(1, 0+1) returns empty, giving 1 correctly by accident
        result *= i
    return result


def sqrt(x: Number) -> Optional[float]:
    """Calculate square root of x.
    
    BUG: No handling for negative numbers!
    Should return None or raise ValueError.
    """
    # BUG: Will return complex number for negative x
    return math.sqrt(x)


def is_even(n: int) -> bool:
    """Check if n is even."""
    return n % 2 == 0


def is_prime(n: int) -> bool:
    """Check if n is prime.
    
    BUG: Wrong for n <= 1
    """
    # BUG: Returns True for 1 (not prime) and 0 (not prime)
    if n < 2:
        return n == 1  # BUG: 1 is not prime!
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor."""
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """Calculate least common multiple."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def average(numbers: list) -> Optional[float]:
    """Calculate average of a list of numbers.
    
    BUG: No handling for empty list!
    """
    # BUG: Will crash on empty list
    return sum(numbers) / len(numbers)


def median(numbers: list) -> Optional[Number]:
    """Calculate median of a list of numbers.
    
    BUG: No handling for empty list!
    """
    # BUG: Will crash on empty list
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    return sorted_nums[mid]


def mode(numbers: list) -> Optional[Number]:
    """Find the mode (most common value) in a list.
    
    BUG: No handling for empty list!
    """
    # BUG: Will crash on empty list
    if not numbers:
        return None
    
    counts = {}
    for n in numbers:
        counts[n] = counts.get(n, 0) + 1
    
    max_count = max(counts.values())
    for n, count in counts.items():
        if count == max_count:
            return n
    return None


def main():
    """Demo the calculator functions."""
    print("Calculator Demo")
    print(f"add(2, 3) = {add(2, 3)}")
    print(f"subtract(5, 2) = {subtract(5, 2)}")
    print(f"multiply(4, 3) = {multiply(4, 3)}")
    print(f"divide(10, 2) = {divide(10, 2)}")
    print(f"power(2, 3) = {power(2, 3)}")
    print(f"factorial(5) = {factorial(5)}")
    print(f"sqrt(16) = {sqrt(16)}")
    print(f"is_prime(7) = {is_prime(7)}")
    print(f"gcd(12, 8) = {gcd(12, 8)}")
    print(f"average([1,2,3,4,5]) = {average([1,2,3,4,5])}")


if __name__ == "__main__":
    main()

