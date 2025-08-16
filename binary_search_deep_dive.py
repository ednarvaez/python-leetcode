"""
BINARY SEARCH DEEP DIVE
Essential for Apple Silicon Validation - Search algorithms in hardware testing
"""

# ============================================================================
# PART 1: Binary Search Fundamentals
# ============================================================================

def explain_binary_search_basics():
    """
    Binary search fundamentals and why it's crucial for hardware validation
    """
    print("BINARY SEARCH FUNDAMENTALS")
    print("=" * 30)
    
    print("🔍 CORE CONCEPT:")
    print("Divide sorted array in half repeatedly until target is found")
    print("Similar to 'guess the number' game with optimal strategy")
    
    print("\n📊 TIME COMPLEXITY ANALYSIS:")
    complexities = [
        ("Best case", "O(1)", "Target is middle element"),
        ("Average case", "O(log n)", "Target requires log₂(n) comparisons"),
        ("Worst case", "O(log n)", "Target is at boundary or not found"),
        ("Space", "O(1)", "Iterative version uses constant space")
    ]
    
    print("Case        | Complexity | Explanation")
    print("-" * 50)
    for case, complexity, explanation in complexities:
        print(f"{case:11} | {complexity:10} | {explanation}")
    
    print("\n🎯 WHY O(log n) IS POWERFUL:")
    print("For hardware validation with large datasets:")
    
    sizes = [100, 1000, 10000, 100000, 1000000]
    print("Array Size | Linear Search | Binary Search | Improvement")
    print("-" * 60)
    for size in sizes:
        linear_ops = size
        binary_ops = int(size.bit_length())  # Approximation of log₂(n)
        improvement = linear_ops // binary_ops
        print(f"{size:10} | {linear_ops:13} | {binary_ops:13} | {improvement}x faster")

def hardware_validation_context():
    """
    Why binary search is essential in silicon validation
    """
    print("\n\nBINARY SEARCH IN SILICON VALIDATION")
    print("=" * 40)
    
    applications = [
        "🔧 THRESHOLD DETECTION: Find voltage/frequency limits",
        "📊 PERFORMANCE ANALYSIS: Locate timing boundaries", 
        "🎯 TEST PATTERN SEARCH: Find failing test vectors",
        "⚡ POWER OPTIMIZATION: Search optimal operating points",
        "🧠 MEMORY TESTING: Binary search for fault locations",
        "📈 CALIBRATION: Find optimal register settings",
        "🔍 DEBUG: Locate error sources in large datasets",
        "⏱️ TIMING ANALYSIS: Find setup/hold violations"
    ]
    
    for app in applications:
        print(f"  {app}")
    
    print("\n🏭 APPLE SILICON SPECIFIC EXAMPLES:")
    apple_examples = [
        "Neural Engine: Search optimal quantization thresholds",
        "GPU: Find maximum stable clock frequencies",  
        "CPU: Locate thermal throttling points",
        "Memory Controller: Search for ECC error patterns",
        "Secure Enclave: Find cryptographic timing vulnerabilities"
    ]
    
    for example in apple_examples:
        print(f"  • {example}")

# ============================================================================
# PART 2: Step-by-Step Algorithm Breakdown
# ============================================================================

def binary_search_step_by_step():
    """
    Detailed step-by-step binary search demonstration
    """
    print("\n\nBINARY SEARCH STEP-BY-STEP ANALYSIS")
    print("=" * 45)
    
    def binary_search_verbose(arr, target):
        """
        INTERVIEW STRATEGY: Walk through each step to show your thinking process
        This verbose version demonstrates the algorithm's logic clearly
        """
        # Initialize search boundaries to cover entire array
        left, right = 0, len(arr) - 1  # Include both endpoints
        step = 1  # Track iterations for educational purposes
        
        # Display initial setup for interviewer
        print(f"Searching for {target} in array: {arr}")
        print(f"Array size: {len(arr)}, Maximum steps needed: {len(arr).bit_length()}")
        print("\nStep | Left | Right | Mid | arr[mid] | Comparison | Action")
        print("-" * 65)
        
        # Continue while search space is valid (non-empty)
        while left <= right:  # <= is crucial - handles single element case
            
            # Calculate middle index (avoids overflow in other languages)
            mid = (left + right) // 2  # Integer division for array index
            mid_val = arr[mid]  # Cache value for clarity and efficiency
            
            # Check if we found the target
            if mid_val == target:
                comparison = "FOUND!"
                action = f"Return index {mid}"
                print(f"{step:4} | {left:4} | {right:5} | {mid:3} | {mid_val:7} | {comparison:10} | {action}")
                return mid  # Success: return index where target was found
                
            # Target is in the right half (higher values)
            elif mid_val < target:
                comparison = "< target"
                action = f"Search right: left = {mid + 1}"
                print(f"{step:4} | {left:4} | {right:5} | {mid:3} | {mid_val:7} | {comparison:10} | {action}")
                left = mid + 1  # Exclude current mid from search space
                
            # Target is in the left half (lower values)
            else:
                comparison = "> target"
                action = f"Search left: right = {mid - 1}"
                print(f"{step:4} | {left:4} | {right:5} | {mid:3} | {mid_val:7} | {comparison:10} | {action}")
                right = mid - 1  # Exclude current mid from search space
            
            step += 1  # Increment for next iteration
        
        # Search space exhausted without finding target
        print(f"{step:4} | {left:4} | {right:5} | N/A | N/A     | NOT FOUND  | Return -1")
        return -1  # Failure: target not in array
    
    # Test cases with different scenarios
    test_cases = [
        ([1, 3, 5, 7, 9, 11, 13, 15], 7, "Found in middle"),
        ([1, 3, 5, 7, 9, 11, 13, 15], 1, "Found at beginning"),
        ([1, 3, 5, 7, 9, 11, 13, 15], 15, "Found at end"),
        ([1, 3, 5, 7, 9, 11, 13, 15], 6, "Not found - between elements")
    ]
    
    for arr, target, description in test_cases:
        print(f"\n📋 TEST CASE: {description}")
        result = binary_search_verbose(arr, target)
        print(f"Result: {'Found at index ' + str(result) if result != -1 else 'Not found'}")

def search_space_visualization():
    """
    Visual representation of how search space shrinks
    """
    print("\n\nSEARCH SPACE VISUALIZATION")
    print("=" * 30)
    
    def visualize_search_space(arr, target):
        """Show how search space shrinks with each iteration"""
        left, right = 0, len(arr) - 1
        step = 1
        
        print(f"Visualizing search for {target} in {arr}")
        
        while left <= right:
            # Create visual representation
            visual = ['.' for _ in range(len(arr))]
            for i in range(left, right + 1):
                visual[i] = str(arr[i])
            
            mid = (left + right) // 2
            visual[mid] = f"[{arr[mid]}]"  # Highlight middle element
            
            print(f"Step {step}: {' '.join(visual)}")
            print(f"         Range: indices {left}-{right}, checking arr[{mid}] = {arr[mid]}")
            
            if arr[mid] == target:
                print(f"         ✓ FOUND! Target {target} at index {mid}")
                return mid
            elif arr[mid] < target:
                print(f"         {arr[mid]} < {target}, search right half")
                left = mid + 1
            else:
                print(f"         {arr[mid]} > {target}, search left half")
                right = mid - 1
            
            step += 1
            print()
        
        print(f"         ✗ NOT FOUND: Target {target} not in array")
        return -1
    
    # Demonstration
    test_array = [2, 5, 8, 12, 16, 23, 38, 45, 67, 78]
    visualize_search_space(test_array, 23)

# ============================================================================
# PART 3: Binary Search Variants for Hardware Testing
# ============================================================================

def binary_search_variants():
    """
    Different binary search variants used in hardware validation
    """
    print("\n\nBINARY SEARCH VARIANTS FOR HARDWARE")
    print("=" * 40)
    
    print("🎯 VARIANT 1: Find First Occurrence")
    print("Used to find first failing test case in sorted test results")
    
    def find_first_occurrence(arr, target):
        """
        BINARY SEARCH VARIANT: Find leftmost occurrence
        HARDWARE USE CASE: Find first failing test in sorted test results
        
        Key difference: When target is found, continue searching left
        to ensure we find the FIRST occurrence, not just any occurrence
        """
        # Standard binary search initialization
        left, right = 0, len(arr) - 1
        result = -1  # Track best candidate found so far
        
        # Continue until search space is exhausted
        while left <= right:
            mid = (left + right) // 2  # Calculate middle index
            
            # Found target, but keep searching left for first occurrence
            if arr[mid] == target:
                result = mid      # Update best candidate
                right = mid - 1   # Search left half to find earlier occurrence
                # Note: Don't return immediately - there might be earlier occurrences
                
            # Target is in right half
            elif arr[mid] < target:
                left = mid + 1    # Standard binary search logic
                
            # Target is in left half  
            else:
                right = mid - 1   # Standard binary search logic
        
        return result  # Return leftmost occurrence (or -1 if not found)
    
    # Example: Find first failing voltage threshold
    voltage_tests = [0, 0, 0, 1, 1, 1, 1]  # 0=pass, 1=fail
    first_fail = find_first_occurrence(voltage_tests, 1)
    print(f"Voltage test results: {voltage_tests}")
    print(f"First failure at index: {first_fail} (threshold found)")
    
    print("\n🎯 VARIANT 2: Find Peak Element")
    print("Used to find maximum performance points in characterization")
    
    def find_peak_element(arr):
        """Find peak element (greater than neighbors)"""
        left, right = 0, len(arr) - 1
        
        while left < right:
            mid = (left + right) // 2
            
            if arr[mid] > arr[mid + 1]:
                right = mid  # Peak is in left half
            else:
                left = mid + 1  # Peak is in right half
        
        return left
    
    # Example: Find maximum frequency before thermal throttling
    frequencies = [1.0, 1.5, 2.1, 2.8, 3.2, 2.9, 2.4, 1.8]  # GHz
    peak_idx = find_peak_element(frequencies)
    print(f"Frequency curve: {frequencies}")
    print(f"Peak performance at index {peak_idx}: {frequencies[peak_idx]} GHz")
    
    print("\n🎯 VARIANT 3: Search in Rotated Array")
    print("Used when test data wraps around (circular buffers)")
    
    def search_rotated_array(arr, target):
        """Search in rotated sorted array"""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return mid
            
            # Check which half is sorted
            if arr[left] <= arr[mid]:  # Left half is sorted
                if arr[left] <= target < arr[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:  # Right half is sorted
                if arr[mid] < target <= arr[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        
        return -1
    
    # Example: Circular buffer of performance measurements
    circular_data = [4, 5, 6, 7, 0, 1, 2]  # Rotated at index 4
    target = 0
    result = search_rotated_array(circular_data, target)
    print(f"Circular buffer: {circular_data}")
    print(f"Found {target} at index: {result}")

# ============================================================================
# PART 4: Hardware-Specific Binary Search Applications
# ============================================================================

def hardware_specific_applications():
    """
    Detailed hardware validation scenarios using binary search
    """
    print("\n\nHARDWARE VALIDATION SCENARIOS")
    print("=" * 35)
    
    print("🔧 SCENARIO 1: Voltage Threshold Detection")
    
    def find_voltage_threshold(voltage_range, test_function):
        """Binary search to find minimum operating voltage"""
        low, high = voltage_range
        precision = 0.01  # 10mV precision
        
        print(f"Finding minimum voltage in range {low}V - {high}V")
        iterations = 0
        
        while high - low > precision:
            mid = (low + high) / 2
            iterations += 1
            
            # Simulate hardware test
            passes = test_function(mid)
            print(f"  Test {iterations}: {mid:.2f}V → {'PASS' if passes else 'FAIL'}")
            
            if passes:
                high = mid  # Can go lower
            else:
                low = mid   # Need higher voltage
        
        threshold = (low + high) / 2
        print(f"  Minimum voltage found: {threshold:.2f}V in {iterations} iterations")
        return threshold
    
    # Simulate voltage test function
    def voltage_test(voltage):
        return voltage >= 0.85  # Minimum 0.85V required
    
    find_voltage_threshold((0.7, 1.2), voltage_test)
    
    print("\n⚡ SCENARIO 2: Frequency Characterization")
    
    def find_max_frequency(freq_range, stability_test):
        """Find maximum stable frequency"""
        low, high = freq_range
        
        print(f"Finding max stable frequency in range {low} - {high} MHz")
        iterations = 0
        
        while high - low > 1:  # 1 MHz precision
            mid = (low + high) // 2
            iterations += 1
            
            stable = stability_test(mid)
            print(f"  Test {iterations}: {mid} MHz → {'STABLE' if stable else 'UNSTABLE'}")
            
            if stable:
                low = mid   # Can go higher
            else:
                high = mid - 1  # Too high, reduce
        
        max_freq = low
        print(f"  Maximum frequency: {max_freq} MHz in {iterations} iterations")
        return max_freq
    
    # Simulate frequency stability test
    def freq_stability_test(frequency):
        return frequency <= 2800  # Max 2.8 GHz stable
    
    find_max_frequency((2000, 3200), freq_stability_test)
    
    print("\n🧠 SCENARIO 3: Memory Error Location")
    
    def find_memory_error(memory_size, error_test):
        """Binary search to locate memory errors"""
        low, high = 0, memory_size - 1
        
        print(f"Locating memory error in {memory_size} byte range")
        iterations = 0
        max_iterations = 20  # Safety limit to prevent infinite loops
        
        while low < high and iterations < max_iterations:
            mid = (low + high) // 2
            iterations += 1
            
            error_in_lower_half = error_test(low, mid)
            print(f"  Test {iterations}: Range {low:04X}-{mid:04X} → {'ERROR' if error_in_lower_half else 'OK'}")
            
            if error_in_lower_half:
                high = mid  # Error is in lower half, narrow to [low, mid]
            else:
                low = mid + 1  # Error is in upper half, narrow to [mid+1, high]
        
        error_addr = low
        print(f"  Error located at address: 0x{error_addr:04X} in {iterations} iterations")
        return error_addr
    
    # Simulate memory error test
    def memory_error_test(start_addr, end_addr):
        error_location = 0x1A3F  # Simulated error address
        return start_addr <= error_location <= end_addr
    
    find_memory_error(0x10000, memory_error_test)  # 64KB memory

# ============================================================================
# PART 5: Common Pitfalls and Edge Cases
# ============================================================================

def binary_search_pitfalls():
    """
    Common mistakes and edge cases in binary search implementation
    """
    print("\n\nCOMMON BINARY SEARCH PITFALLS")
    print("=" * 35)
    
    print("⚠️  PITFALL 1: Integer Overflow")
    print("Wrong:  mid = (left + right) / 2")
    print("Right:  mid = left + (right - left) / 2")
    print("Reason: Prevents overflow when left + right > MAX_INT")
    
    print("\n⚠️  PITFALL 2: Infinite Loop")
    print("Wrong:  while left < right: ... right = mid")
    print("Right:  while left <= right: ... right = mid - 1")
    print("Reason: Ensures loop termination")
    
    print("\n⚠️  PITFALL 3: Off-by-One Errors")
    print("Always verify boundary conditions:")
    
    def test_boundary_conditions():
        """Test edge cases"""
        test_cases = [
            ([], 1, "Empty array"),
            ([1], 1, "Single element - found"),
            ([1], 2, "Single element - not found"),
            ([1, 2], 1, "Two elements - first"),
            ([1, 2], 2, "Two elements - second"),
            ([1, 2], 3, "Two elements - not found")
        ]
        
        def safe_binary_search(arr, target):
            """
            PRODUCTION-READY binary search with edge case handling
            INTERVIEW TIP: Always demonstrate defensive programming
            """
            # Edge case: empty array
            if not arr:
                return -1  # Can't find anything in empty array
                
            # Initialize search boundaries
            left, right = 0, len(arr) - 1
            
            # Main search loop
            while left <= right:
                # OVERFLOW-SAFE middle calculation
                # In languages like C++/Java: (left + right) might overflow
                # Safe formula: left + (right - left) // 2
                mid = left + (right - left) // 2
                
                # Target found
                if arr[mid] == target:
                    return mid
                    
                # Search right half
                elif arr[mid] < target:
                    left = mid + 1  # Exclude mid from future searches
                    
                # Search left half
                else:
                    right = mid - 1  # Exclude mid from future searches
            
            # Target not found after exhausting search space
            return -1
        
        print("Edge Case Testing:")
        print("Array      | Target | Result | Description")
        print("-" * 45)
        
        for arr, target, description in test_cases:
            result = safe_binary_search(arr, target)
            result_str = str(result) if result != -1 else "Not found"
            print(f"{str(arr):10} | {target:6} | {result_str:10} | {description}")
    
    test_boundary_conditions()

# ============================================================================
# PART 6: Performance Analysis for Hardware Applications
# ============================================================================

def performance_analysis():
    """
    Performance characteristics important for hardware validation
    """
    print("\n\nPERFORMANCE ANALYSIS FOR HARDWARE VALIDATION")
    print("=" * 50)
    
    print("📊 COMPARISON WITH OTHER SEARCH METHODS:")
    
    import time
    import random
    
    def benchmark_search_methods(size):
        """Benchmark different search approaches"""
        # Generate sorted test data
        arr = sorted(random.sample(range(size * 10), size))
        target = arr[size // 2]  # Target in middle
        
        # Linear search
        start_time = time.perf_counter()
        for i, val in enumerate(arr):
            if val == target:
                linear_result = i
                break
        linear_time = time.perf_counter() - start_time
        
        # Binary search
        start_time = time.perf_counter()
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                binary_result = mid
                break
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        binary_time = time.perf_counter() - start_time
        
        return linear_time, binary_time, linear_time / binary_time
    
    print("Array Size | Linear (μs) | Binary (μs) | Speedup")
    print("-" * 50)
    
    sizes = [100, 1000, 10000]
    for size in sizes:
        linear_t, binary_t, speedup = benchmark_search_methods(size)
        print(f"{size:10} | {linear_t*1e6:11.2f} | {binary_t*1e6:11.2f} | {speedup:7.1f}x")
    
    print("\n🎯 HARDWARE VALIDATION IMPLICATIONS:")
    implications = [
        "Real-time testing: Binary search enables live characterization",
        "Large datasets: Essential for processing millions of test vectors",
        "Power efficiency: Fewer operations = lower test power consumption",
        "Time-to-market: Faster validation cycles reduce development time"
    ]
    
    for implication in implications:
        print(f"  • {implication}")

# ============================================================================
# PART 7: Apple Interview Problems
# ============================================================================

def apple_interview_problems():
    """
    Binary search problems specific to Apple Silicon validation interviews
    """
    print("\n\nAPPLE SILICON VALIDATION INTERVIEW PROBLEMS")
    print("=" * 50)
    
    problems = [
        {
            "title": "Neural Engine Quantization Threshold",
            "problem": "Find optimal quantization bits that maintain accuracy above 95%",
            "solution": "Binary search on quantization levels (1-16 bits)",
            "complexity": "O(log k) where k is bit range",
            "code": "Binary search on [1,16] testing accuracy at each level"
        },
        {
            "title": "GPU Shader Compiler Optimization",
            "problem": "Find maximum optimization level before compilation fails",
            "solution": "Binary search on optimization levels",
            "complexity": "O(log n) where n is max optimization level",
            "code": "Test compilation success at each optimization level"
        },
        {
            "title": "Memory Timing Violation Detection",
            "problem": "Find minimum clock period that avoids timing violations",
            "solution": "Binary search on clock periods with timing analysis",
            "complexity": "O(log t) where t is timing range",
            "code": "Binary search with setup/hold time verification"
        },
        {
            "title": "Thermal Throttling Point Identification", 
            "problem": "Find temperature where CPU starts throttling performance",
            "solution": "Binary search on temperature range monitoring performance",
            "complexity": "O(log T) where T is temperature range",
            "code": "Monitor frequency vs temperature with binary search"
        }
    ]
    
    for i, prob in enumerate(problems, 1):
        print(f"\n🎯 PROBLEM {i}: {prob['title']}")
        print(f"   Challenge: {prob['problem']}")
        print(f"   Approach: {prob['solution']}")
        print(f"   Complexity: {prob['complexity']}")
        print(f"   Implementation: {prob['code']}")

# ============================================================================
# PART 8: Practice Exercises
# ============================================================================

def practice_exercises():
    """
    Hands-on binary search exercises
    """
    print("\n\nBINARY SEARCH PRACTICE EXERCISES")
    print("=" * 35)
    
    exercises = [
        {
            "problem": "Find square root using binary search",
            "hint": "Search in range [0, x] where mid*mid <= x",
            "test_case": "x = 8, answer = 2"
        },
        {
            "problem": "Search in 2D matrix (sorted rows and columns)",
            "hint": "Start from top-right corner, eliminate row or column",
            "test_case": "Find 7 in [[1,4,7],[2,5,8],[3,6,9]]"
        },
        {
            "problem": "Find minimum in rotated sorted array",
            "hint": "Compare with rightmost element to determine rotation",
            "test_case": "[4,5,6,7,0,1,2] → minimum is 0"
        },
        {
            "problem": "Capacity to ship packages within D days",
            "hint": "Binary search on ship capacity, verify feasibility",
            "test_case": "weights=[1,2,3,4,5,6,7,8,9,10], D=5"
        }
    ]
    
    print("💪 Master these problems:")
    for i, ex in enumerate(exercises, 1):
        print(f"\n📝 EXERCISE {i}:")
        print(f"   Problem: {ex['problem']}")
        print(f"   Hint: {ex['hint']}")
        print(f"   Test: {ex['test_case']}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("BINARY SEARCH MASTERY FOR APPLE SILICON VALIDATION")
    print("=" * 55)
    
    explain_binary_search_basics()
    hardware_validation_context()
    binary_search_step_by_step()
    search_space_visualization()
    binary_search_variants()
    hardware_specific_applications()
    binary_search_pitfalls()
    performance_analysis()
    apple_interview_problems()
    practice_exercises()
    
    print("\n" + "=" * 55)
    print("🎓 BINARY SEARCH MASTERY CHECKLIST:")
    print("✓ Understand O(log n) time complexity and why it matters")
    print("✓ Master iterative implementation (avoid recursion overhead)")
    print("✓ Handle edge cases and prevent infinite loops")
    print("✓ Know variants: first/last occurrence, peak finding")
    print("✓ Apply to hardware: thresholds, characterization, debugging")
    print("✓ Recognize when binary search is applicable (sorted data)")
    print("✓ Practice hardware-specific validation scenarios")