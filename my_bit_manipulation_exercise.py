###### set bit 6
# bit mannipulation example
# OR operation

"""Step-by-Step Breakdown:

  1 << 3 - Creates a mask with bit 3 set:
  1 in binary:     00000001
  1 << 3:          00001000  (decimal 8)

  ~(1 << 3) - Inverts the mask:
  1 << 3:          00001000
  ~(1 << 3):       11110111  (all bits 1 except bit 3)

  num1 & ~(1 << 3) - Clears bit 3 in num1:
  Example: num1 = 15 (00001111)
  num1:            00001111
  ~(1 << 3):       11110111
  Result:          00000111  (decimal 7)

  Visual Example:

  num1 = 0b00001111  # 15 in decimal
  print(f"Before: {num1:08b} = {num1}")

  num1 = num1 & ~(1 << 3)  # Clear bit 3
  print(f"After:  {num1:08b} = {num1}")

  Output:
  Before: 00001111 = 15
  After:  00000111 = 7

  Common Bit Manipulation Pattern:

  - Set bit: num |= (1 << position)
  - Clear bit: num &= ~(1 << position) ← This is what you have
  - Toggle bit: num ^= (1 << position)
  - Check bit: (num >> position) & 1
"""

num = 0b00001111
print(f"num = {format(num,'08b')}")
# set bit 6
num = num | (1 << 6)
print(f"num = {num} (decimal), {bin(num)} (binary), {format(num, '08b')} (b-bit binary)")
print(f"num = {format(num,'08b')}")

print("###############################")

num1 = 0b00001111
print(f"num1 = {format(num1,'08b')}")
##### clear bit 3
num1 = num1 & ~(1 << 3)
print(f"num1 = {num1} (decimal), {bin(num1)} (binary), {format(num1, '08b')} (b-bit binary)")




