def is_power_of_two_basic(n):
    """
    BASIC APPROACH: Division method
    Interview Strategy: Start with this approach to show logical thinking
    Time: O(log n), Space: O(1)
    """
    # Edge case: powers of 2 must be positive (2^0=1, 2^1=2, etc.)
    if n <= 0:
        return False
    
# The comment `# Keep dividing by 2 while the number is even` is describing the logic implemented in
# the `is_power_of_two_basic` function in the Python code snippet.
    # Keep dividing by 2 while the number is even
    # If n is a power of 2, we should eventually reach 1
    while n % 2 == 0:  # Check if n is divisible by 2
        n //= 2         # Integer division by 2 (equivalent to right shift)
        
    # If we've divided out all factors of 2 and are left with 1,
    # then the original number was a power of 2
    return n == 1  # Fixed: should return n == 1, not just n


def is_power_of_two_bit_manipulation(n):
    """
    BIT MANIPULATION APPROACH: Brian Kernighan's algorithm
    Interview Strategy: This is the "wow" solution that impresses hardware interviewers
    Time: O(1), Space: O(1)
    
    Key Insight: Powers of 2 have exactly ONE bit set in binary:
    1 = 0001, 2 = 0010, 4 = 0100, 8 = 1000
    
    The trick: n & (n-1) turns off the rightmost set bit
    If n is a power of 2, this operation gives 0
    """
    # First check: n must be positive (eliminates n <= 0)
    # Second check: n & (n-1) == 0 means n has exactly one bit set
    #
    # Example walkthrough for n = 8:
    # 8 in binary:     1000
    # 8-1 = 7 binary:  0111  
    # 8 & 7:           0000  ← Result is 0, so 8 is power of 2
    #
    # Example walkthrough for n = 6:
    # 6 in binary:     0110
    # 6-1 = 5 binary:  0101
    # 6 & 5:           0100  ← Result is not 0, so 6 is not power of 2
    return n > 0 and (n & (n - 1)) == 0

# Test the functions
def test_power_of_two():
    """
    TESTING STRATEGY for interviews:
    1. Include edge cases (0, negative numbers)
    2. Include obvious powers of 2 (1, 2, 4, 8, 16)
    3. Include numbers that are NOT powers of 2 (3, 6, 10)
    4. Show both approaches give same results
    """
    # Carefully chosen test cases covering edge cases and common scenarios
    test_cases = [1, 2, 4, 8, 16, 3, 6, 10, 0, -1]
    
    print("Testing Power of 2 Detection:")
    print("Number | Basic | Bit Manipulation")
    print("-" * 35)
    
    # Test both implementations on each test case
    for num in test_cases:
        # Get results from both approaches
        basic_result = is_power_of_two_basic(num)
        bit_result = is_power_of_two_bit_manipulation(num)
        
        # Display formatted results for easy comparison
        print(f"{num:6} | {basic_result:5} | {bit_result:13}")

if __name__ == "__main__":
    """
    INTERVIEW TIP: Always include a main block to demonstrate your code works
    This shows you think about testing and validation
    """
    print("Apple Silicon Validation Coding Interview Practice")
    print("=" * 55)
    
    # Run all tests to verify both approaches work correctly
    test_power_of_two()
    