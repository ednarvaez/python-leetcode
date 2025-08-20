"""  Step-by-Step Breakdown

  What Each Line Does:

  1. bit = n & 1
    - Extracts the rightmost (least significant) bit of n
    - & 1 masks all bits except the last one
    - Example: 1101 & 0001 = 0001 (extracts the 1)
  2. result = (result << 1) | bit
    - result << 1: Shifts all bits in result one position left
    - | bit: Adds the extracted bit to the rightmost position
    - This builds the reversed number bit by bit
  3. n >>= 1
    - Shifts n one position right
    - Moves to the next bit for processing

  Visual Example

  Let's say n = 1101 (binary):

  Initial: n = 1101, result = 0000

  Iteration 1:
  - bit = 1101 & 1 = 1
  - result = (0000 << 1) | 1 = 0001
  - n = 1101 >> 1 = 0110

  Iteration 2:
  - bit = 0110 & 1 = 0
  - result = (0001 << 1) | 0 = 0010
  - n = 0110 >> 1 = 0011

  Iteration 3:
  - bit = 0011 & 1 = 1
  - result = (0010 << 1) | 1 = 0101
  - n = 0011 >> 1 = 0001

  Iteration 4:
  - bit = 0001 & 1 = 1
  - result = (0101 << 1) | 1 = 1011
  - n = 0001 >> 1 = 0000

  Result: 1101 becomes 1011 (reading the bits in reverse order)

  Purpose

  This is commonly used in algorithms that need to reverse the bit pattern
  of numbers, such as:
  - Digital signal processing (FFT algorithms)
  - Cryptography
  - Bit manipulation puzzles
  - Hardware interface programming
"""

for i in range(32):
    # Extract least significant bit
    bit = n & 1
    # Shift result left and add the bit
    result = (result << 1) | bit
    # Shift n right to process next bit
    n >>= 1
    
    
