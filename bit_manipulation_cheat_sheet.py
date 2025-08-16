"""
BIT MANIPULATION CHEAT SHEET
Quick reference for Apple Silicon Validation interviews
"""

# ============================================================================
# VISUAL EXPLANATION: Why n & (n-1) works for powers of 2
# ============================================================================

def visual_explanation():
    """
    INTERVIEW STRATEGY: Use visual aids to explain bit manipulation
    
    This function demonstrates WHY the n & (n-1) trick works for detecting powers of 2
    Visual explanations help interviewers see your deep understanding
    """
    print("WHY n & (n-1) DETECTS POWERS OF 2")
    print("=" * 40)
    
    print("\n🔍 VISUAL BREAKDOWN:")
    print("\nPowers of 2 have EXACTLY ONE bit set:")
    
    # List of powers of 2 with their binary representations
    examples = [
        (1, "00000001"),   # 2^0
        (2, "00000010"),   # 2^1
        (4, "00000100"),   # 2^2
        (8, "00001000"),   # 2^3
        (16, "00010000")   # 2^4
    ]
    
    # Display each power of 2 and its binary pattern
    for num, binary in examples:
        print(f"  {num:2} = {binary} ← Only ONE bit is 1")
    
    print("\n🧮 THE MAGIC HAPPENS HERE:")
    print("\nWhen you subtract 1 from a power of 2:")
    print("- All bits to the RIGHT of the set bit become 1")
    print("- The set bit becomes 0") 
    print("- All bits to the LEFT stay 0")
    
    # Detailed walkthrough with n = 8
    n = 8
    print(f"\nExample with {n}:")
    # Show original number in binary
    print(f"  n     = {n}   = {format(n, '08b')}")
    
    # Show n-1 in binary (notice how bits flip)
    print(f"  n-1   = {n-1}   = {format(n-1, '08b')} ← Notice the pattern!")
    
    # Show the AND operation result
    print(f"  n&(n-1) = {n&(n-1)}   = {format(n&(n-1), '08b')} ← AND gives 0!")
    
    print("\n💡 KEY INSIGHT:")
    print("When you AND a power of 2 with (itself - 1):")
    print("- The single '1' bit ANDs with '0' → gives 0")
    print("- All the '0' bits AND with '1' → gives 0") 
    print("- Result is always 0 for powers of 2!")
    
    print("\n❌ COUNTER-EXAMPLE (not power of 2):")
    # Show why non-powers of 2 don't work
    n = 6  # 6 = 4 + 2, so has multiple bits set
    print(f"  n     = {n}   = {format(n, '08b')} ← Multiple bits set")
    print(f"  n-1   = {n-1}   = {format(n-1, '08b')}")
    print(f"  n&(n-1) = {n&(n-1)}   = {format(n&(n-1), '08b')} ← Still has bits!")

# ============================================================================
# COMMON BIT MANIPULATION PATTERNS FOR HARDWARE
# ============================================================================

def bit_manipulation_patterns():
    """
    HARDWARE VALIDATION TOOLKIT: Essential bit manipulation patterns
    
    These patterns are the building blocks for register manipulation,
    error detection, and performance optimization in silicon validation
    """
    print("\n\nESSENTIAL BIT PATTERNS FOR HARDWARE VALIDATION")
    print("=" * 55)
    
    # Core patterns every hardware engineer should know
    patterns = [
        ("Check if power of 2", "n > 0 and (n & (n-1)) == 0", [1,2,4,8,3,6]),
        ("Get rightmost set bit", "n & (-n)", [12, 8, 10]),
        ("Turn off rightmost set bit", "n & (n-1)", [12, 8, 10]),
        ("Check if bit N is set", "n & (1 << N)", [5, 8, 12]),
        ("Set bit N", "n | (1 << N)", [5, 8, 12]),
        ("Clear bit N", "n & ~(1 << N)", [5, 8, 12]),
        ("Toggle bit N", "n ^ (1 << N)", [5, 8, 12]),
        ("Count set bits", "bin(n).count('1')", [7, 15, 31])
    ]
    
    # Demonstrate each pattern with examples
    for operation, formula, test_nums in patterns:
        print(f"\n📋 {operation.upper()}:")
        print(f"   Formula: {formula}")
        print("   Examples:")
        
        # Show first 3 test cases for each pattern
        for num in test_nums[:3]:
            
            # Power of 2 check: validate if number has exactly one bit set
            if operation == "Check if power of 2":
                result = num > 0 and (num & (num-1)) == 0
                print(f"     {num:2} → {result} (binary: {format(num, '08b')})")
                
            # Rightmost set bit: isolate the lowest 1 bit using two's complement
            elif operation == "Get rightmost set bit":
                result = num & (-num)  # -num is two's complement: flip bits + 1
                print(f"     {num:2} → {result} (binary: {format(num, '08b')} → {format(result, '08b')})")
                
            # Turn off rightmost set bit: remove the lowest 1 bit
            elif operation == "Turn off rightmost set bit":
                result = num & (num-1)  # Same trick as power of 2 detection
                print(f"     {num:2} → {result} (binary: {format(num, '08b')} → {format(result, '08b')})")

# ============================================================================
# HARDWARE-SPECIFIC APPLICATIONS
# ============================================================================

def hardware_applications():
    """
    Real-world silicon validation applications
    """
    print("\n\nHARDWARE VALIDATION APPLICATIONS")
    print("=" * 40)
    
    print("🔧 REGISTER VALIDATION:")
    print("   - Check if register size is power of 2")
    print("   - Validate bit field alignments")
    print("   - Test register reset values")
    
    print("\n🧠 MEMORY TESTING:")
    print("   - Verify cache line sizes (64, 128, 256 bytes)")
    print("   - Check memory alignment requirements")
    print("   - Validate page sizes (4KB, 2MB, 1GB)")
    
    print("\n⚡ PERFORMANCE OPTIMIZATION:")
    print("   - Powers of 2 enable fast division/multiplication")
    print("   - Bit shifts instead of arithmetic operations")
    print("   - Efficient memory addressing")
    
    print("\n🐛 ERROR DETECTION:")
    print("   - XOR for parity checking")
    print("   - Hamming codes using bit manipulation")
    print("   - Single bit error correction")

# ============================================================================
# PRACTICE PROBLEMS
# ============================================================================

def practice_problems():
    """
    Practice problems specifically for hardware validation roles
    """
    print("\n\nPRACTICE PROBLEMS FOR APPLE INTERVIEWS")
    print("=" * 45)
    
    problems = [
        {
            "problem": "Given a 32-bit register value, check if it represents a valid cache line size",
            "solution": "return n > 0 and (n & (n-1)) == 0 and n >= 16",
            "test_cases": [16, 32, 64, 128, 15, 33]
        },
        {
            "problem": "Count number of enabled interrupt bits in a status register",
            "solution": "return bin(n).count('1')",
            "test_cases": [0b10101010, 0b11110000, 0b00000001]
        },
        {
            "problem": "Check if memory address is aligned to N-byte boundary",
            "solution": "return (address & (alignment - 1)) == 0",
            "test_cases": [(0x1000, 8), (0x1004, 8), (0x1008, 8)]
        }
    ]
    
    for i, prob in enumerate(problems, 1):
        print(f"\n🎯 PROBLEM {i}:")
        print(f"   {prob['problem']}")
        print(f"   Solution pattern: {prob['solution']}")
        print("   Test cases:")
        
        for case in prob['test_cases'][:3]:
            if isinstance(case, tuple):
                print(f"     {case}")
            else:
                print(f"     {case} (0b{format(case, '08b')})")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    visual_explanation()
    bit_manipulation_patterns()
    hardware_applications()
    practice_problems()
    
    print("\n\n🎓 INTERVIEW SUCCESS TIPS:")
    print("=" * 30)
    print("1. Always explain your bit manipulation logic step-by-step")
    print("2. Draw binary representations when solving problems")
    print("3. Connect bit operations to hardware concepts")
    print("4. Practice timing complexity analysis (most bit ops are O(1))")
    print("5. Know when to use bit manipulation vs. arithmetic operations")