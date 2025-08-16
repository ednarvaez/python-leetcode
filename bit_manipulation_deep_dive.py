"""
Bit Manipulation Deep Dive for Apple Silicon Validation Engineers
Understanding why bit manipulation is crucial for hardware roles
"""

# ============================================================================
# PART 1: Understanding Binary Representation
# ============================================================================

def show_binary_representations():
    """
    Visualize how numbers look in binary - fundamental for hardware engineers
    """
    print("PART 1: Binary Representation Basics")
    print("=" * 50)
    
    numbers = [1, 2, 4, 8, 16, 32, 3, 5, 7, 15]
    
    print("Decimal | Binary (8-bit) | Explanation")
    print("-" * 50)
    
    for num in numbers:
        binary = format(num, '08b')  # 8-bit binary representation
        if num & (num - 1) == 0 and num > 0:  # Power of 2
            explanation = "Power of 2 - only ONE bit set"
        else:
            explanation = f"NOT power of 2 - {bin(num).count('1')} bits set"
        
        print(f"{num:7} | {binary:10} | {explanation}")

# ============================================================================
# PART 2: Why Powers of 2 Matter in Hardware
# ============================================================================

def explain_powers_of_2_in_hardware():
    """
    Explain why powers of 2 are everywhere in computer hardware
    """
    print("\nPART 2: Powers of 2 in Hardware Design")
    print("=" * 50)
    
    hardware_examples = {
        1: "Single bit flag/enable",
        2: "2-state system (on/off)",
        4: "4-byte word size, 4 cores",
        8: "Byte size (8 bits)",
        16: "16-bit data bus width",
        32: "32-bit registers/addresses",
        64: "64-bit architecture",
        128: "Cache line size",
        256: "Memory page size (often 256B or 4KB)",
        512: "Common buffer sizes",
        1024: "1KB - standard memory unit",
        2048: "2KB - L1 cache size",
        4096: "4KB - standard page size"
    }
    
    print("Power of 2 | Hardware Usage")
    print("-" * 40)
    for power, usage in hardware_examples.items():
        print(f"{power:9} | {usage}")

# ============================================================================
# PART 3: The Magic of n & (n-1)
# ============================================================================

def demonstrate_n_and_n_minus_1():
    """
    Step-by-step demonstration of why n & (n-1) works
    """
    print("\nPART 3: Understanding n & (n-1) - The Hardware Engineer's Tool")
    print("=" * 60)
    
    test_numbers = [1, 2, 4, 8, 16, 3, 6, 7, 12, 15]
    
    print("n   | Binary   | n-1 | Binary(n-1) | n&(n-1) | Binary(result) | Power of 2?")
    print("-" * 75)
    
    for n in test_numbers:
        n_binary = format(n, '08b')
        n_minus_1 = n - 1
        n_minus_1_binary = format(n_minus_1, '08b')
        result = n & (n - 1)
        result_binary = format(result, '08b')
        is_power_of_2 = "YES" if result == 0 and n > 0 else "NO"
        
        print(f"{n:3} | {n_binary} | {n_minus_1:3} | {n_minus_1_binary:11} | {result:7} | {result_binary:12} | {is_power_of_2}")

def explain_the_magic():
    """
    Detailed explanation of WHY n & (n-1) works
    """
    print("\nWHY DOES n & (n-1) WORK?")
    print("=" * 30)
    
    examples = [
        (8, "Power of 2 example"),
        (12, "Not power of 2 example")
    ]
    
    for num, description in examples:
        print(f"\n{description}: n = {num}")
        print(f"n     = {num:3} = {format(num, '08b')}")
        print(f"n-1   = {num-1:3} = {format(num-1, '08b')}")
        print(f"n&(n-1) = {num & (num-1):3} = {format(num & (num-1), '08b')}")
        
        if num & (num - 1) == 0:
            print("Result is 0 → This IS a power of 2!")
            print("Why? Powers of 2 have exactly ONE bit set.")
            print("Subtracting 1 flips all bits to the right of that bit.")
            print("AND-ing them gives 0 because no bits overlap.")
        else:
            print("Result is NOT 0 → This is NOT a power of 2!")
            print("Why? Multiple bits are set, so some remain after AND operation.")

# ============================================================================
# PART 4: Step-by-Step Bit Operations
# ============================================================================

def step_by_step_bit_operations():
    """
    Show each bit operation step by step
    """
    print("\nPART 4: Step-by-Step Bit Operations")
    print("=" * 45)
    
    # Example with 8 (power of 2)
    n = 8
    print(f"Example 1: Testing if {n} is a power of 2")
    print(f"Step 1: n = {n}")
    print(f"        Binary: {format(n, '08b')}")
    print(f"Step 2: n-1 = {n-1}")
    print(f"        Binary: {format(n-1, '08b')}")
    print(f"Step 3: n & (n-1) = {n} & {n-1}")
    print(f"        {format(n, '08b')}")
    print(f"      & {format(n-1, '08b')}")
    print(f"      = {format(n & (n-1), '08b')} = {n & (n-1)}")
    print(f"Step 4: Result is {n & (n-1)}, so {n} {'IS' if n & (n-1) == 0 else 'IS NOT'} a power of 2")
    
    print("\n" + "-" * 40)
    
    # Example with 6 (not power of 2)
    n = 6
    print(f"Example 2: Testing if {n} is a power of 2")
    print(f"Step 1: n = {n}")
    print(f"        Binary: {format(n, '08b')}")
    print(f"Step 2: n-1 = {n-1}")
    print(f"        Binary: {format(n-1, '08b')}")
    print(f"Step 3: n & (n-1) = {n} & {n-1}")
    print(f"        {format(n, '08b')}")
    print(f"      & {format(n-1, '08b')}")
    print(f"      = {format(n & (n-1), '08b')} = {n & (n-1)}")
    print(f"Step 4: Result is {n & (n-1)}, so {n} {'IS' if n & (n-1) == 0 else 'IS NOT'} a power of 2")

# ============================================================================
# PART 5: Hardware Applications
# ============================================================================

def hardware_applications():
    """
    Real-world applications in silicon validation
    """
    print("\nPART 5: Real Hardware Applications")
    print("=" * 40)
    
    print("1. MEMORY ALIGNMENT CHECKING:")
    print("   - Memory addresses must be aligned to power-of-2 boundaries")
    print("   - Example: 64-bit data must start at addresses divisible by 8")
    
    def is_aligned(address, alignment):
        return (address & (alignment - 1)) == 0
    
    addresses = [0x1000, 0x1004, 0x1008, 0x1001]
    alignment = 8  # 8-byte alignment
    
    print(f"\n   Testing {alignment}-byte alignment:")
    print("   Address  | Hex    | Binary     | Aligned?")
    print("   " + "-" * 45)
    
    for addr in addresses:
        binary = format(addr, '012b')
        aligned = is_aligned(addr, alignment)
        print(f"   {addr:7} | 0x{addr:04X} | {binary} | {'YES' if aligned else 'NO'}")
    
    print("\n2. CACHE LINE OPTIMIZATION:")
    print("   - Cache lines are typically 64 bytes (power of 2)")
    print("   - Data structures should align to cache boundaries")
    
    print("\n3. REGISTER BIT FIELD VALIDATION:")
    print("   - Hardware registers often have power-of-2 sized fields")
    print("   - Quick validation of field sizes and positions")

# ============================================================================
# PART 6: Advanced Bit Manipulation Tricks
# ============================================================================

def advanced_bit_tricks():
    """
    Advanced bit manipulation techniques for hardware engineers
    """
    print("\nPART 6: Advanced Bit Manipulation for Hardware")
    print("=" * 50)
    
    print("1. ISOLATE THE RIGHTMOST SET BIT:")
    print("   Formula: n & (-n)")
    
    numbers = [12, 8, 10, 16]
    print("   n   | Binary   | -n       | n&(-n) | Result Binary | Isolated Bit")
    print("   " + "-" * 70)
    
    for n in numbers:
        neg_n = -n & 0xFF  # 8-bit two's complement
        isolated = n & (-n)
        print(f"   {n:3} | {format(n, '08b')} | {format(neg_n, '08b')} | {isolated:6} | {format(isolated, '08b'):11} | Bit {isolated.bit_length()-1}")
    
    print("\n2. TURN OFF THE RIGHTMOST SET BIT:")
    print("   Formula: n & (n-1)  [We already learned this!]")
    
    print("\n3. CHECK IF NUMBER IS POWER OF 4:")
    print("   Formula: n > 0 and (n & (n-1)) == 0 and (n & 0x55555555) != 0")
    print("   Powers of 4 have bits set only at even positions (0, 2, 4, 6...)")
    
    powers_of_4 = [1, 4, 16, 64, 2, 8, 32]
    print("   n   | Power of 2? | Even bit pos? | Power of 4?")
    print("   " + "-" * 50)
    
    for n in powers_of_4:
        is_pow2 = n > 0 and (n & (n-1)) == 0
        is_even_pos = (n & 0x55555555) != 0
        is_pow4 = is_pow2 and is_even_pos
        print(f"   {n:3} | {str(is_pow2):11} | {str(is_even_pos):13} | {str(is_pow4):11}")

# ============================================================================
# PART 7: Interactive Practice
# ============================================================================

def interactive_practice():
    """
    Interactive exercises to reinforce learning
    """
    print("\nPART 7: Practice Exercises")
    print("=" * 35)
    
    exercises = [
        (7, "Not a power of 2 - has multiple bits set"),
        (32, "Power of 2 - only bit 5 is set"),
        (15, "Not a power of 2 - has 4 bits set"),
        (128, "Power of 2 - only bit 7 is set"),
        (100, "Not a power of 2 - multiple bits set")
    ]
    
    print("Try to predict the results before running:")
    print("Number | Your Prediction | Actual Result | n&(n-1) | Explanation")
    print("-" * 75)
    
    for num, explanation in exercises:
        result = num & (num - 1)
        is_power = "Power of 2" if result == 0 and num > 0 else "Not power of 2"
        print(f"{num:6} | {'?':15} | {is_power:13} | {result:7} | {explanation}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("BIT MANIPULATION DEEP DIVE FOR HARDWARE ENGINEERS")
    print("=" * 55)
    
    show_binary_representations()
    explain_powers_of_2_in_hardware()
    demonstrate_n_and_n_minus_1()
    explain_the_magic()
    step_by_step_bit_operations()
    hardware_applications()
    advanced_bit_tricks()
    interactive_practice()
    
    print("\n" + "=" * 55)
    print("KEY TAKEAWAYS:")
    print("1. Powers of 2 have exactly ONE bit set in binary")
    print("2. n & (n-1) removes the rightmost set bit")
    print("3. For powers of 2: n & (n-1) = 0 (no remaining bits)")
    print("4. This technique is O(1) time and space - perfect for hardware")
    print("5. Bit manipulation is fundamental to processor design and validation")
    print("6. Understanding binary operations is crucial for debugging hardware")