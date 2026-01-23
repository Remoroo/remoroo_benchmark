"""Tests for calculator module.

NOTE: These tests are incomplete!
- Only covers basic happy paths
- Many edge cases missing
- Need to add more tests to achieve 80% coverage

Current coverage: ~40%
Target coverage: >= 80%
"""

import pytest
import calc


class TestBasicOperations:
    """Tests for basic arithmetic operations."""
    
    def test_add_positive(self):
        assert calc.add(2, 3) == 5
    
    def test_subtract_positive(self):
        assert calc.subtract(5, 2) == 3
    
    def test_multiply_positive(self):
        assert calc.multiply(4, 3) == 12


class TestDivide:
    """Tests for division."""
    
    def test_divide_positive(self):
        assert calc.divide(10, 2) == 5.0
    
    def test_divide_by_zero(self):
        """BUG: This test will FAIL because divide() crashes on zero."""
        # Should return None, but currently crashes
        result = calc.divide(10, 0)
        assert result is None


class TestPower:
    """Tests for power function."""
    
    def test_power_positive(self):
        assert calc.power(2, 3) == 8
    
    def test_power_zero(self):
        assert calc.power(5, 0) == 1
    
    def test_power_negative_exponent(self):
        """BUG: This test will FAIL because of wrong implementation."""
        # power(2, -2) should return 0.25
        assert calc.power(2, -2) == 0.25


class TestFactorial:
    """Tests for factorial function."""
    
    def test_factorial_positive(self):
        assert calc.factorial(5) == 120
    
    def test_factorial_zero(self):
        """factorial(0) should return 1."""
        assert calc.factorial(0) == 1
    
    def test_factorial_negative(self):
        """BUG: Should raise ValueError for negative input."""
        with pytest.raises(ValueError):
            calc.factorial(-5)


class TestSqrt:
    """Tests for square root function."""
    
    def test_sqrt_positive(self):
        assert calc.sqrt(16) == 4.0
    
    def test_sqrt_negative(self):
        """BUG: This test will FAIL because sqrt() crashes on negative."""
        # Should return None, but currently crashes
        result = calc.sqrt(-16)
        assert result is None


class TestIsPrime:
    """Tests for prime checking."""
    
    def test_is_prime_7(self):
        assert calc.is_prime(7) == True
    
    def test_is_prime_4(self):
        assert calc.is_prime(4) == False
    
    def test_is_prime_1(self):
        """BUG: 1 is NOT prime, but function returns True."""
        assert calc.is_prime(1) == False
    
    def test_is_prime_0(self):
        """0 is NOT prime."""
        assert calc.is_prime(0) == False


# MISSING TESTS (needed for coverage):
# - test_add_negative
# - test_subtract_negative
# - test_multiply_negative
# - test_divide_negative
# - test_is_even
# - test_gcd
# - test_lcm
# - test_average
# - test_average_empty
# - test_median
# - test_median_even_length
# - test_median_empty
# - test_mode
# - test_mode_empty


def run_coverage_check():
    """Helper to run coverage and save results."""
    import subprocess
    import json
    import os
    
    # Run pytest with coverage
    result = subprocess.run(
        ["python", "-m", "pytest", "test_calc.py", 
         "--cov=calc", "--cov-report=json", "-v"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    # Read coverage report
    if os.path.exists("coverage.json"):
        with open("coverage.json", "r") as f:
            coverage_data = json.load(f)
        
        total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
        
        # Save to artifacts
        os.makedirs("artifacts", exist_ok=True)
        with open("artifacts/coverage.json", "w") as f:
            json.dump({
                "tests_pass": result.returncode == 0,
                "coverage": total_coverage,
                "details": coverage_data.get("totals", {})
            }, f, indent=2)
        
        print(f"\n=== Coverage Summary ===")
        print(f"tests_pass: {result.returncode == 0}")
        print(f"coverage: {total_coverage:.1f}%")
        
        return result.returncode == 0, total_coverage
    
    return False, 0


if __name__ == "__main__":
    run_coverage_check()

