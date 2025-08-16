"""
Apple Silicon Validation Coding Interview Practice
Common coding questions and solutions with step-by-step explanations
"""

# ============================================================================
# PROBLEM 1: Check if a number is a power of 2 (Common in hardware validation)
# ============================================================================

def is_power_of_two_basic(n):
    """
    INTERVIEW STRATEGY: Start with this intuitive approach first
    Basic approach: Keep dividing by 2
    Time: O(log n), Space: O(1)
    """
    # Handle edge cases: powers of 2 are positive integers
    if n <= 0:
        return False
    
    # Keep dividing by 2 while n is even
    # If n is truly a power of 2, we'll eventually reach 1
    while n % 2 == 0:  # Check if n is divisible by 2
        n //= 2         # Divide by 2 (same as right shift by 1)
    
    # If we've removed all factors of 2 and have 1 left, it was a power of 2
    return n == 1

def is_power_of_two_bit_manipulation(n):
    """
    INTERVIEW GOLD: This is the solution that wows hardware interviewers
    Bit manipulation approach using Brian Kernighan's algorithm
    
    Key insight: Powers of 2 have exactly ONE bit set in binary
    Examples: 1=0001, 2=0010, 4=0100, 8=1000, 16=10000
    
    Magic trick: n & (n-1) clears the rightmost set bit
    If n is power of 2, this gives 0 (since only one bit was set)
    Time: O(1), Space: O(1)
    """
    # Two conditions must be met:
    # 1. n > 0 (powers of 2 are positive)
    # 2. n & (n-1) == 0 (exactly one bit set)
    #
    # Example: n = 8 (binary: 1000)
    # n-1 = 7 (binary: 0111)
    # 8 & 7 = 1000 & 0111 = 0000 ✓
    #
    # Counter-example: n = 6 (binary: 0110) 
    # n-1 = 5 (binary: 0101)
    # 6 & 5 = 0110 & 0101 = 0100 ≠ 0 ✗
    return n > 0 and (n & (n - 1)) == 0

# Test the functions
def test_power_of_two():
    test_cases = [1, 2, 4, 8, 16, 3, 6, 10, 0, -1]
    print("Testing Power of 2 Detection:")
    print("Number | Basic | Bit Manipulation")
    print("-" * 35)
    
    for num in test_cases:
        basic_result = is_power_of_two_basic(num)
        bit_result = is_power_of_two_bit_manipulation(num)
        print(f"{num:6} | {basic_result:5} | {bit_result:13}")

# ============================================================================
# PROBLEM 2: Count number of 1s in binary representation (Hamming Weight)
# ============================================================================

def count_ones_basic(n):
    """
    BASIC APPROACH: Use built-in Python functions
    Good for explaining the problem, but interviewers want manual implementation
    Time: O(log n), Space: O(log n) due to string creation
    """
    # bin() converts to binary string like '0b1010'
    # count('1') counts occurrences of character '1'
    return bin(n).count('1')

def count_ones_bit_manipulation(n):
    """
    OPTIMAL APPROACH: Brian Kernighan's algorithm
    This is the hardware engineer's favorite - shows deep bit understanding
    
    Key insight: n & (n-1) removes the rightmost set bit
    We count how many times we can remove a set bit until n becomes 0
    Time: O(number of set bits), Space: O(1)
    """
    count = 0
    while n:  # While n is not zero (has set bits remaining)
        count += 1          # Increment count for this set bit
        n &= (n - 1)        # Remove the rightmost set bit
        
        # Example walkthrough for n = 12 (binary: 1100)
        # Iteration 1: n = 1100, n-1 = 1011, n &= (n-1) → n = 1000, count = 1
        # Iteration 2: n = 1000, n-1 = 0111, n &= (n-1) → n = 0000, count = 2
        # Result: 12 has 2 set bits
    return count

def test_count_ones():
    test_cases = [5, 7, 15, 16, 31, 0]
    print("\nTesting Count of 1s in Binary:")
    print("Number | Binary    | Basic | Bit Manipulation")
    print("-" * 45)
    
    for num in test_cases:
        binary_repr = bin(num)[2:]  # Remove '0b' prefix
        basic_result = count_ones_basic(num)
        bit_result = count_ones_bit_manipulation(num)
        print(f"{num:6} | {binary_repr:9} | {basic_result:5} | {bit_result:13}")

# ============================================================================
# PROBLEM 3: Find single number (XOR application - common in error detection)
# ============================================================================

def find_single_number(nums):
    """
    CLASSIC XOR PROBLEM: Perfect for hardware validation interviews
    
    Problem: Given array where every element appears twice except one, find the single one
    
    XOR PROPERTIES (crucial for hardware understanding):
    1. a ^ a = 0 (anything XOR with itself is 0)
    2. a ^ 0 = a (anything XOR with 0 is itself)  
    3. XOR is commutative: a ^ b = b ^ a
    4. XOR is associative: (a ^ b) ^ c = a ^ (b ^ c)
    
    Strategy: XOR all numbers together
    - Pairs will cancel out to 0
    - Single number will remain
    
    Time: O(n), Space: O(1)
    """
    result = 0  # Start with 0 (identity element for XOR)
    
    # XOR all numbers together
    for num in nums:
        result ^= num  # XOR accumulator with current number
        
        # Example walkthrough for [4, 1, 2, 1, 2]:
        # result = 0
        # result ^= 4  → result = 4    (0 ^ 4 = 4)
        # result ^= 1  → result = 5    (4 ^ 1 = 5) 
        # result ^= 2  → result = 7    (5 ^ 2 = 7)
        # result ^= 1  → result = 6    (7 ^ 1 = 6, cancels previous 1)
        # result ^= 2  → result = 4    (6 ^ 2 = 4, cancels previous 2)
        # Final result: 4 (the single number)
    
    return result

def test_single_number():
    test_cases = [
        [2, 2, 1],
        [4, 1, 2, 1, 2],
        [1],
        [7, 3, 5, 4, 5, 3, 4]
    ]
    
    print("\nTesting Find Single Number (XOR):")
    for i, nums in enumerate(test_cases):
        result = find_single_number(nums)
        print(f"Test {i+1}: {nums} -> Single number: {result}")

# ============================================================================
# PROBLEM 4: Binary Search (Common in validation algorithms)
# ============================================================================

def binary_search(arr, target):
    """
    FUNDAMENTAL ALGORITHM: Binary search - essential for any tech interview
    
    Prerequisite: Array must be sorted
    Strategy: Divide search space in half each iteration
    
    INTERVIEW TIP: Always clarify if array is sorted!
    Time: O(log n), Space: O(1)
    """
    # Initialize search boundaries
    left, right = 0, len(arr) - 1  # Include both endpoints in search space
    
    # Continue while search space is valid
    while left <= right:  # Equal is important - single element case
        
        # Calculate middle index (avoid overflow in other languages)
        mid = (left + right) // 2  # In Python, // is safe from overflow
        # Alternative: mid = left + (right - left) // 2 (overflow-safe in C++)
        
        # Check if we found the target
        if arr[mid] == target:
            return mid  # Return index where target was found
            
        # Target is in the right half
        elif arr[mid] < target:
            left = mid + 1  # Exclude mid from search space
            
        # Target is in the left half  
        else:
            right = mid - 1  # Exclude mid from search space
    
    # Target not found in array
    return -1

def test_binary_search():
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    targets = [7, 1, 15, 6, 0, 20]
    
    print("\nTesting Binary Search:")
    print(f"Array: {arr}")
    print("Target | Index")
    print("-" * 15)
    
    for target in targets:
        index = binary_search(arr, target)
        print(f"{target:6} | {index:5}")

# ============================================================================
# PROBLEM 5: Two Sum (Array manipulation - common pattern)
# ============================================================================

def two_sum(nums, target):
    """
    HASH MAP PATTERN: One of the most important interview patterns
    
    Problem: Find indices of two numbers that add up to target
    
    BRUTE FORCE: O(n²) - check all pairs
    OPTIMIZED: O(n) using hash map - trade space for time
    
    Strategy: For each number, check if its complement exists in what we've seen
    Time: O(n), Space: O(n)
    """
    # Hash map to store: {value: index}
    # This allows O(1) lookup of complements
    num_map = {}
    
    # Iterate through array with both index and value
    for i, num in enumerate(nums):
        
        # Calculate what number we need to reach target
        complement = target - num  # If num + complement = target
        
        # Check if we've seen the complement before
        if complement in num_map:  # O(1) hash map lookup
            # Found the pair! Return indices
            return [num_map[complement], i]  # Earlier index first
            
        # Haven't seen complement yet, store current number and index
        num_map[num] = i
        
        # Example walkthrough for nums=[2,7,11,15], target=9:
        # i=0, num=2, complement=7, num_map={} → store {2: 0}
        # i=1, num=7, complement=2, num_map={2: 0} → found! return [0, 1]
    
    # No solution found (problem guarantees solution exists)
    return []

def test_two_sum():
    test_cases = [
        ([2, 7, 11, 15], 9),
        ([3, 2, 4], 6),
        ([3, 3], 6),
        ([1, 2, 3, 4, 5], 8)
    ]
    
    print("\nTesting Two Sum:")
    for nums, target in test_cases:
        result = two_sum(nums, target)
        print(f"Array: {nums}, Target: {target} -> Indices: {result}")
        if result:
            print(f"  Values: {nums[result[0]]} + {nums[result[1]]} = {target}")

# ============================================================================
# PROBLEM 6: Simulate Register Operations (Hardware-specific)
# ============================================================================

class RegisterSimulator:
    """
    HARDWARE VALIDATION GOLD: This shows you understand silicon validation
    
    Simulates basic register operations that you'd encounter in:
    - CPU register manipulation
    - Memory-mapped I/O registers  
    - Control/status registers
    - Hardware state machines
    """
    
    def __init__(self, size=8):
        """
        Initialize a register of given bit width
        size: Number of bits in the register (e.g., 8, 16, 32, 64)
        """
        self.size = size
        self.register = 0  # Start with all bits cleared
        self.max_value = (1 << size) - 1  # 2^size - 1 (all bits set)
        
        # Example for 8-bit register:
        # max_value = (1 << 8) - 1 = 256 - 1 = 255 = 0xFF = 11111111
    
    def set_bit(self, position):
        """
        Set bit at position to 1 (register |= mask)
        Common in: Enabling features, setting flags, interrupt enables
        """
        if 0 <= position < self.size:  # Bounds checking
            # Create mask with bit set at position: 1 << position
            # OR with register to set that bit: register |= mask
            self.register |= (1 << position)
            
            # Example: set_bit(3) on register 0000 → mask 1000 → result 1000
    
    def clear_bit(self, position):
        """
        Clear bit at position to 0 (register &= ~mask)
        Common in: Disabling features, clearing flags, acknowledging interrupts
        """
        if 0 <= position < self.size:  # Bounds checking
            # Create mask with bit set: 1 << position
            # Invert mask: ~(1 << position) - all bits set except position
            # AND with register to clear that bit: register &= ~mask
            self.register &= ~(1 << position)
            
            # Example: clear_bit(3) on register 1111 → mask ~1000 = 0111 → result 0111
    
    def toggle_bit(self, position):
        """
        Toggle bit at position (register ^= mask)
        Common in: State machines, toggling GPIO pins, test patterns
        """
        if 0 <= position < self.size:  # Bounds checking
            # Create mask and XOR to flip the bit: register ^= mask
            self.register ^= (1 << position)
            
            # Example: toggle_bit(3) on 0101 → mask 1000 → result 1101
            # Example: toggle_bit(3) on 1101 → mask 1000 → result 0101
    
    def get_bit(self, position):
        """
        Read bit value at position (isolate and shift)
        Common in: Reading status flags, checking conditions
        """
        if 0 <= position < self.size:  # Bounds checking
            # Right shift to move bit to LSB, then mask with 1
            return (self.register >> position) & 1
            
            # Example: get_bit(3) on 1010 → (1010 >> 3) = 0001 → 0001 & 1 = 1
        return 0  # Invalid position returns 0
    
    def get_binary_string(self):
        """
        Get binary representation with leading zeros
        Useful for: Debugging, visualization, test output
        """
        # format() with '0{size}b' pads with leading zeros
        return format(self.register, f'0{self.size}b')
        
        # Example: 8-bit register with value 5 → '00000101'
    
    def reset(self):
        """
        Reset register to all zeros
        Common in: System reset, initialization, clearing state
        """
        self.register = 0

def test_register_simulator():
    print("\nTesting Register Simulator:")
    reg = RegisterSimulator(8)  # 8-bit register
    
    print(f"Initial state: {reg.get_binary_string()} (decimal: {reg.register})")
    
    # Set some bits
    reg.set_bit(0)  # Set LSB
    reg.set_bit(3)  # Set bit 3
    reg.set_bit(7)  # Set MSB
    print(f"After setting bits 0,3,7: {reg.get_binary_string()} (decimal: {reg.register})")
    
    # Clear a bit
    reg.clear_bit(3)
    print(f"After clearing bit 3: {reg.get_binary_string()} (decimal: {reg.register})")
    
    # Toggle a bit
    reg.toggle_bit(1)
    print(f"After toggling bit 1: {reg.get_binary_string()} (decimal: {reg.register})")
    
    # Check individual bits
    print(f"Bit 0: {reg.get_bit(0)}, Bit 1: {reg.get_bit(1)}, Bit 7: {reg.get_bit(7)}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("Apple Silicon Validation Coding Interview Practice")
    print("=" * 55)
    
    # Run all tests
    test_power_of_two()
    test_count_ones()
    test_single_number()
    test_binary_search()
    test_two_sum()
    test_register_simulator()
    
    print("\n" + "=" * 55)
    print("Practice Tips for Apple Silicon Validation Interviews:")
    print("1. Focus on bit manipulation - it's crucial for hardware roles")
    print("2. Understand time/space complexity analysis")
    print("3. Practice explaining your thought process clearly")
    print("4. Know basic data structures and algorithms")
    print("5. Be familiar with register operations and binary representations")