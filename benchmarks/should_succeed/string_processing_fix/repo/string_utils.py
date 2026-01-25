"""String utility functions with a bug."""

def reverse_string(s):
    """Reverse a string.
    
    Args:
        s: The string to reverse.
    
    Returns:
        The reversed string.
    """
    if not s:
        return ""
    
    # Bug: This function doesn't actually reverse the string
    # It just returns the original string
    return s

def main():
    """Test the string reversal function."""
    print("Testing string reversal...")
    
    test_cases = [
        ("Hello", "olleH"),
        ("World", "dlroW"),
        ("Hello World!", "!dlroW olleH"),
    ]
    
    for input_str, expected in test_cases:
        result = reverse_string(input_str)
        print(f"reverse_string('{input_str}') = '{result}' (expected: '{expected}')")
        if result == expected:
            print(f"  ✓ PASS")
        else:
            print(f"  ✗ FAIL")
    
    # Main test case
    test_input = "Hello World!"
    result = reverse_string(test_input)
    print(f"\nreversed_output: {result}")
    
    if result == "!dlroW olleH":
        print("SUCCESS: String correctly reversed")
    else:
        print(f"FAILED: Expected '!dlroW olleH', got '{result}'")

if __name__ == "__main__":
    main()

