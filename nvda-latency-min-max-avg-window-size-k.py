"""

Shift Window Stats (Python) — NVIDIA
Problem: For a latency list, compute min/avg/max for each sliding window of size k.
Target: O(n) using a deque for min/max; simple running sum for avg.


"""




from collections import deque
from typing import List, Tuple

def sliding_window_stats(latencies: List[float], k: int) -> List[Tuple[float, float, float]]:
    """
    Compute min/avg/max for each sliding window of size k.
    
    Time Complexity: O(n)
    Space Complexity: O(k)
    
    Args:
        latencies: List of latency values
        k: Window size
        
    Returns:
        List of tuples (min, avg, max) for each window
    """
    if not latencies or k <= 0 or k > len(latencies):
        return []
    
    results = []
    
    # Deques to maintain min/max in O(1) amortized time
    min_deque = deque()  # Stores indices, maintains increasing order of values
    max_deque = deque()  # Stores indices, maintains decreasing order of values
    
    # Running sum for average calculation
    window_sum = 0.0
    
    for i in range(len(latencies)):
        current = latencies[i]
        
        # Add current element to window sum
        window_sum += current
        
        # Maintain min_deque (increasing order)
        while min_deque and latencies[min_deque[-1]] >= current:
            min_deque.pop()
        min_deque.append(i)
        
        # Maintain max_deque (decreasing order)
        while max_deque and latencies[max_deque[-1]] <= current:
            max_deque.pop()
        max_deque.append(i)
        
        # Remove elements outside current window
        if min_deque[0] <= i - k:
            min_deque.popleft()
        if max_deque[0] <= i - k:
            max_deque.popleft()
        
        # If we have a complete window
        if i >= k - 1:
            # Remove element that's leaving the window
            if i >= k:
                window_sum -= latencies[i - k]
            
            # Calculate stats
            window_min = latencies[min_deque[0]]
            window_max = latencies[max_deque[0]]
            window_avg = window_sum / k
            
            results.append((window_min, window_avg, window_max))
    
    return results

def sliding_window_stats_simple(latencies: List[float], k: int) -> List[Tuple[float, float, float]]:
    """
    Simple O(n*k) implementation for comparison/validation.
    """
    if not latencies or k <= 0 or k > len(latencies):
        return []
    
    results = []
    
    for i in range(len(latencies) - k + 1):
        window = latencies[i:i+k]
        window_min = min(window)
        window_max = max(window)
        window_avg = sum(window) / k
        results.append((window_min, window_avg, window_max))
    
    return results

def test_sliding_window():
    """Test sliding window stats with various inputs."""
    # Test case from problem description
    latencies = [5, 1, 3, 4, 6]
    k = 3
    
    print("=== Sliding Window Stats Test ===")
    print(f"Input: {latencies}")
    print(f"Window size: {k}")
    print()
    
    # Test optimized version
    results_opt = sliding_window_stats(latencies, k)
    print("Optimized O(n) results:")
    for i, (min_val, avg_val, max_val) in enumerate(results_opt):
        window_start = i
        window_end = i + k - 1
        print(f"  Window [{window_start}:{window_end+1}]: min={min_val}, avg={avg_val:.2f}, max={max_val}")
    
    print()
    
    # Test simple version for validation
    results_simple = sliding_window_stats_simple(latencies, k)
    print("Simple O(n*k) results (validation):")
    for i, (min_val, avg_val, max_val) in enumerate(results_simple):
        window_start = i
        window_end = i + k - 1
        print(f"  Window [{window_start}:{window_end+1}]: min={min_val}, avg={avg_val:.2f}, max={max_val}")
    
    # Verify results match
    match = results_opt == results_simple
    print(f"\nResults match: {match}")
    
    # Performance test with larger data
    import time
    import random
    
    large_data = [random.uniform(0, 100) for _ in range(10000)]
    k_large = 100
    
    # Time optimized version
    start_time = time.time()
    results_opt_large = sliding_window_stats(large_data, k_large)
    opt_time = time.time() - start_time
    
    print(f"\nPerformance test (n=10000, k=100):")
    print(f"Optimized version: {opt_time:.4f} seconds")

if __name__ == "__main__":
    test_sliding_window()