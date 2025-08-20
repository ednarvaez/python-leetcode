"""Reverse Bits of an Integer (Python/C++) — Apple
Problem: Return the integer whose bit representation is reversed (e.g., 13 → 1101 → 1011 → 11).
Constraints: 32-bit unsigned"""




def reverse_bits(n: int) -> int:
    """
    Reverse bits of a 32-bit unsigned integer.
    
    Args:
        n: 32-bit unsigned integer
        
    Returns:
        Integer with reversed bit pattern
    """
    result = 0
    for i in range(32):
        # Extract least significant bit
        bit = n & 1
        # Shift result left and add the bit
        result = (result << 1) | bit
        # Shift n right to process next bit
        n >>= 1
    return result

def reverse_bits_optimized(n: int) -> int:
    """
    Optimized bit reversal using bit manipulation tricks.
    """
    # Swap pairs of bits
    n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)
    # Swap nibbles
    n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)
    # Swap bytes in pairs
    n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)
    # Swap 2-byte pairs
    n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)
    # Swap 4-byte pairs
    n = (n >> 16) | (n << 16)
    return n & 0xFFFFFFFF  # Ensure 32-bit result

def reverse_bits_builtin(n: int) -> int:
    """
    Using Python built-in functions (less efficient but concise).
    """
    # Convert to 32-bit binary string, reverse, convert back
    binary_str = format(n, '032b')
    reversed_str = binary_str[::-1]
    return int(reversed_str, 2)

# Test cases
def test_reverse_bits():
    test_cases = [
        (0b00000000000000000000000000000101, 0b10100000000000000000000000000000),  # 5 -> 2684354560
        (0b00000000000000000000000000001101, 0b10110000000000000000000000000000),  # 13 -> 2952790016
        (0xFFFFFFFF, 0xFFFFFFFF),  # All 1s -> All 1s
        (0x00000000, 0x00000000),  # All 0s -> All 0s
        (0x80000000, 0x00000001),  # MSB set -> LSB set
    ]
    
    for input_val, expected in test_cases:
        result = reverse_bits(input_val)
        print(f"Input: {input_val:08x} ({input_val:032b})")
        print(f"Output: {result:08x} ({result:032b})")
        print(f"Expected: {expected:08x} - {'PASS' if result == expected else 'FAIL'}")
        print()

if __name__ == "__main__":
    test_reverse_bits()