"""
HAMMING WEIGHT (Count 1s) DEEP DIVE
Critical for Apple Silicon Validation - Understanding bit counting algorithms
"""

# ============================================================================
# PART 1: Understanding Hamming Weight
# ============================================================================

def explain_hamming_weight():
    """
    What is Hamming Weight and why it matters in hardware validation
    """
    print("HAMMING WEIGHT FUNDAMENTALS")
    print("=" * 35)
    
    print("🔍 DEFINITION:")
    print("Hamming Weight = Number of '1' bits in binary representation")
    print("Named after Richard Hamming (error-correcting codes)")
    
    print("\n📊 EXAMPLES:")
    examples = [
        (7, "00000111", "3 ones - common in 3-bit counters"),
        (15, "00001111", "4 ones - nibble (half-byte) full"),
        (31, "00011111", "5 ones - often seen in 5-bit fields"),
        (255, "11111111", "8 ones - full byte"),
        (5, "00000101", "2 ones - sparse bit pattern"),
        (0, "00000000", "0 ones - empty register")
    ]
    
    print("Number | Binary   | Hamming Weight | Hardware Context")
    print("-" * 60)
    for num, binary, weight, context in examples:
        hamming = bin(num).count('1')
        print(f"{num:6} | {binary} | {hamming:13} | {context}")

def hardware_importance():
    """
    Why Hamming Weight is crucial in silicon validation
    """
    print("\n\nWHY HAMMING WEIGHT MATTERS IN HARDWARE")
    print("=" * 45)
    
    applications = [
        "🔧 ERROR DETECTION: Parity bits, ECC codes",
        "⚡ POWER ANALYSIS: More 1s = higher power consumption",
        "🧠 CACHE VALIDATION: Track dirty bits, valid bits",
        "📊 PERFORMANCE COUNTERS: Count active units/cores",
        "🔒 SECURITY: Detect bit-flip attacks",
        "🎯 TEST PATTERNS: Generate specific bit densities",
        "📡 SIGNAL INTEGRITY: Analyze switching activity"
    ]
    
    for app in applications:
        print(f"  {app}")

# ============================================================================
# PART 2: Algorithm Comparison
# ============================================================================

def algorithm_comparison():
    """
    Compare different approaches to count 1s
    """
    print("\n\nALGORITHM COMPARISON")
    print("=" * 25)
    
    def naive_approach(n):
        """Convert to string and count - O(log n) time, O(log n) space"""
        return bin(n).count('1')
    
    def bit_shift_approach(n):
        """Shift and check each bit - O(32) time for 32-bit"""
        count = 0
        while n:
            count += n & 1
            n >>= 1
        return count
    
    def kernighan_approach(n):
        """Brian Kernighan's algorithm - O(number of set bits)"""
        count = 0
        while n:
            count += 1
            n &= (n - 1)  # Remove rightmost set bit
        return count
    
    def lookup_table_approach(n):
        """Precomputed lookup table - O(1) for small numbers"""
        # For demonstration - real implementation would use larger table
        table = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]
        if n < 16:
            return table[n]
        return bin(n).count('1')  # Fallback
    
    test_numbers = [7, 15, 31, 85, 170, 255]
    
    print("Method Comparison (Time Complexity):")
    print("Number | Naive O(log n) | Shift O(32) | Kernighan O(bits) | Lookup O(1)")
    print("-" * 75)
    
    for num in test_numbers:
        naive = naive_approach(num)
        shift = bit_shift_approach(num)
        kernighan = kernighan_approach(num)
        lookup = lookup_table_approach(num)
        
        print(f"{num:6} | {naive:13} | {shift:10} | {kernighan:16} | {lookup:10}")

# ============================================================================
# PART 3: Brian Kernighan's Algorithm Deep Dive
# ============================================================================

def kernighan_deep_dive():
    """
    Step-by-step explanation of the optimal algorithm
    """
    print("\n\nBRIAN KERNIGHAN'S ALGORITHM DEEP DIVE")
    print("=" * 45)
    
    print("🧮 THE MAGIC: n & (n-1) removes the rightmost set bit")
    print("⚡ EFFICIENCY: Only loops for the number of set bits!")
    
    def kernighan_with_steps(n):
        """Show each step of the algorithm"""
        original = n
        count = 0
        steps = []
        
        print(f"\nCounting 1s in {original} = {format(original, '08b')}")
        print("Step | n        | Binary   | n-1      | n&(n-1)  | Count")
        print("-" * 60)
        
        step = 0
        while n:
            n_minus_1 = n - 1
            new_n = n & (n - 1)
            count += 1
            steps.append((step, n, format(n, '08b'), n_minus_1, format(new_n, '08b'), count))
            print(f"{step:4} | {n:8} | {format(n, '08b')} | {n_minus_1:8} | {format(new_n, '08b')} | {count:5}")
            n = new_n
            step += 1
        
        print(f"\nFinal count: {count}")
        return count
    
    # Demonstrate with different numbers
    test_cases = [7, 12, 15]
    for num in test_cases:
        kernighan_with_steps(num)

def visual_bit_removal():
    """
    Visual demonstration of bit removal
    """
    print("\n\nVISUAL BIT REMOVAL DEMONSTRATION")
    print("=" * 40)
    
    n = 12  # 1100 in binary
    print(f"Starting with n = {n} = {format(n, '08b')}")
    
    iteration = 1
    while n:
        print(f"\nIteration {iteration}:")
        print(f"  Current n:     {format(n, '08b')}")
        print(f"  n - 1:         {format(n-1, '08b')}")
        print(f"  n & (n-1):     {format(n & (n-1), '08b')} ← Rightmost '1' removed!")
        
        n &= (n - 1)
        iteration += 1
    
    print(f"\nResult: n = {n} = {format(n, '08b')} (all bits removed)")

# ============================================================================
# PART 4: Hardware Implementation Insights
# ============================================================================

def hardware_implementation():
    """
    How this algorithm maps to actual hardware
    """
    print("\n\nHARDWARE IMPLEMENTATION INSIGHTS")
    print("=" * 40)
    
    print("🔧 SILICON IMPLEMENTATION:")
    print("  • Each n & (n-1) operation is a single AND gate cycle")
    print("  • Can be parallelized with population count (POPCNT) instructions")
    print("  • Modern CPUs have dedicated POPCNT hardware")
    
    print("\n⚡ PERFORMANCE CHARACTERISTICS:")
    print("  • Best case: O(1) for powers of 2 (only 1 bit set)")
    print("  • Worst case: O(log n) for numbers like 2^n - 1 (all bits set)")
    print("  • Average case: O(log n / 2) for random bit patterns")
    
    print("\n🎯 VALIDATION APPLICATIONS:")
    validation_examples = [
        ("Register bit counting", "Count active interrupt enables"),
        ("Error syndrome analysis", "Count error bits in ECC"),
        ("Power estimation", "Estimate switching activity"),
        ("Test coverage", "Count tested bit combinations"),
        ("Mask validation", "Verify bit mask density")
    ]
    
    for application, description in validation_examples:
        print(f"  • {application}: {description}")

# ============================================================================
# PART 5: Advanced Techniques
# ============================================================================

def advanced_techniques():
    """
    Advanced bit counting techniques for high-performance scenarios
    """
    print("\n\nADVANCED BIT COUNTING TECHNIQUES")
    print("=" * 40)
    
    print("🚀 PARALLEL BIT COUNTING (Divide & Conquer):")
    print("Used in hardware POPCNT instructions")
    
    def parallel_bit_count_8bit(n):
        """Demonstrate parallel counting for 8-bit numbers"""
        print(f"\nParallel counting for {n} = {format(n, '08b')}")
        
        # Step 1: Count bits in pairs
        n = (n & 0x55) + ((n >> 1) & 0x55)  # 0x55 = 01010101
        print(f"After pair counting:   {format(n, '08b')} (each 2-bit field has count)")
        
        # Step 2: Count 2-bit sums in 4-bit groups  
        n = (n & 0x33) + ((n >> 2) & 0x33)  # 0x33 = 00110011
        print(f"After 4-bit grouping:  {format(n, '08b')} (each 4-bit field has count)")
        
        # Step 3: Count 4-bit sums in 8-bit result
        n = (n & 0x0F) + ((n >> 4) & 0x0F)  # 0x0F = 00001111
        print(f"Final 8-bit result:    {format(n, '08b')} (total count in lower 4 bits)")
        
        return n
    
    # Demonstrate with example
    test_num = 0b10110101  # 181 in decimal
    result = parallel_bit_count_8bit(test_num)
    print(f"Total 1s: {result}")
    
    print("\n🎯 LOOKUP TABLE METHOD:")
    print("Precompute counts for all possible byte values")
    
    # Generate lookup table for 4-bit values (demonstration)
    lookup_4bit = [bin(i).count('1') for i in range(16)]
    print("4-bit lookup table:", lookup_4bit)
    
    def lookup_method(n):
        """Use lookup table for fast counting"""
        count = 0
        while n:
            count += lookup_4bit[n & 0xF]  # Count low 4 bits
            n >>= 4
        return count
    
    print(f"\nUsing lookup for {test_num}: {lookup_method(test_num)} ones")

# ============================================================================
# PART 6: Apple Interview Problems
# ============================================================================

def apple_interview_problems():
    """
    Specific problems Apple might ask about bit counting
    """
    print("\n\nAPPLE SILICON VALIDATION INTERVIEW PROBLEMS")
    print("=" * 50)
    
    problems = [
        {
            "title": "Power Consumption Estimation",
            "problem": "Given a 32-bit instruction, estimate relative power consumption based on bit density",
            "solution": "Higher Hamming weight = more transistor switching = higher power",
            "code": "power_factor = hamming_weight(instruction) / 32.0"
        },
        {
            "title": "ECC Syndrome Analysis", 
            "problem": "Determine if an error syndrome indicates single or multi-bit error",
            "solution": "Single-bit error has Hamming weight = 1, multi-bit has weight > 1",
            "code": "is_single_bit_error = hamming_weight(syndrome) == 1"
        },
        {
            "title": "Cache Line Validation",
            "problem": "Count dirty bits in a cache line to decide write-back strategy",
            "solution": "Use bit counting to determine if partial or full write-back",
            "code": "dirty_count = hamming_weight(dirty_mask)"
        },
        {
            "title": "Interrupt Priority Encoding",
            "problem": "Find highest priority interrupt from a bit vector",
            "solution": "Combine bit counting with bit scanning",
            "code": "highest = 31 - leading_zeros(interrupt_vector)"
        }
    ]
    
    for i, prob in enumerate(problems, 1):
        print(f"\n🎯 PROBLEM {i}: {prob['title']}")
        print(f"   Question: {prob['problem']}")
        print(f"   Solution: {prob['solution']}")
        print(f"   Code: {prob['code']}")

# ============================================================================
# PART 7: Practice Exercises
# ============================================================================

def practice_exercises():
    """
    Hands-on exercises to master the concept
    """
    print("\n\nPRACTICE EXERCISES")
    print("=" * 20)
    
    exercises = [
        {
            "problem": "Count 1s without using built-in functions",
            "input": [7, 15, 255, 0, 1],
            "hint": "Use n & (n-1) technique"
        },
        {
            "problem": "Find number with odd number of 1s in array",
            "input": [[1, 2, 3, 4, 5], [7, 15, 31, 127]],
            "hint": "Check hamming_weight(n) % 2"
        },
        {
            "problem": "Determine minimum bit flips to transform A to B",
            "input": [(5, 3), (10, 15), (0, 7)],
            "hint": "Count 1s in A XOR B"
        }
    ]
    
    print("Try solving these problems:")
    for i, ex in enumerate(exercises, 1):
        print(f"\n📝 EXERCISE {i}:")
        print(f"   Problem: {ex['problem']}")
        print(f"   Test input: {ex['input']}")
        print(f"   Hint: {ex['hint']}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("HAMMING WEIGHT MASTERY FOR APPLE SILICON VALIDATION")
    print("=" * 55)
    
    explain_hamming_weight()
    hardware_importance()
    algorithm_comparison()
    kernighan_deep_dive()
    visual_bit_removal()
    hardware_implementation()
    advanced_techniques()
    apple_interview_problems()
    practice_exercises()
    
    print("\n" + "=" * 55)
    print("🎓 KEY TAKEAWAYS:")
    print("1. Hamming weight = count of 1 bits (critical for hardware)")
    print("2. Brian Kernighan's algorithm: n & (n-1) removes rightmost 1")
    print("3. Time complexity: O(number of set bits) - very efficient")
    print("4. Hardware applications: power, error detection, validation")
    print("5. Modern CPUs have dedicated POPCNT instructions")
    print("6. Essential for Apple silicon validation roles!")