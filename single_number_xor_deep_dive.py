"""
SINGLE NUMBER (XOR) DEEP DIVE
Critical XOR applications for Apple Silicon Validation
"""

# ============================================================================
# PART 1: Understanding XOR in Hardware Context
# ============================================================================

def explain_xor_fundamentals():
    """
    XOR fundamentals and why it's crucial for hardware validation
    """
    print("XOR FUNDAMENTALS FOR HARDWARE ENGINEERS")
    print("=" * 45)
    
    print("🔍 XOR TRUTH TABLE:")
    print("A | B | A⊕B | Meaning")
    print("--|---|-----|--------")
    print("0 | 0 |  0  | Same inputs → 0")
    print("0 | 1 |  1  | Different inputs → 1") 
    print("1 | 0 |  1  | Different inputs → 1")
    print("1 | 1 |  0  | Same inputs → 0")
    
    print("\n💡 KEY XOR PROPERTIES:")
    properties = [
        ("Self-cancellation", "a ⊕ a = 0", "Any number XOR with itself = 0"),
        ("Identity", "a ⊕ 0 = a", "XOR with 0 leaves number unchanged"),
        ("Commutative", "a ⊕ b = b ⊕ a", "Order doesn't matter"),
        ("Associative", "(a⊕b)⊕c = a⊕(b⊕c)", "Grouping doesn't matter"),
        ("Involution", "a ⊕ b ⊕ b = a", "Double XOR cancels out")
    ]
    
    for name, formula, explanation in properties:
        print(f"  • {name:15}: {formula:12} - {explanation}")

def hardware_applications_xor():
    """
    Why XOR is everywhere in computer hardware
    """
    print("\n\nXOR IN SILICON VALIDATION & HARDWARE")
    print("=" * 40)
    
    applications = [
        "🔧 ERROR DETECTION: Parity bits, checksums, ECC codes",
        "🔒 ENCRYPTION: XOR ciphers, stream ciphers, AES",
        "🧠 MEMORY TESTING: Pattern generation, data integrity",
        "⚡ POWER ANALYSIS: Toggle rate calculation (switching activity)",
        "🎯 LFSR GENERATORS: Pseudo-random test pattern generation",
        "📊 DIFFERENTIAL ANALYSIS: Compare expected vs actual results",
        "🔄 FAULT INJECTION: Simulate bit-flip errors",
        "🚀 HASH FUNCTIONS: Core component of hash algorithms"
    ]
    
    for app in applications:
        print(f"  {app}")
    
    print("\n🎯 APPLE SILICON SPECIFIC USES:")
    apple_uses = [
        "Neural Engine validation: Weight corruption detection",
        "Secure Enclave: Key derivation and encryption",
        "Memory controller: Error correction codes (ECC)",
        "GPU validation: Texture compression error detection",
        "Power management: Activity monitoring via XOR patterns"
    ]
    
    for use in apple_uses:
        print(f"  • {use}")

# ============================================================================
# PART 2: Single Number Problem Deep Dive
# ============================================================================

def single_number_algorithm():
    """
    Step-by-step breakdown of the single number algorithm
    """
    print("\n\nSINGLE NUMBER ALGORITHM BREAKDOWN")
    print("=" * 40)
    
    print("🎯 PROBLEM: Find the number that appears once in array where all others appear twice")
    print("💡 SOLUTION: XOR all numbers - duplicates cancel out!")
    
    def find_single_with_steps(nums):
        """Show each XOR step"""
        print(f"\nFinding single number in: {nums}")
        result = 0
        
        print("Step | Current | Next | XOR Result | Binary Visualization")
        print("-" * 65)
        
        for i, num in enumerate(nums):
            old_result = result
            result ^= num
            print(f"{i+1:4} | {old_result:7} | {num:4} | {result:10} | {format(old_result, '08b')} ⊕ {format(num, '08b')} = {format(result, '08b')}")
        
        print(f"\nSingle number found: {result}")
        return result
    
    # Test cases with step-by-step analysis
    test_cases = [
        [2, 2, 1],
        [4, 1, 2, 1, 2],
        [7, 3, 5, 4, 5, 3, 4]
    ]
    
    for nums in test_cases:
        find_single_with_steps(nums)

def xor_cancellation_visualization():
    """
    Visual demonstration of how XOR cancellation works
    """
    print("\n\nXOR CANCELLATION VISUALIZATION")
    print("=" * 35)
    
    print("🔍 WHY DUPLICATES CANCEL OUT:")
    
    # Example: [4, 1, 2, 1, 2] - find single number 4
    nums = [4, 1, 2, 1, 2]
    print(f"Array: {nums}")
    print("Rearranging to show pairs: [1, 1, 2, 2, 4]")
    
    print("\nXOR Process:")
    print("  1 ⊕ 1 = 0  (first pair cancels)")
    print("  2 ⊕ 2 = 0  (second pair cancels)")
    print("  0 ⊕ 0 = 0  (canceled pairs)")
    print("  0 ⊕ 4 = 4  (single number remains)")
    
    print("\n🧮 BIT-LEVEL ANALYSIS:")
    unique_nums = list(set(nums))
    print("Number | Binary   | Appears | Contribution to Final XOR")
    print("-" * 55)
    
    for num in unique_nums:
        count = nums.count(num)
        binary = format(num, '08b')
        if count % 2 == 0:
            contribution = "Cancels out (even count)"
        else:
            contribution = f"Remains (odd count) → {binary}"
        print(f"{num:6} | {binary} | {count:7} | {contribution}")

# ============================================================================
# PART 3: Advanced XOR Problems
# ============================================================================

def advanced_xor_problems():
    """
    More complex XOR problems for Apple interviews
    """
    print("\n\nADVANCED XOR PROBLEMS")
    print("=" * 25)
    
    print("🎯 PROBLEM 1: Single Number II")
    print("Every element appears 3 times except one (appears once)")
    
    def single_number_ii(nums):
        """Use bit manipulation for elements appearing 3 times"""
        ones = twos = 0
        
        print(f"Finding single in array where others appear 3x: {nums}")
        print("Using two variables to track bit states:")
        print("Step | Number | Ones     | Twos     | Explanation")
        print("-" * 55)
        
        for i, num in enumerate(nums):
            old_ones, old_twos = ones, twos
            
            # Update ones and twos
            twos |= ones & num  # Bits that appeared twice
            ones ^= num         # Bits that appeared once
            
            # Remove bits that appeared three times
            common = ones & twos
            ones &= ~common
            twos &= ~common
            
            print(f"{i+1:4} | {num:6} | {format(ones, '08b')} | {format(twos, '08b')} | Tracking bit occurrences")
        
        return ones
    
    # Test case: [2, 2, 3, 2] - answer is 3
    result = single_number_ii([2, 2, 3, 2])
    print(f"Single number (appears once): {result}")
    
    print("\n🎯 PROBLEM 2: Single Number III")
    print("Two numbers appear once, all others appear twice")
    
    def single_number_iii(nums):
        """Find two numbers that appear once"""
        # XOR all numbers - result is XOR of the two unique numbers
        xor_all = 0
        for num in nums:
            xor_all ^= num
        
        # Find rightmost set bit to distinguish the two numbers
        rightmost_bit = xor_all & (-xor_all)
        
        num1 = num2 = 0
        for num in nums:
            if num & rightmost_bit:
                num1 ^= num
            else:
                num2 ^= num
        
        return [num1, num2]
    
    # Test case: [1, 2, 1, 3, 2, 5] - answer is [3, 5]
    result = single_number_iii([1, 2, 1, 3, 2, 5])
    print(f"Two single numbers: {result}")

# ============================================================================
# PART 4: XOR in Error Detection & Correction
# ============================================================================

def xor_error_detection():
    """
    XOR applications in error detection and correction
    """
    print("\n\nXOR IN ERROR DETECTION & CORRECTION")
    print("=" * 40)
    
    print("🔧 PARITY BIT CALCULATION:")
    
    def calculate_parity(data_bits):
        """Calculate even parity bit using XOR"""
        parity = 0
        for bit in data_bits:
            parity ^= bit
        return parity
    
    # Example: 7-bit ASCII 'A' = 1000001
    ascii_A = [1, 0, 0, 0, 0, 0, 1]
    parity = calculate_parity(ascii_A)
    
    print(f"Data bits for 'A': {ascii_A}")
    print(f"Parity bit (even): {parity}")
    print(f"Complete 8-bit word: {ascii_A + [parity]}")
    
    print("\n🛡️ ERROR DETECTION DEMO:")
    
    def detect_single_bit_error(received_bits):
        """Detect single bit error using parity"""
        total_parity = 0
        for bit in received_bits:
            total_parity ^= bit
        
        if total_parity == 0:
            return "No error detected"
        else:
            return "Single bit error detected!"
    
    # Test error detection
    original = [1, 0, 0, 0, 0, 0, 1, 1]  # 'A' with parity
    corrupted = [1, 0, 0, 0, 1, 0, 1, 1]  # Bit 4 flipped
    
    print(f"Original:  {original} → {detect_single_bit_error(original)}")
    print(f"Corrupted: {corrupted} → {detect_single_bit_error(corrupted)}")
    
    print("\n🔬 HAMMING CODE EXAMPLE:")
    print("Hamming codes use XOR for both detection and correction")
    
    def hamming_syndrome(received):
        """Calculate Hamming syndrome using XOR"""
        # Simplified 7-bit Hamming code
        h1 = received[0] ^ received[2] ^ received[4] ^ received[6]  # Parity bit 1
        h2 = received[1] ^ received[2] ^ received[5] ^ received[6]  # Parity bit 2  
        h4 = received[3] ^ received[4] ^ received[5] ^ received[6]  # Parity bit 4
        
        syndrome = h4 * 4 + h2 * 2 + h1
        return syndrome
    
    # Example with single bit error
    received_data = [0, 0, 1, 0, 1, 0, 1]  # Hamming(7,4) code
    syndrome = hamming_syndrome(received_data)
    
    print(f"Received: {received_data}")
    print(f"Syndrome: {syndrome} → {'No error' if syndrome == 0 else f'Error at position {syndrome}'}")

# ============================================================================
# PART 5: Hardware Implementation Details
# ============================================================================

def hardware_implementation_xor():
    """
    How XOR is implemented in actual hardware
    """
    print("\n\nXOR HARDWARE IMPLEMENTATION")
    print("=" * 35)
    
    print("⚡ GATE-LEVEL IMPLEMENTATION:")
    print("XOR = (A AND NOT B) OR (NOT A AND B)")
    print("Transistor count: 8 transistors for CMOS XOR gate")
    
    print("\n🚀 SILICON OPTIMIZATIONS:")
    optimizations = [
        "Parallel XOR: Multiple bits processed simultaneously",
        "Tree structures: Reduce XOR chain delay",
        "Lookup tables: Fast XOR for small bit widths",
        "Dedicated XOR units: In cryptographic accelerators"
    ]
    
    for opt in optimizations:
        print(f"  • {opt}")
    
    print("\n📊 PERFORMANCE CHARACTERISTICS:")
    print("  • Propagation delay: ~0.1-0.3ns in modern process")
    print("  • Power consumption: Low (complementary switching)")
    print("  • Area overhead: Minimal for basic XOR operations")
    print("  • Scalability: Excellent for wide data paths")

# ============================================================================
# PART 6: Apple Interview Problems
# ============================================================================

def apple_interview_xor_problems():
    """
    XOR problems specific to Apple Silicon validation
    """
    print("\n\nAPPLE SILICON VALIDATION XOR PROBLEMS")
    print("=" * 45)
    
    problems = [
        {
            "title": "Neural Engine Weight Validation",
            "problem": "Detect corrupted weights in neural network by comparing checksums",
            "solution": "XOR all weights, compare with stored checksum",
            "code": "checksum_valid = (computed_xor == stored_checksum)"
        },
        {
            "title": "GPU Texture Compression Verification", 
            "problem": "Verify texture data integrity after compression/decompression",
            "solution": "XOR original and decompressed data to find differences",
            "code": "error_mask = original_texture ^ decompressed_texture"
        },
        {
            "title": "Secure Enclave Key Derivation",
            "problem": "Generate derived keys from master key using XOR operations",
            "solution": "Use XOR in key stretching and derivation functions",
            "code": "derived_key = master_key ^ hash(salt + counter)"
        },
        {
            "title": "Memory Controller ECC Validation",
            "problem": "Implement single-bit error correction using Hamming codes",
            "solution": "Use XOR to calculate syndrome and locate errors",
            "code": "error_position = syndrome_bit1 ^ syndrome_bit2 ^ syndrome_bit4"
        }
    ]
    
    for i, prob in enumerate(problems, 1):
        print(f"\n🎯 PROBLEM {i}: {prob['title']}")
        print(f"   Challenge: {prob['problem']}")
        print(f"   Approach: {prob['solution']}")
        print(f"   Code: {prob['code']}")

# ============================================================================
# PART 7: Practice Exercises
# ============================================================================

def practice_exercises_xor():
    """
    Hands-on XOR exercises
    """
    print("\n\nXOR PRACTICE EXERCISES")
    print("=" * 25)
    
    exercises = [
        {
            "problem": "Swap two variables without temporary variable",
            "hint": "Use XOR properties: a^=b; b^=a; a^=b;",
            "test": "a=5, b=7"
        },
        {
            "problem": "Find missing number in array [0,1,2,...,n] with one missing",
            "hint": "XOR all numbers 0 to n, then XOR with array elements",
            "test": "[0,1,3,4,5] missing 2"
        },
        {
            "problem": "Check if two strings are anagrams using XOR",
            "hint": "XOR all characters - anagrams will result in 0",
            "test": "'listen' and 'silent'"
        },
        {
            "problem": "Generate Gray code sequence using XOR",
            "hint": "Gray[i] = i ^ (i >> 1)",
            "test": "Generate 4-bit Gray code"
        }
    ]
    
    print("💪 Try these problems:")
    for i, ex in enumerate(exercises, 1):
        print(f"\n📝 EXERCISE {i}:")
        print(f"   Problem: {ex['problem']}")
        print(f"   Hint: {ex['hint']}")
        print(f"   Test case: {ex['test']}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("XOR MASTERY FOR APPLE SILICON VALIDATION")
    print("=" * 45)
    
    explain_xor_fundamentals()
    hardware_applications_xor()
    single_number_algorithm()
    xor_cancellation_visualization()
    advanced_xor_problems()
    xor_error_detection()
    hardware_implementation_xor()
    apple_interview_xor_problems()
    practice_exercises_xor()
    
    print("\n" + "=" * 45)
    print("🎓 XOR MASTERY CHECKLIST:")
    print("✓ Understand XOR truth table and properties")
    print("✓ Master single number problem variations")
    print("✓ Know XOR applications in error detection")
    print("✓ Understand hardware implementation details")
    print("✓ Practice XOR-based algorithms and optimizations")
    print("✓ Connect XOR to real silicon validation scenarios")