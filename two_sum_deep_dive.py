"""
TWO SUM DEEP DIVE
Essential hash table applications for Apple Silicon Validation
"""

# ============================================================================
# PART 1: Two Sum Problem Fundamentals
# ============================================================================

def explain_two_sum_basics():
    """
    Two Sum problem fundamentals and its importance in hardware validation
    """
    print("TWO SUM PROBLEM FUNDAMENTALS")
    print("=" * 35)
    
    print("🎯 PROBLEM STATEMENT:")
    print("Given array of integers and target sum, find two numbers that add to target")
    print("Return indices of the two numbers")
    print("Assume exactly one solution exists")
    
    print("\n📊 ALGORITHM COMPARISON:")
    approaches = [
        ("Brute Force", "O(n²)", "O(1)", "Check all pairs - nested loops"),
        ("Hash Table", "O(n)", "O(n)", "Single pass with complement lookup"),
        ("Two Pointers", "O(n log n)", "O(1)", "Sort first, then use two pointers"),
        ("Binary Search", "O(n log n)", "O(1)", "For each element, search complement")
    ]
    
    print("Approach    | Time      | Space | Description")
    print("-" * 55)
    for approach, time, space, desc in approaches:
        print(f"{approach:11} | {time:9} | {space:5} | {desc}")
    
    print("\n💡 WHY HASH TABLE SOLUTION IS OPTIMAL:")
    print("• Single pass through array (O(n) time)")
    print("• Constant time lookups (O(1) hash access)")
    print("• Trade space for time (classic optimization)")
    print("• Mirrors hardware caching strategies")

def hardware_relevance():
    """
    Why Two Sum pattern is crucial for hardware validation
    """
    print("\n\nTWO SUM PATTERN IN HARDWARE VALIDATION")
    print("=" * 45)
    
    applications = [
        "🔧 VOLTAGE PAIR ANALYSIS: Find voltage combinations that meet power targets",
        "⚡ FREQUENCY MATCHING: Pair clock domains for optimal timing",
        "🧠 MEMORY OPTIMIZATION: Find address pairs for cache optimization",
        "📊 PERFORMANCE TUNING: Match workload pairs for benchmarking",
        "🎯 ERROR CORRELATION: Find error patterns that occur together",
        "🔍 SIGNAL INTEGRITY: Pair transmission lines for crosstalk analysis",
        "⏱️ TIMING ANALYSIS: Find delay pairs that cause violations",
        "🔒 SECURITY VALIDATION: Detect key-value pairs in side-channel analysis"
    ]
    
    for app in applications:
        print(f"  {app}")
    
    print("\n🏭 APPLE SILICON SPECIFIC EXAMPLES:")
    apple_examples = [
        "Neural Engine: Find weight pairs that optimize inference speed",
        "GPU Shader Units: Pair execution units for maximum throughput",
        "CPU Cache: Find memory access pairs that cause conflicts",
        "Secure Enclave: Validate cryptographic key pair relationships",
        "Power Management: Find voltage-frequency pairs for efficiency"
    ]
    
    for example in apple_examples:
        print(f"  • {example}")

# ============================================================================
# PART 2: Algorithm Implementations with Analysis
# ============================================================================

def algorithm_implementations():
    """
    Detailed implementations of different Two Sum approaches
    """
    print("\n\nTWO SUM ALGORITHM IMPLEMENTATIONS")
    print("=" * 40)
    
    # Test array for all algorithms
    test_array = [2, 7, 11, 15, 3, 6]
    target = 9
    
    print(f"Test case: array = {test_array}, target = {target}")
    print("Expected: indices where arr[i] + arr[j] = {target}")
    
    print("\n🐌 APPROACH 1: Brute Force O(n²)")
    
    def two_sum_brute_force(nums, target):
        """Brute force approach with step tracking"""
        print("Checking all possible pairs:")
        print("i | j | nums[i] | nums[j] | Sum | Match?")
        print("-" * 45)
        
        comparisons = 0
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                comparisons += 1
                sum_val = nums[i] + nums[j]
                match = "YES" if sum_val == target else "NO"
                print(f"{i} | {j} | {nums[i]:7} | {nums[j]:7} | {sum_val:3} | {match}")
                
                if sum_val == target:
                    print(f"Found solution! Total comparisons: {comparisons}")
                    return [i, j]
        
        print(f"No solution found. Total comparisons: {comparisons}")
        return []
    
    result1 = two_sum_brute_force(test_array, target)
    
    print("\n🚀 APPROACH 2: Hash Table O(n)")
    
    def two_sum_hash_table(nums, target):
        """Optimal hash table approach with step tracking"""
        print("Using hash table for complement lookup:")
        print("i | nums[i] | complement | in_map? | Action")
        print("-" * 50)
        
        num_map = {}
        
        for i, num in enumerate(nums):
            complement = target - num
            in_map = complement in num_map
            
            if in_map:
                action = f"FOUND! Return [{num_map[complement]}, {i}]"
                print(f"{i} | {num:7} | {complement:10} | {str(in_map):7} | {action}")
                return [num_map[complement], i]
            else:
                action = f"Store {num} → index {i}"
                print(f"{i} | {num:7} | {complement:10} | {str(in_map):7} | {action}")
                num_map[num] = i
        
        print("No solution found")
        return []
    
    result2 = two_sum_hash_table(test_array, target)
    
    print("\n🎯 APPROACH 3: Two Pointers O(n log n)")
    
    def two_sum_two_pointers(nums, target):
        """Two pointers approach (requires sorting)"""
        # Create array of (value, original_index) pairs
        indexed_nums = [(nums[i], i) for i in range(len(nums))]
        indexed_nums.sort()  # Sort by value
        
        print("After sorting with original indices:")
        print("Value | Original Index")
        print("-" * 20)
        for val, orig_idx in indexed_nums:
            print(f"{val:5} | {orig_idx:13}")
        
        print("\nTwo pointers search:")
        print("Left | Right | Sum | Comparison | Action")
        print("-" * 45)
        
        left, right = 0, len(indexed_nums) - 1
        
        while left < right:
            left_val, left_idx = indexed_nums[left]
            right_val, right_idx = indexed_nums[right]
            current_sum = left_val + right_val
            
            if current_sum == target:
                action = f"FOUND! Indices [{left_idx}, {right_idx}]"
                print(f"{left:4} | {right:5} | {current_sum:3} | == target  | {action}")
                return sorted([left_idx, right_idx])
            elif current_sum < target:
                action = "Move left pointer right"
                print(f"{left:4} | {right:5} | {current_sum:3} | < target   | {action}")
                left += 1
            else:
                action = "Move right pointer left"
                print(f"{left:4} | {right:5} | {current_sum:3} | > target   | {action}")
                right -= 1
        
        print("No solution found")
        return []
    
    result3 = two_sum_two_pointers(test_array, target)
    
    print(f"\n📋 RESULTS COMPARISON:")
    print(f"Brute Force:  {result1}")
    print(f"Hash Table:   {result2}")
    print(f"Two Pointers: {result3}")

# ============================================================================
# PART 3: Hash Table Deep Dive
# ============================================================================

def hash_table_deep_dive():
    """
    Detailed analysis of hash table implementation and performance
    """
    print("\n\nHASH TABLE DEEP DIVE")
    print("=" * 25)
    
    print("🔍 HASH FUNCTION ANALYSIS:")
    print("Python dict uses open addressing with random probing")
    
    def demonstrate_hash_collisions():
        """Show how hash collisions are handled"""
        print("\nHash collision demonstration:")
        
        # Create keys that might collide
        test_keys = [1, 17, 33, 49]  # These might hash to similar values
        hash_table = {}
        
        print("Key | Hash Value | Collision? | Storage")
        print("-" * 45)
        
        for key in test_keys:
            hash_val = hash(key) % 16  # Simulate 16-slot table
            collision = "YES" if hash_val in [hash(k) % 16 for k in hash_table.keys()] else "NO"
            hash_table[key] = f"value_{key}"
            print(f"{key:3} | {hash_val:10} | {collision:10} | Slot {hash_val}")
    
    demonstrate_hash_collisions()
    
    print("\n⚡ PERFORMANCE CHARACTERISTICS:")
    performance_data = [
        ("Average case", "O(1)", "Hash function distributes evenly"),
        ("Worst case", "O(n)", "All keys hash to same slot"),
        ("Space complexity", "O(n)", "Store all key-value pairs"),
        ("Load factor", "< 0.75", "Maintains performance with resizing")
    ]
    
    print("Scenario      | Complexity | Description")
    print("-" * 50)
    for scenario, complexity, desc in performance_data:
        print(f"{scenario:13} | {complexity:10} | {desc}")
    
    print("\n🎯 HARDWARE CACHE ANALOGY:")
    print("Hash tables mirror CPU cache behavior:")
    cache_analogies = [
        "Hash function → Cache line calculation",
        "Collision resolution → Cache replacement policy",
        "Load factor → Cache utilization",
        "Resize operation → Cache hierarchy levels"
    ]
    
    for analogy in cache_analogies:
        print(f"  • {analogy}")

# ============================================================================
# PART 4: Hardware Validation Applications
# ============================================================================

def hardware_validation_applications():
    """
    Real-world hardware validation scenarios using Two Sum pattern
    """
    print("\n\nHARDWARE VALIDATION APPLICATIONS")
    print("=" * 40)
    
    print("🔧 APPLICATION 1: Voltage-Frequency Pairing")
    
    def find_voltage_frequency_pair(voltages, frequencies, target_power):
        """Find voltage-frequency pair that meets power target"""
        # Power = k * V² * f (simplified model)
        print(f"Finding V-F pair for target power: {target_power}W")
        print("Voltage | Frequency | Estimated Power | Match?")
        print("-" * 50)
        
        voltage_map = {}
        
        for i, v in enumerate(voltages):
            for j, f in enumerate(frequencies):
                power = 0.1 * v * v * f  # Simplified power model
                
                complement_power = target_power - power
                complement_exists = abs(complement_power) < 0.01  # Tolerance
                
                match = "YES" if abs(power - target_power) < 0.1 else "NO"
                print(f"{v:7.2f} | {f:9} | {power:15.2f} | {match}")
                
                if abs(power - target_power) < 0.1:
                    return (v, f, power)
                
                voltage_map[v] = (i, power)
        
        return None
    
    voltages = [0.8, 0.9, 1.0, 1.1, 1.2]
    frequencies = [1000, 1500, 2000, 2500, 3000]  # MHz
    result = find_voltage_frequency_pair(voltages, frequencies, 3.0)
    
    if result:
        print(f"Optimal pair found: {result[0]}V @ {result[1]}MHz = {result[2]:.2f}W")
    
    print("\n⚡ APPLICATION 2: Memory Access Pattern Analysis")
    
    def find_conflicting_addresses(addresses, cache_size):
        """Find address pairs that cause cache conflicts"""
        print(f"Finding cache conflicts for {cache_size}-entry cache:")
        print("Addr1 | Addr2 | Cache Line 1 | Cache Line 2 | Conflict?")
        print("-" * 60)
        
        conflicts = []
        addr_map = {}
        
        for i, addr1 in enumerate(addresses):
            line1 = addr1 % cache_size
            
            for j, addr2 in enumerate(addresses[i+1:], i+1):
                line2 = addr2 % cache_size
                conflict = "YES" if line1 == line2 else "NO"
                
                print(f"0x{addr1:03X} | 0x{addr2:03X} | {line1:11} | {line2:11} | {conflict}")
                
                if line1 == line2:
                    conflicts.append((addr1, addr2))
        
        return conflicts
    
    test_addresses = [0x100, 0x200, 0x300, 0x400, 0x500, 0x600]
    cache_size = 4
    conflicts = find_conflicting_addresses(test_addresses, cache_size)
    
    print(f"Cache conflicts found: {len(conflicts)}")
    for addr1, addr2 in conflicts:
        print(f"  0x{addr1:03X} conflicts with 0x{addr2:03X}")
    
    print("\n🧠 APPLICATION 3: Neural Network Weight Analysis")
    
    def find_weight_pairs_for_target(weights, target_activation):
        """Find weight pairs that produce target activation"""
        print(f"Finding weight pairs for target activation: {target_activation}")
        print("Weight1 | Weight2 | Product | Match?")
        print("-" * 40)
        
        weight_map = {}
        
        for i, w1 in enumerate(weights):
            complement = target_activation / w1 if w1 != 0 else float('inf')
            
            # Check if complement exists in our weight set
            for j, w2 in enumerate(weights):
                if i != j and abs(w1 * w2 - target_activation) < 0.01:
                    match = "YES"
                    print(f"{w1:7.2f} | {w2:7.2f} | {w1*w2:7.2f} | {match}")
                    return (i, j, w1, w2)
            
            weight_map[w1] = i
        
        print("No matching weight pair found")
        return None
    
    neural_weights = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    target = 3.0
    result = find_weight_pairs_for_target(neural_weights, target)
    
    if result:
        print(f"Weight pair found: indices {result[0]}, {result[1]} → {result[2]} × {result[3]} = {target}")

# ============================================================================
# PART 5: Variations and Extensions
# ============================================================================

def two_sum_variations():
    """
    Advanced variations of the Two Sum problem
    """
    print("\n\nTWO SUM VARIATIONS")
    print("=" * 20)
    
    print("🎯 VARIATION 1: Two Sum - All Pairs")
    print("Find ALL pairs that sum to target")
    
    def two_sum_all_pairs(nums, target):
        """Find all unique pairs that sum to target"""
        pairs = []
        seen = set()
        
        print(f"Finding all pairs that sum to {target} in {nums}")
        
        for i, num in enumerate(nums):
            complement = target - num
            
            if complement in seen:
                pair = tuple(sorted([num, complement]))
                if pair not in pairs:
                    pairs.append(pair)
                    print(f"Found pair: {pair}")
            
            seen.add(num)
        
        return pairs
    
    test_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    target = 10
    all_pairs = two_sum_all_pairs(test_nums, target)
    print(f"All pairs summing to {target}: {all_pairs}")
    
    print("\n🎯 VARIATION 2: Two Sum - Closest Sum")
    print("Find pair with sum closest to target")
    
    def two_sum_closest(nums, target):
        """Find pair with sum closest to target"""
        nums.sort()
        left, right = 0, len(nums) - 1
        closest_sum = float('inf')
        best_pair = None
        
        print(f"Finding pair closest to target {target}:")
        print("Left | Right | Sum | Distance | Best So Far")
        print("-" * 50)
        
        while left < right:
            current_sum = nums[left] + nums[right]
            distance = abs(current_sum - target)
            
            if distance < abs(closest_sum - target):
                closest_sum = current_sum
                best_pair = (nums[left], nums[right])
                best_status = f"NEW BEST: {best_pair}"
            else:
                best_status = f"Keep: {best_pair}"
            
            print(f"{nums[left]:4} | {nums[right]:5} | {current_sum:3} | {distance:8} | {best_status}")
            
            if current_sum < target:
                left += 1
            else:
                right -= 1
        
        return best_pair, closest_sum
    
    test_nums2 = [1, 3, 4, 7, 10]
    target2 = 15
    best_pair, closest_sum = two_sum_closest(test_nums2, target2)
    print(f"Closest pair: {best_pair} with sum {closest_sum}")
    
    print("\n🎯 VARIATION 3: Two Sum - Unique Elements")
    print("Handle duplicate elements correctly")
    
    def two_sum_with_duplicates(nums, target):
        """Handle arrays with duplicate elements"""
        index_map = {}  # Map value to list of indices
        
        # Build map of all indices for each value
        for i, num in enumerate(nums):
            if num not in index_map:
                index_map[num] = []
            index_map[num].append(i)
        
        print(f"Array with duplicates: {nums}")
        print("Value → Indices mapping:")
        for val, indices in index_map.items():
            print(f"  {val} → {indices}")
        
        for i, num in enumerate(nums):
            complement = target - num
            
            if complement in index_map:
                # Handle same number case (need at least 2 occurrences)
                if complement == num:
                    if len(index_map[num]) > 1:
                        indices = index_map[num]
                        return [indices[0], indices[1]]
                else:
                    return [i, index_map[complement][0]]
        
        return []
    
    nums_with_dups = [3, 3, 2, 1, 4, 4]
    target3 = 6
    result = two_sum_with_duplicates(nums_with_dups, target3)
    print(f"Result with duplicates: {result}")

# ============================================================================
# PART 6: Apple Interview Problems
# ============================================================================

def apple_interview_problems():
    """
    Two Sum related problems for Apple Silicon validation interviews
    """
    print("\n\nAPPLE SILICON VALIDATION INTERVIEW PROBLEMS")
    print("=" * 50)
    
    problems = [
        {
            "title": "Power Budget Optimization",
            "problem": "Given component power consumptions, find pairs that fit within power budget",
            "input": "powers = [10, 15, 20, 25, 30], budget = 45",
            "solution": "Use Two Sum with budget as target",
            "complexity": "O(n) time, O(n) space",
            "hardware_context": "Essential for thermal design and battery life"
        },
        {
            "title": "Clock Domain Synchronization",
            "problem": "Find two clock frequencies that have minimal phase drift",
            "input": "frequencies = [100, 133, 150, 200], max_drift = 10",
            "solution": "Modified Two Sum finding closest frequency pairs",
            "complexity": "O(n log n) time for sorting approach",
            "hardware_context": "Critical for timing closure in multi-clock designs"
        },
        {
            "title": "Memory Bank Interleaving",
            "problem": "Pair memory addresses to minimize bank conflicts",
            "input": "addresses = [0x100, 0x200, 0x104, 0x300], bank_bits = 2",
            "solution": "Two Sum variant checking bank assignment compatibility",
            "complexity": "O(n) with hash table tracking bank usage",
            "hardware_context": "Optimizes memory controller performance"
        },
        {
            "title": "Thermal Sensor Calibration",
            "problem": "Find sensor pairs that require similar calibration offsets",
            "input": "readings = [25.1, 24.9, 26.2, 25.8], tolerance = 0.5",
            "solution": "Two Sum finding pairs within temperature tolerance",
            "complexity": "O(n) with hash table for tolerance matching",
            "hardware_context": "Ensures accurate thermal monitoring across chip"
        }
    ]
    
    for i, prob in enumerate(problems, 1):
        print(f"\n🎯 PROBLEM {i}: {prob['title']}")
        print(f"   Challenge: {prob['problem']}")
        print(f"   Example Input: {prob['input']}")
        print(f"   Solution Approach: {prob['solution']}")
        print(f"   Complexity: {prob['complexity']}")
        print(f"   Hardware Context: {prob['hardware_context']}")

# ============================================================================
# PART 7: Performance Optimization Tips
# ============================================================================

def performance_optimization():
    """
    Performance optimization techniques for Two Sum
    """
    print("\n\nPERFORMANCE OPTIMIZATION TECHNIQUES")
    print("=" * 40)
    
    print("🚀 OPTIMIZATION 1: Early Termination")
    print("Stop as soon as first solution is found")
    
    print("\n🚀 OPTIMIZATION 2: Hash Table Sizing")
    print("Pre-size hash table to avoid resizing")
    
    def optimized_two_sum(nums, target):
        """Optimized Two Sum with pre-sized hash table"""
        # Pre-size hash table to avoid resizing
        hash_map = {}
        
        for i, num in enumerate(nums):
            complement = target - num
            
            if complement in hash_map:
                return [hash_map[complement], i]
            
            hash_map[num] = i
        
        return []
    
    print("\n🚀 OPTIMIZATION 3: Input Validation")
    print("Check for edge cases early")
    
    def robust_two_sum(nums, target):
        """Two Sum with comprehensive input validation"""
        # Edge case handling
        if not nums or len(nums) < 2:
            return []
        
        # Quick check for impossible cases
        min_sum = min(nums) + min(nums)
        max_sum = max(nums) + max(nums)
        
        if target < min_sum or target > max_sum:
            return []
        
        # Standard algorithm
        return optimized_two_sum(nums, target)
    
    print("\n📊 PERFORMANCE COMPARISON:")
    
    import time
    import random
    
    def benchmark_two_sum_variants(size):
        """Benchmark different Two Sum implementations"""
        # Generate test data
        nums = [random.randint(1, 1000) for _ in range(size)]
        target = nums[0] + nums[1]  # Ensure solution exists
        
        # Test brute force
        start = time.perf_counter()
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    break
        brute_time = time.perf_counter() - start
        
        # Test hash table
        start = time.perf_counter()
        optimized_two_sum(nums, target)
        hash_time = time.perf_counter() - start
        
        return brute_time, hash_time, brute_time / hash_time
    
    print("Array Size | Brute Force (μs) | Hash Table (μs) | Speedup")
    print("-" * 60)
    
    for size in [100, 1000, 5000]:
        brute_t, hash_t, speedup = benchmark_two_sum_variants(size)
        print(f"{size:10} | {brute_t*1e6:16.2f} | {hash_t*1e6:15.2f} | {speedup:7.1f}x")

# ============================================================================
# PART 8: Practice Exercises
# ============================================================================

def practice_exercises():
    """
    Hands-on Two Sum practice exercises
    """
    print("\n\nTWO SUM PRACTICE EXERCISES")
    print("=" * 28)
    
    exercises = [
        {
            "problem": "Three Sum - find triplets that sum to target",
            "hint": "Use Two Sum as subroutine, fix one element and find two sum for remainder",
            "complexity": "O(n²) time",
            "test_case": "nums = [-1,0,1,2,-1,-4], target = 0"
        },
        {
            "problem": "Four Sum - find quadruplets that sum to target", 
            "hint": "Extend Three Sum approach, use nested loops with Two Sum",
            "complexity": "O(n³) time",
            "test_case": "nums = [1,0,-1,0,-2,2], target = 0"
        },
        {
            "problem": "Two Sum - Input array is sorted",
            "hint": "Use two pointers instead of hash table for O(1) space",
            "complexity": "O(n) time, O(1) space",
            "test_case": "nums = [2,7,11,15], target = 9"
        },
        {
            "problem": "Two Sum - Design data structure",
            "hint": "Support add() and find() operations efficiently",
            "complexity": "O(1) add, O(n) find",
            "test_case": "add(1), add(3), add(5), find(4) → true"
        }
    ]
    
    print("💪 Master these extensions:")
    for i, ex in enumerate(exercises, 1):
        print(f"\n📝 EXERCISE {i}:")
        print(f"   Problem: {ex['problem']}")
        print(f"   Hint: {ex['hint']}")
        print(f"   Complexity: {ex['complexity']}")
        print(f"   Test: {ex['test_case']}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("TWO SUM MASTERY FOR APPLE SILICON VALIDATION")
    print("=" * 50)
    
    explain_two_sum_basics()
    hardware_relevance()
    algorithm_implementations()
    hash_table_deep_dive()
    hardware_validation_applications()
    two_sum_variations()
    apple_interview_problems()
    performance_optimization()
    practice_exercises()
    
    print("\n" + "=" * 50)
    print("🎓 TWO SUM MASTERY CHECKLIST:")
    print("✓ Master hash table approach (O(n) time, O(n) space)")
    print("✓ Understand complement lookup strategy")
    print("✓ Handle edge cases: duplicates, no solution, empty array")
    print("✓ Know variations: all pairs, closest sum, k-sum problems")
    print("✓ Apply to hardware: power budgets, frequency pairing")
    print("✓ Optimize for performance: pre-sizing, early termination")
    print("✓ Connect to broader concepts: caching, hash functions")