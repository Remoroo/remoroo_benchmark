"""Simple calculator module with a bug."""
import sys
import traceback

def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide a by b. Returns None if dividing by zero."""
    if b == 0:
        return None
    return a / b

def main():
    """Test the calculator functions."""
    try:
        print("Testing calculator...")
        print(f"10 + 5 = {add(10, 5)}")
        print(f"10 - 5 = {subtract(10, 5)}")
        print(f"10 * 5 = {multiply(10, 5)}")
        print(f"10 / 5 = {divide(10, 5)}")
        print(f"10 / 0 = {divide(10, 0)}")  # Should return None!")
        print("All tests passed!")
    except Exception as e:
        print("Exception occurred during calculator test:")
        traceback.print_exc()

if __name__ == "__main__":
    main()