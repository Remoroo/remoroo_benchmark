"""Statistics module with numerical instability bug.

This module calculates variance using the naive textbook formula:
    Var(X) = E[X²] - E[X]²

This formula is mathematically correct but numerically UNSTABLE!
When values are large, both E[X²] and E[X]² are huge numbers,
and subtracting them causes "catastrophic cancellation" - 
the significant digits cancel out, leaving only rounding errors.

Example of the problem:
    Data: [1e9 + 1, 1e9 + 2, 1e9 + 3]
    True variance: 0.6667
    Naive formula: Can return negative numbers or garbage!

The fix: Use Welford's online algorithm or two-pass method:
    1. First pass: compute mean
    2. Second pass: compute sum of squared deviations from mean
"""

import math
from typing import List

def mean(data: List[float]) -> float:
    """Calculate the arithmetic mean."""
    if not data:
        return 0.0
    return sum(data) / len(data)


def variance_naive(data: List[float]) -> float:
    """Calculate variance using the UNSTABLE naive formula.
    
    BUG: This suffers from catastrophic cancellation!
    
    The formula Var = E[X²] - E[X]² is mathematically correct
    but numerically unstable for large values.
    
    When X values are around 1e9:
    - E[X²] ≈ 1e18 (huge number)
    - E[X]² ≈ 1e18 (another huge number)
    - Their difference should be tiny (~0.667)
    - But floating point can't represent the precision needed!
    
    This can return:
    - Negative variance (impossible!)
    - Zero when it should be non-zero
    - Wildly incorrect positive values
    """
    if len(data) < 2:
        return 0.0
    
    n = len(data)
    
    # Compute E[X²] - sum of squares divided by n
    sum_sq = sum(x * x for x in data)
    mean_sq = sum_sq / n
    
    # Compute E[X]² - square of mean
    avg = sum(data) / n
    sq_mean = avg * avg
    
    # BUG: This subtraction causes catastrophic cancellation!
    # Both mean_sq and sq_mean are ~1e18, but variance should be ~0.667
    # The precision is lost in the large numbers
    variance = mean_sq - sq_mean
    
    return variance


def variance(data: List[float]) -> float:
    """Calculate variance - NEEDS TO BE FIXED!
    
    Currently uses the numerically unstable naive formula.
    
    TODO: Replace with a stable algorithm:
    
    Option 1: Two-pass algorithm
        1. First pass: compute mean
        2. Second pass: compute sum((x - mean)²) / n
    
    Option 2: Welford's online algorithm
        Initialize: mean = 0, M2 = 0, n = 0
        For each x:
            n += 1
            delta = x - mean
            mean += delta / n
            delta2 = x - mean
            M2 += delta * delta2
        Return M2 / n
    """
    return variance_naive(data)  # BUG: Using unstable algorithm!


def std_dev(data: List[float]) -> float:
    """Calculate standard deviation."""
    var = variance(data)
    if var < 0:
        # This should never happen with correct variance!
        print(f"WARNING: Negative variance {var}! Numerical instability detected.")
        return float('nan')
    return math.sqrt(var)


def main():
    """Test the statistics functions."""
    
    # Test 1: Small values (works fine)
    small_data = [1, 2, 3, 4, 5]
    print("Test 1: Small values [1, 2, 3, 4, 5]")
    print(f"  Mean: {mean(small_data)}")
    print(f"  Variance: {variance(small_data)}")
    print(f"  Std Dev: {std_dev(small_data)}")
    print()
    
    # Test 2: Large values with small variance (THE PROBLEM CASE)
    # True variance = Var([1, 2, 3]) = 0.6667
    large_data = [1e9 + 1, 1e9 + 2, 1e9 + 3]
    print("Test 2: Large values [1e9+1, 1e9+2, 1e9+3]")
    print(f"  Mean: {mean(large_data)}")
    
    var = variance(large_data)
    print(f"  Variance: {var}")
    print(f"  Std Dev: {std_dev(large_data)}")
    
    # The true variance is 2/3 ≈ 0.6667
    expected_variance = 2/3
    tolerance = 0.01
    
    variance_correct = abs(var - expected_variance) < tolerance
    
    print(f"\n  Expected variance: {expected_variance:.4f}")
    print(f"  Actual variance: {var}")
    print(f"  variance_correct: {variance_correct}")
    
    if variance_correct:
        print("\nSUCCESS: Variance calculation is numerically stable!")
    else:
        if var < 0:
            print(f"\nFAILED: Got NEGATIVE variance! Catastrophic cancellation occurred.")
        else:
            print(f"\nFAILED: Variance is wrong. Off by {abs(var - expected_variance):.2e}")
            print("This is due to numerical instability in the naive formula.")


if __name__ == "__main__":
    main()

