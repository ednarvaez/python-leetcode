"""1. Log Grep with Context (Python) — NVIDIA
Problem: Given a log file, print the line before and after each line containing a target substring (like "ERROR").
Input: file path, pattern
Output: triples of (prev, match, next); handle boundaries"""


from collections import deque
from typing import List, Tuple, Optional

def grep_with_context(file_path: str, pattern: str) -> List[Tuple[Optional[str], str, Optional[str]]]:
    """
    Find lines containing pattern and return with context (prev, match, next).
    
    Args:
        file_path: Path to log file
        pattern: Substring to search for
        
    Returns:
        List of tuples (prev_line, match_line, next_line)
    """
    results = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        # Strip newlines for cleaner output
        lines = [line.rstrip('\n\r') for line in lines]
        
        for i, line in enumerate(lines):
            if pattern in line:
                prev_line = lines[i-1] if i > 0 else None
                match_line = line
                next_line = lines[i+1] if i < len(lines)-1 else None
                
                results.append((prev_line, match_line, next_line))
                
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
        
    return results

def grep_with_context_streaming(file_path: str, pattern: str) -> List[Tuple[Optional[str], str, Optional[str]]]:
    """
    Memory-efficient version using a sliding window approach.
    Better for very large log files.
    """
    results = []
    window = deque(maxlen=3)  # [prev, current, next]
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Initialize window with first two lines
            for _ in range(2):
                try:
                    line = next(f).rstrip('\n\r')
                    window.append(line)
                except StopIteration:
                    break
            
            # Process remaining lines
            for line in f:
                line = line.rstrip('\n\r')
                window.append(line)
                
                # Check middle element (current line being processed)
                if len(window) >= 2 and pattern in window[-2]:
                    prev_line = window[0] if len(window) == 3 else None
                    match_line = window[-2]
                    next_line = window[-1]
                    results.append((prev_line, match_line, next_line))
            
            # Check last line
            if len(window) >= 1 and pattern in window[-1]:
                prev_line = window[-2] if len(window) >= 2 else None
                match_line = window[-1]
                next_line = None
                results.append((prev_line, match_line, next_line))
                
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
        
    return results

# Example usage and test
def test_grep_context():
    # Create sample log file
    sample_log = """2024-08-19 10:00:01 INFO System starting
2024-08-19 10:00:02 DEBUG Loading configuration
2024-08-19 10:00:03 ERROR Failed to connect to database
2024-08-19 10:00:04 INFO Retrying connection
2024-08-19 10:00:05 INFO Connection established
2024-08-19 10:00:06 ERROR Memory allocation failed
2024-08-19 10:00:07 FATAL System shutdown"""
    
    with open('sample.log', 'w') as f:
        f.write(sample_log)
    
    # Test the function
    results = grep_with_context('sample.log', 'ERROR')
    
    print("Grep results with context:")
    for i, (prev, match, next_line) in enumerate(results, 1):
        print(f"\nMatch {i}:")
        print(f"  Prev: {prev}")
        print(f"  Match: {match}")
        print(f"  Next: {next_line}")

if __name__ == "__main__":
    test_grep_context()