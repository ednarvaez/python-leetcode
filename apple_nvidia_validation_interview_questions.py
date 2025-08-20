"""
APPLE & NVIDIA POST SILICON VALIDATION INTERVIEW QUESTIONS
Based on real interview experiences from Glassdoor, Blind, and LeetCode discussions

RESEARCH INSIGHTS:
- Apple focuses heavily on bit manipulation and hardware understanding
- Nvidia asks medium-difficulty LeetCode questions with practical hardware twists
- Both companies expect deep technical knowledge beyond just coding
- Assembly language understanding is often tested
- Cache coherency and memory management questions are common
"""

import math
from typing import List, Optional

# ============================================================================
# PART 1: ACTUAL APPLE INTERVIEW QUESTIONS (From Glassdoor/Blind)
# ============================================================================

def power_of_two_validation(n: int) -> bool:
    """
    ACTUAL APPLE QUESTION: "Check if a register size is a valid power of 2"
    
    INTERVIEW CONTEXT: Apple validation engineers often need to verify that
    cache line sizes, register widths, and memory block sizes are powers of 2
    
    HARDWARE SIGNIFICANCE:
    - Cache lines must be powers of 2 for efficient addressing
    - Register widths (8, 16, 32, 64 bits) are always powers of 2
    - Memory alignment requirements depend on power-of-2 boundaries
    
    INTERVIEWER EXPECTATION: Start with basic approach, then show bit manipulation
    """
    # Edge case: powers of 2 must be positive
    if n <= 0:
        return False
    
    # BIT MANIPULATION MAGIC: Brian Kernighan's algorithm
    # Powers of 2 have exactly ONE bit set in binary representation
    # n & (n-1) clears the rightmost set bit
    # If only one bit was set, result becomes 0
    return (n & (n - 1)) == 0

def set_nth_bit_register(register_value: int, bit_position: int) -> int:
    """
    ACTUAL APPLE QUESTION: "Set the nth bit in a register value"
    
    HARDWARE CONTEXT: 
    - Setting interrupt enable bits
    - Configuring control register
    ACTUAL APPLE QUESTION: "Set the nth bit in a register value"
    
    HARDWARE CONTEXT: 
    - Setting interrupt enable bits
    - Configuring control registers
    - Enabling features in status registers
    s
    - Enabling features in status registers
    
    INTERVIEW TIP: Explain the OR operation and bit masking clearly
    """
    # Create a mask with only the nth bit set
    # 1 << bit_position creates: ...00001000... (1 at position n)
    mask = 1 << bit_position
    
    # OR operation sets the bit: original | mask
    # If bit was 0: 0 | 1 = 1 (sets the bit)
    # If bit was 1: 1 | 1 = 1 (keeps it set)
    return register_value | mask

def clear_nth_bit_register(register_value: int, bit_position: int) -> int:
    """
    ACTUAL APPLE QUESTION: "Clear the nth bit in a register value"
    
    HARDWARE CONTEXT:
    - Clearing interrupt flags
    - Disabling features
    - Acknowledging status bits
    
    BITWISE EXPLANATION: Use AND with inverted mask
    """
    # Create mask with nth bit set: ...00001000...
    mask = 1 << bit_position
    
    # Invert mask to get: ...11110111... (0 at position n, 1s elsewhere)
    inverted_mask = ~mask
    
    # AND operation clears the bit: original & inverted_mask
    # Target bit: anything & 0 = 0 (clears the bit)
    # Other bits: anything & 1 = unchanged
    return register_value & inverted_mask

def replace_bits_in_register(register_value: int, replacement: int, start_bit: int, end_bit: int) -> int:
    """
    ACTUAL APPLE QUESTION: "Replace bits 16-13 with another number"
    
    SILICON VALIDATION USE CASE:
    - Updating specific bit fields in control registers
    - Modifying configuration values without affecting other bits
    - Implementing atomic register updates
    
    ALGORITHM BREAKDOWN:
    1. Create mask to clear target bit range
    2. Clear the target bits in original value
    3. Shift replacement value to correct position
    4. OR the shifted replacement with cleared original
    """
    # Calculate bit range width
    num_bits = end_bit - start_bit + 1
    
    # Create mask with 1s in target range: (1 << num_bits) - 1
    # Example: 4 bits -> (1 << 4) - 1 = 16 - 1 = 15 = 0b1111
    range_mask = (1 << num_bits) - 1
    
    # Shift mask to target position
    positioned_mask = range_mask << start_bit
    
    # Invert mask to clear target bits: ~positioned_mask
    clear_mask = ~positioned_mask
    
    # Clear target bits in original register
    cleared_register = register_value & clear_mask
    
    # Ensure replacement fits in the bit range
    masked_replacement = replacement & range_mask
    
    # Shift replacement to target position
    positioned_replacement = masked_replacement << start_bit
    
    # Combine cleared register with positioned replacement
    return cleared_register | positioned_replacement

# ============================================================================
# PART 2: NVIDIA INTERVIEW QUESTIONS (From LeetCode Experience)
# ============================================================================

def count_set_bits_hamming_weight(n: int) -> int:
    """
    ACTUAL NVIDIA QUESTION: "Count number of 1s in binary representation"
    
    HARDWARE SIGNIFICANCE:
    - Error detection in memory systems
    - Parity checking in communication protocols
    - Population count in parallel processing
    
    INTERVIEW APPROACH: Show multiple solutions with complexity analysis
    """
    # APPROACH 1: Built-in function (mention but don't use in interview)
    # return bin(n).count('1')
    
    # APPROACH 2: Brian Kernighan's algorithm (preferred for hardware interviews)
    count = 0
    while n:
        count += 1
        n &= (n - 1)  # Remove rightmost set bit
        # This loop runs exactly as many times as there are set bits
        # Time: O(number of set bits), Space: O(1)
    
    return count

def find_single_number_xor(nums: List[int]) -> int:
    """
    NVIDIA FAVORITE: "Find single number where others appear twice"
    
    XOR PROPERTIES (crucial for hardware understanding):
    1. a ^ a = 0 (self-canceling)
    2. a ^ 0 = a (identity)
    3. XOR is commutative and associative
    
    HARDWARE APPLICATION:
    - Error detection and correction
    - Checksum calculations
    - Parity generation
    """
    result = 0
    # XOR all numbers together
    # Pairs will cancel out due to a ^ a = 0
    # Single number will remain due to a ^ 0 = a
    for num in nums:
        result ^= num
    return result

def maximum_depth_binary_tree(root: Optional['TreeNode']) -> int:
    """
    ACTUAL NVIDIA QUESTION: "Find maximum depth of binary tree"
    LeetCode: https://leetcode.com/problems/maximum-depth-of-binary-tree/
    
    HARDWARE CONTEXT:
    - Analyzing circuit timing paths
    - Cache hierarchy depth calculations
    - Pipeline stage counting
    
    APPROACH: Recursive depth-first search
    """
    # Base case: empty tree has depth 0
    if not root:
        return 0
    
    # Recursive case: 1 + maximum depth of subtrees
    # This represents the longest path from root to any leaf
    left_depth = maximum_depth_binary_tree(root.left)
    right_depth = maximum_depth_binary_tree(root.right)
    
    return 1 + max(left_depth, right_depth)

def last_stone_weight(stones: List[int]) -> int:
    """
    NVIDIA FAVORITE QUESTION: "Last Stone Weight"
    
    PROBLEM: Given stones with weights, repeatedly:
    1. Pick two heaviest stones
    2. If equal weight, both destroyed
    3. If different, replace with difference
    4. Return weight of last stone (or 0)
    
    HARDWARE PARALLEL: Resource allocation and load balancing
    """
    import heapq
    
    # Python heapq is min-heap, so negate values for max-heap behavior
    max_heap = [-stone for stone in stones]
    heapq.heapify(max_heap)
    
    # Continue until at most one stone remains
    while len(max_heap) > 1:
        # Extract two heaviest stones (negate to get original values)
        first = -heapq.heappop(max_heap)   # Heaviest
        second = -heapq.heappop(max_heap)  # Second heaviest
        
        # If stones have different weights, add difference back
        if first != second:
            heapq.heappush(max_heap, -(first - second))
    
    # Return last stone weight (or 0 if no stones left)
    return -max_heap[0] if max_heap else 0

# ============================================================================
# PART 3: ASSEMBLY LANGUAGE QUESTIONS (Common in Hardware Interviews)
# ============================================================================

def assembly_multiply_explanation():
    """
    ACTUAL INTERVIEW QUESTION: "Implement A*B*C using basic assembly instructions"
    
    AVAILABLE INSTRUCTIONS: ADD, SUB, JNZ (jump if not zero), JZ (jump if zero), MOV
    
    ALGORITHM: Multiplication by repeated addition
    A * B means adding A to itself B times
    """
    print("ASSEMBLY MULTIPLICATION ALGORITHM")
    print("=" * 40)
    print("\nProblem: Calculate A * B * C using only ADD, SUB, JNZ, JZ, MOV")
    print("\nSolution breakdown:")
    print("1. First calculate A * B using repeated addition")
    print("2. Then multiply result by C")
    print("\nPseudo-assembly for A * B:")
    
    assembly_code = """
    ; Input: A in register R1, B in register R2
    ; Output: A*B in register R3
    
    MOV R3, 0        ; Initialize result to 0
    MOV R4, R2       ; Copy B to counter
    
    LOOP:
    JZ R4, DONE      ; If counter is 0, we're done
    ADD R3, R1       ; Add A to result
    SUB R4, 1        ; Decrement counter
    JNZ R4, LOOP     ; If counter not zero, continue loop
    
    DONE:
    ; R3 now contains A * B
    """
    
    print(assembly_code)
    print("\nKEY INSIGHTS FOR INTERVIEWERS:")
    print("- Multiplication is repeated addition")
    print("- Loop control using conditional jumps")
    print("- Register management and data flow")
    print("- Time complexity: O(B) for A * B")

def memory_alignment_check(address: int, alignment: int) -> bool:
    """
    COMMON HARDWARE QUESTION: "Check if memory address is aligned to N-byte boundary"
    
    ALIGNMENT REQUIREMENTS:
    - 32-bit integers: must be 4-byte aligned (address % 4 == 0)
    - 64-bit integers: must be 8-byte aligned (address % 8 == 0)
    - Cache lines: typically 64-byte aligned (address % 64 == 0)
    
    BIT MANIPULATION TRICK: address & (alignment - 1) == 0
    This works because alignment is always a power of 2
    """
    # Verify alignment is power of 2
    if alignment <= 0 or (alignment & (alignment - 1)) != 0:
        raise ValueError("Alignment must be a positive power of 2")
    
    # Check alignment using bit manipulation
    # If address is aligned, lower bits should be zero
    # alignment - 1 creates mask with 1s in lower bits
    # AND operation isolates these bits
    return (address & (alignment - 1)) == 0

# ============================================================================
# PART 4: CACHE COHERENCY AND MEMORY VALIDATION
# ============================================================================

def cache_line_size_validator(size: int) -> bool:
    """
    APPLE INTERVIEW CONTEXT: "Validate cache line size configuration"
    
    REQUIREMENTS:
    - Must be power of 2
    - Typically between 16 and 512 bytes
    - Common sizes: 32, 64, 128, 256 bytes
    
    HARDWARE SIGNIFICANCE:
    - Affects memory bandwidth utilization
    - Impacts cache efficiency
    - Determines optimal data structure alignment
    """
    # Check if size is positive power of 2
    if size <= 0 or (size & (size - 1)) != 0:
        return False
    
    # Check if size is in valid range for cache lines
    MIN_CACHE_LINE = 16   # 16 bytes minimum
    MAX_CACHE_LINE = 512  # 512 bytes maximum
    
    return MIN_CACHE_LINE <= size <= MAX_CACHE_LINE

def validate_register_width(width: int) -> bool:
    """
    HARDWARE VALIDATION: "Check if register width is valid"
    
    VALID REGISTER WIDTHS: 8, 16, 32, 64, 128, 256, 512 bits
    All must be powers of 2 and at least 8 bits
    """
    # Must be positive power of 2
    if width <= 0 or (width & (width - 1)) != 0:
        return False
    
    # Must be at least 8 bits
    if width < 8:
        return False
    
    # Common register widths in modern processors
    valid_widths = {8, 16, 32, 64, 128, 256, 512}
    return width in valid_widths

# ============================================================================
# PART 5: PRACTICAL HARDWARE DEBUGGING SCENARIOS
# ============================================================================

def find_faulty_memory_bit(good_value: int, faulty_value: int) -> int:
    """
    REAL HARDWARE DEBUG SCENARIO: "Find which bit is stuck/flipped in memory"
    
    APPROACH: XOR the values to find differing bits
    Then find position of the differing bit
    
    HARDWARE CONTEXT:
    - Single bit errors in RAM
    - Stuck-at faults in memory cells
    - Cosmic ray induced bit flips
    """
    # XOR reveals differing bits (1 where bits differ, 0 where same)
    diff = good_value ^ faulty_value
    
    # Check if exactly one bit differs (single bit error)
    if diff == 0:
        return -1  # No difference
    
    if (diff & (diff - 1)) != 0:
        return -2  # Multiple bit errors
    
    # Find position of the single differing bit
    bit_position = 0
    while diff > 1:
        diff >>= 1
        bit_position += 1
    
    return bit_position

def detect_interrupt_priority_conflicts(interrupt_mask: int, priority_levels: List[int]) -> List[int]:
    """
    HARDWARE VALIDATION: "Detect conflicting interrupt priorities"
    
    PROBLEM: Multiple interrupts shouldn't have same priority level
    Given interrupt mask and priority levels, find conflicts
    
    APPROACH: Use bit manipulation to track seen priorities
    """
    conflicts = []
    seen_priorities = 0  # Bit vector to track seen priority levels
    
    for i, priority in enumerate(priority_levels):
        # Check if this interrupt is enabled (bit set in mask)
        if interrupt_mask & (1 << i):
            # Check if this priority level was already seen
            priority_bit = 1 << priority
            
            if seen_priorities & priority_bit:
                conflicts.append(priority)
            else:
                seen_priorities |= priority_bit
    
    return conflicts

# ============================================================================
# PART 6: TESTING AND VALIDATION FUNCTIONS
# ============================================================================

def test_power_of_two_validation():
    """Test power of 2 validation with hardware-relevant examples"""
    print("\nTESTING POWER OF 2 VALIDATION")
    print("=" * 35)
    
    # Test cases: cache line sizes, register widths, memory sizes
    test_cases = [
        (32, True, "32-byte cache line"),
        (64, True, "64-byte cache line"),
        (128, True, "128-bit register"),
        (33, False, "Invalid cache size"),
        (0, False, "Invalid zero size"),
        (1024, True, "1KB memory block")
    ]
    
    for value, expected, description in test_cases:
        result = power_of_two_validation(value)
        status = "✓" if result == expected else "✗"
        print(f"{status} {value:4d} → {result:5} ({description})")

def test_bit_manipulation_register_ops():
    """Test register bit manipulation operations"""
    print("\nTESTING REGISTER BIT OPERATIONS")
    print("=" * 35)
    
    # Start with a register value
    register = 0b00001010  # Binary: 10 (decimal)
    
    print(f"Initial register:     0b{register:08b} ({register})")
    
    # Set bit 5
    register = set_nth_bit_register(register, 5)
    print(f"After setting bit 5:  0b{register:08b} ({register})")
    
    # Clear bit 1
    register = clear_nth_bit_register(register, 1)
    print(f"After clearing bit 1: 0b{register:08b} ({register})")
    
    # Replace bits 6-4 with value 5 (0b101)
    register = replace_bits_in_register(register, 5, 4, 6)
    print(f"After replacing 6-4:  0b{register:08b} ({register})")

def test_assembly_concepts():
    """Demonstrate assembly language concepts"""
    print("\nASSEMBLY LANGUAGE CONCEPTS")
    print("=" * 30)
    
    # Demonstrate the multiplication algorithm in Python
    def multiply_by_addition(a: int, b: int) -> int:
        """Simulate assembly multiplication using only addition"""
        result = 0
        counter = b
        
        print(f"Calculating {a} * {b} using repeated addition:")
        iteration = 1
        
        while counter > 0:
            result += a
            counter -= 1
            print(f"  Iteration {iteration}: result = {result}, counter = {counter}")
            iteration += 1
        
        return result
    
    # Test multiplication
    a, b = 7, 4
    result = multiply_by_addition(a, b)
    print(f"Final result: {a} * {b} = {result}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("APPLE & NVIDIA POST SILICON VALIDATION INTERVIEW PREP")
    print("=" * 60)
    print("Based on real interview experiences and candidate feedback")
    
    # Run all tests
    test_power_of_two_validation()
    test_bit_manipulation_register_ops()
    assembly_multiply_explanation()
    test_assembly_concepts()
    
    print("\n" + "=" * 60)
    print("🎯 INTERVIEW SUCCESS STRATEGIES:")
    print("✓ Always explain your bit manipulation logic step-by-step")
    print("✓ Connect algorithms to hardware concepts (caches, registers, etc.)")
    print("✓ Show multiple approaches (basic → optimized)")
    print("✓ Demonstrate understanding of assembly/low-level concepts")
    print("✓ Practice explaining complex topics simply")
    print("✓ Know your computer architecture fundamentals")
    
    print("\n🔧 HARDWARE FOCUS AREAS:")
    print("• Cache coherency and memory hierarchies")
    print("• Register design and bit field manipulation")
    print("• Assembly language and instruction sets")
    print("• Memory alignment and addressing")
    print("• Error detection and correction mechanisms")
    print("• Interrupt handling and priority systems")