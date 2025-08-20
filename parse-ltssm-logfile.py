"""
 PCIe LTSSM Summary (Python) — Validation
Problem: Parse a CSV trace of LTSSM states (Detect, Polling, Config, L0, Recovery, etc.).
Output: (a) first time to L0, (b) number of retrains, (c) longest dwell in Recovery"""



import csv
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class LTSSMState(Enum):
    DETECT = "Detect"
    POLLING = "Polling" 
    CONFIG = "Config"
    L0 = "L0"
    RECOVERY = "Recovery"
    L0S = "L0s"
    L1 = "L1"
    L2 = "L2"
    DISABLED = "Disabled"
    LOOPBACK = "Loopback"
    HOTRESET = "HotReset"

@dataclass
class LTSSMEvent:
    timestamp: float
    state: str
    data: Optional[str] = None

@dataclass  
class LTSSMAnalysis:
    first_l0_time: Optional[float]
    retrain_count: int
    longest_recovery_dwell: float
    total_time: float
    state_dwells: Dict[str, float]
    speed_changes: List[Tuple[float, str, str]]

def parse_ltssm_trace(csv_file: str) -> LTSSMAnalysis:
    """
    Parse LTSSM CSV trace and extract key metrics.
    
    Expected CSV format:
    timestamp, ltssm_state, additional_data
    """
    events = []
    
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamp = float(row['timestamp'])
                state = row['ltssm_state'].strip()
                data = row.get('additional_data', '').strip()
                events.append(LTSSMEvent(timestamp, state, data))
                
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return LTSSMAnalysis(None, 0, 0.0, 0.0, {}, [])
    
    if not events:
        return LTSSMAnalysis(None, 0, 0.0, 0.0, {}, [])
    
    # Initialize analysis
    first_l0_time = None
    retrain_count = 0
    longest_recovery_dwell = 0.0
    current_recovery_start = None
    state_dwells = {}
    speed_changes = []
    
    # Track state transitions
    prev_event = events[0]
    current_speed = "Gen1"  # Default starting speed
    
    for i, event in enumerate(events[1:], 1):
        # Calculate dwell time
        dwell_time = event.timestamp - prev_event.timestamp
        
        # Track state dwell times
        if prev_event.state not in state_dwells:
            state_dwells[prev_event.state] = 0.0
        state_dwells[prev_event.state] += dwell_time
        
        # Find first L0
        if event.state == "L0" and first_l0_time is None:
            first_l0_time = event.timestamp
        
        # Count retrains (Recovery -> Config or Recovery -> Polling)
        if (prev_event.state == "Recovery" and 
            event.state in ["Config", "Polling"]):
            retrain_count += 1
        
        # Track Recovery state dwell
        if prev_event.state == "Recovery":
            if current_recovery_start is None:
                current_recovery_start = prev_event.timestamp
        else:
            if current_recovery_start is not None:
                recovery_dwell = prev_event.timestamp - current_recovery_start
                longest_recovery_dwell = max(longest_recovery_dwell, recovery_dwell)
                current_recovery_start = None
        
        # Track speed changes
        if event.data and "Gen" in event.data:
            new_speed = event.data
            if new_speed != current_speed:
                speed_changes.append((event.timestamp, current_speed, new_speed))
                current_speed = new_speed
        
        prev_event = event
    
    # Handle final Recovery state if trace ends in Recovery
    if current_recovery_start is not None:
        recovery_dwell = events[-1].timestamp - current_recovery_start
        longest_recovery_dwell = max(longest_recovery_dwell, recovery_dwell)
    
    total_time = events[-1].timestamp - events[0].timestamp
    
    return LTSSMAnalysis(
        first_l0_time=first_l0_time,
        retrain_count=retrain_count,
        longest_recovery_dwell=longest_recovery_dwell,
        total_time=total_time,
        state_dwells=state_dwells,
        speed_changes=speed_changes
    )

def print_ltssm_analysis(analysis: LTSSMAnalysis):
    """Pretty print LTSSM analysis results."""
    print("=== LTSSM Trace Analysis ===")
    print(f"Total trace time: {analysis.total_time:.3f} ms")
    print()
    
    if analysis.first_l0_time:
        print(f"First time to L0: {analysis.first_l0_time:.3f} ms")
    else:
        print("Never reached L0 state")
    
    print(f"Number of retrains: {analysis.retrain_count}")
    print(f"Longest Recovery dwell: {analysis.longest_recovery_dwell:.3f} ms")
    print()
    
    print("State dwell times:")
    for state, dwell in sorted(analysis.state_dwells.items()):
        percentage = (dwell / analysis.total_time) * 100 if analysis.total_time > 0 else 0
        print(f"  {state:12}: {dwell:8.3f} ms ({percentage:5.1f}%)")
    
    if analysis.speed_changes:
        print(f"\nSpeed changes ({len(analysis.speed_changes)}):")
        for timestamp, old_speed, new_speed in analysis.speed_changes:
            print(f"  {timestamp:8.3f} ms: {old_speed} -> {new_speed}")

# Example usage and test
def create_sample_ltssm_trace():
    """Create a sample LTSSM trace for testing."""
    trace_data = [
        (0.000, "Detect", ""),
        (0.100, "Polling", ""),
        (0.500, "Config", "Gen1"),
        (2.000, "L0", "Gen1"),
        (5.000, "Recovery", ""),
        (5.200, "Config", "Gen2"),
        (6.000, "L0", "Gen2"),
        (10.000, "L0s", ""),
        (10.050, "L0", "Gen2"),
        (15.000, "Recovery", ""),
        (15.800, "Config", "Gen3"),
        (16.500, "L0", "Gen3"),
        (20.000, "Recovery", ""),
        (23.000, "L0", "Gen3"),
    ]
    
    with open('sample_ltssm.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'ltssm_state', 'additional_data'])
        for timestamp, state, data in trace_data:
            writer.writerow([timestamp, state, data])

def test_ltssm_parser():
    create_sample_ltssm_trace()
    analysis = parse_ltssm_trace('sample_ltssm.csv')
    print_ltssm_analysis(analysis)

if __name__ == "__main__":
    test_ltssm_parser()