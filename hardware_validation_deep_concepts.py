"""
HARDWARE VALIDATION DEEP CONCEPTS
Advanced questions based on Apple/Nvidia interview feedback

CANDIDATE FEEDBACK ANALYSIS:
- "Better know exactly how shit works down to the physics"
- "Cache coherency, how to validate cache, etc."
- "Explaining device drivers in ridiculous detail down to the physics"
- "Very technically focused, lots of computer architecture questions"

This file covers the DEEP technical concepts that separate successful candidates
"""

import heapq
from typing import List, Dict, Tuple, Optional
from collections import defaultdict, deque

# ============================================================================
# PART 1: CACHE COHERENCY AND VALIDATION (Apple's Favorite Topic)
# ============================================================================

class CacheLineState:
    """
    MESI PROTOCOL SIMULATION
    
    Real interview question: "How do you validate cache coherency?"
    
    MESI States:
    - Modified (M): Cache has modified data, memory is stale
    - Exclusive (E): Cache has clean data, no other caches have it  
    - Shared (S): Cache has clean data, other caches may have it
    - Invalid (I): Cache line is invalid
    """
    MODIFIED = "M"
    EXCLUSIVE = "E" 
    SHARED = "S"
    INVALID = "I"

class CacheCoherencyValidator:
    """
    ADVANCED HARDWARE CONCEPT: Cache coherency validation
    
    INTERVIEW EXPECTATION: Explain how multiple CPU caches stay synchronized
    Real Apple question: "How do you test cache coherency in multi-core systems?"
    """
    
    def __init__(self, num_cores: int, cache_size: int):
        """
        Initialize cache coherency system
        
        PARAMETERS:
        num_cores: Number of CPU cores (each has L1 cache)
        cache_size: Number of cache lines per core
        """
        self.num_cores = num_cores
        self.cache_size = cache_size
        
        # Each core has cache with [address] -> (data, state)
        self.caches = [{}] for _ in range(num_cores)
        
        # Shared memory (main memory)
        self.memory = {}
        
        # Bus snooping log for validation
        self.bus_transactions = []
    
    def read_request(self, core_id: int, address: int) -> Tuple[int, str]:
        """
        CACHE READ OPERATION with MESI protocol
        
        ALGORITHM:
        1. Check local cache first
        2. If miss, check other caches (bus snooping)
        3. Update states according to MESI protocol
        4. Log transaction for validation
        
        RETURNS: (data, final_state)
        """
        cache = self.caches[core_id]
        
        # Cache hit case
        if address in cache:
            data, state = cache[address]
            self.bus_transactions.append(f"Core {core_id}: READ HIT {address} (state={state})")
            return data, state
        
        # Cache miss - need to fetch from memory or other caches
        self.bus_transactions.append(f"Core {core_id}: READ MISS {address}")
        
        # Check if other caches have this data (bus snooping)
        other_has_data = False
        other_modified = False
        
        for other_core in range(self.num_cores):
            if other_core != core_id and address in self.caches[other_core]:
                other_data, other_state = self.caches[other_core][address]
                other_has_data = True
                
                if other_state == CacheLineState.MODIFIED:
                    # Other cache has modified data - must write back to memory first
                    self.memory[address] = other_data
                    self.caches[other_core][address] = (other_data, CacheLineState.SHARED)
                    other_modified = True
                    self.bus_transactions.append(f"Core {other_core}: WRITEBACK {address}")
                
                elif other_state == CacheLineState.EXCLUSIVE:
                    # Change other cache from Exclusive to Shared
                    self.caches[other_core][address] = (other_data, CacheLineState.SHARED)
        
        # Get data from memory
        if address not in self.memory:
            self.memory[address] = 0  # Default value
        
        data = self.memory[address]
        
        # Determine new state for requesting cache
        if other_has_data:
            new_state = CacheLineState.SHARED  # Others have it, so shared
        else:
            new_state = CacheLineState.EXCLUSIVE  # Only we have it
        
        # Add to requesting cache
        cache[address] = (data, new_state)
        self.bus_transactions.append(f"Core {core_id}: LOADED {address} (state={new_state})")
        
        return data, new_state
    
    def write_request(self, core_id: int, address: int, data: int) -> str:
        """
        CACHE WRITE OPERATION with MESI protocol
        
        WRITE POLICY: Write-back with write-allocate
        
        ALGORITHM:
        1. If cache miss, first do read to get exclusive access
        2. Invalidate all other caches (send invalidation messages)
        3. Update local cache to Modified state
        4. Memory is now stale until write-back
        """
        cache = self.caches[core_id]
        
        # If not in cache, first read it to get exclusive access
        if address not in cache:
            self.read_request(core_id, address)
        
        # Invalidate all other caches that have this address
        for other_core in range(self.num_cores):
            if other_core != core_id and address in self.caches[other_core]:
                old_data, old_state = self.caches[other_core][address]
                
                if old_state == CacheLineState.MODIFIED:
                    # Other cache has modified data - write back first
                    self.memory[address] = old_data
                    self.bus_transactions.append(f"Core {other_core}: FORCED_WRITEBACK {address}")
                
                # Invalidate the other cache line
                del self.caches[other_core][address]
                self.bus_transactions.append(f"Core {other_core}: INVALIDATED {address}")
        
        # Update local cache with new data in Modified state
        cache[address] = (data, CacheLineState.MODIFIED)
        self.bus_transactions.append(f"Core {core_id}: WRITE {address}={data} (state=M)")
        
        return CacheLineState.MODIFIED
    
    def validate_coherency(self) -> List[str]:
        """
        VALIDATION FUNCTION: Check for cache coherency violations
        
        RULES TO CHECK:
        1. At most one cache can be in Modified state for any address
        2. If any cache is Modified, no other cache should have the address
        3. If multiple caches have same address, all must be in Shared state
        4. Modified data should eventually be written back to memory
        
        RETURNS: List of coherency violations found
        """
        violations = []
        
        # Track all addresses across all caches
        address_states = defaultdict(list)  # address -> [(core_id, state), ...]
        
        for core_id, cache in enumerate(self.caches):
            for address, (data, state) in cache.items():
                address_states[address].append((core_id, state, data))
        
        # Check coherency rules for each address
        for address, core_states in address_states.items():
            modified_count = 0
            exclusive_count = 0
            shared_cores = []
            
            for core_id, state, data in core_states:
                if state == CacheLineState.MODIFIED:
                    modified_count += 1
                elif state == CacheLineState.EXCLUSIVE:
                    exclusive_count += 1
                elif state == CacheLineState.SHARED:
                    shared_cores.append(core_id)
            
            # RULE 1: At most one Modified
            if modified_count > 1:
                violations.append(f"VIOLATION: Address {address} has {modified_count} Modified copies")
            
            # RULE 2: Modified excludes all others
            if modified_count > 0 and (exclusive_count > 0 or len(shared_cores) > 0):
                violations.append(f"VIOLATION: Address {address} is Modified but other caches have copies")
            
            # RULE 3: Exclusive excludes all others
            if exclusive_count > 0 and (modified_count > 0 or len(shared_cores) > 0):
                violations.append(f"VIOLATION: Address {address} is Exclusive but other caches have copies")
            
            # RULE 4: Multiple copies must all be Shared
            if len(core_states) > 1:
                non_shared = [state for _, state, _ in core_states if state != CacheLineState.SHARED]
                if non_shared:
                    violations.append(f"VIOLATION: Address {address} has multiple copies but not all Shared")
        
        return violations

# ============================================================================
# PART 2: MEMORY HIERARCHY AND TLB VALIDATION
# ============================================================================

class TLBEntry:
    """Translation Lookaside Buffer Entry"""
    def __init__(self, virtual_page: int, physical_page: int, valid: bool = True, dirty: bool = False):
        self.virtual_page = virtual_page    # Virtual page number
        self.physical_page = physical_page  # Physical page number  
        self.valid = valid                  # Valid bit
        self.dirty = dirty                  # Dirty bit (page has been written)
        self.access_time = 0               # For LRU replacement

class TLBValidator:
    """
    ADVANCED CONCEPT: Translation Lookaside Buffer validation
    
    Real interview question: "How do you validate virtual memory translation?"
    Expected knowledge: TLB hits/misses, page faults, memory protection
    """
    
    def __init__(self, tlb_size: int = 64):
        """
        Initialize TLB with specified number of entries
        
        TYPICAL TLB SIZES:
        - L1 TLB: 32-128 entries
        - L2 TLB: 512-1024 entries
        """
        self.tlb_size = tlb_size
        self.tlb = {}  # virtual_page -> TLBEntry
        self.access_counter = 0
        
        # Statistics for validation
        self.hits = 0
        self.misses = 0
        self.page_faults = 0
        
        # Page table (simplified - normally in OS)
        self.page_table = {}  # virtual_page -> physical_page
    
    def translate_address(self, virtual_address: int, page_size: int = 4096) -> Tuple[int, str]:
        """
        VIRTUAL TO PHYSICAL ADDRESS TRANSLATION
        
        PROCESS:
        1. Extract virtual page number from virtual address
        2. Check TLB for translation (fast path)
        3. If TLB miss, check page table (slow path)
        4. If page fault, handle allocation
        5. Update TLB with new translation
        
        RETURNS: (physical_address, status)
        """
        self.access_counter += 1
        
        # Extract page number and offset
        virtual_page = virtual_address // page_size
        offset = virtual_address % page_size
        
        # Check TLB first (fast path)
        if virtual_page in self.tlb:
            tlb_entry = self.tlb[virtual_page]
            if tlb_entry.valid:
                # TLB HIT
                self.hits += 1
                tlb_entry.access_time = self.access_counter  # Update for LRU
                physical_address = tlb_entry.physical_page * page_size + offset
                return physical_address, "TLB_HIT"
        
        # TLB MISS - check page table
        self.misses += 1
        
        if virtual_page not in self.page_table:
            # PAGE FAULT - page not allocated
            self.page_faults += 1
            # Simulate OS page allocation
            self.page_table[virtual_page] = self._allocate_physical_page()
            status = "PAGE_FAULT"
        else:
            status = "TLB_MISS"
        
        # Get physical page from page table
        physical_page = self.page_table[virtual_page]
        
        # Update TLB (may need to evict old entry)
        self._update_tlb(virtual_page, physical_page)
        
        physical_address = physical_page * page_size + offset
        return physical_address, status
    
    def _allocate_physical_page(self) -> int:
        """Simulate physical page allocation"""
        # In real systems, this involves complex memory management
        # For simulation, just use incremental allocation
        return len(self.page_table) + 1000  # Start at page 1000
    
    def _update_tlb(self, virtual_page: int, physical_page: int):
        """
        UPDATE TLB with new translation
        
        TLB REPLACEMENT POLICY: LRU (Least Recently Used)
        If TLB is full, evict the least recently used entry
        """
        # If TLB is full, need to evict an entry
        if len(self.tlb) >= self.tlb_size and virtual_page not in self.tlb:
            # Find LRU entry to evict
            lru_page = min(self.tlb.keys(), key=lambda vp: self.tlb[vp].access_time)
            del self.tlb[lru_page]
        
        # Add new entry
        self.tlb[virtual_page] = TLBEntry(virtual_page, physical_page)
        self.tlb[virtual_page].access_time = self.access_counter
    
    def get_statistics(self) -> Dict[str, float]:
        """
        TLB PERFORMANCE METRICS for validation
        
        KEY METRICS:
        - Hit rate: Percentage of TLB hits
        - Miss rate: Percentage of TLB misses  
        - Page fault rate: Percentage of page faults
        """
        total_accesses = self.hits + self.misses
        if total_accesses == 0:
            return {"hit_rate": 0.0, "miss_rate": 0.0, "page_fault_rate": 0.0}
        
        return {
            "hit_rate": (self.hits / total_accesses) * 100,
            "miss_rate": (self.misses / total_accesses) * 100,
            "page_fault_rate": (self.page_faults / total_accesses) * 100,
            "total_accesses": total_accesses
        }

# ============================================================================
# PART 3: OUT-OF-ORDER PIPELINE VALIDATION
# ============================================================================

class InstructionType:
    """Instruction types for pipeline simulation"""
    LOAD = "LOAD"
    STORE = "STORE"
    ALU = "ALU"
    BRANCH = "BRANCH"
    NOP = "NOP"

class Instruction:
    """Pipeline instruction representation"""
    def __init__(self, inst_type: str, src_regs: List[int], dest_reg: int, immediate: int = 0):
        self.type = inst_type
        self.src_regs = src_regs      # Source register dependencies
        self.dest_reg = dest_reg      # Destination register
        self.immediate = immediate    # Immediate value
        self.issued = False          # Has been issued to execution unit
        self.completed = False       # Has completed execution
        self.cycle_issued = -1       # Cycle when issued
        self.cycle_completed = -1    # Cycle when completed

class OutOfOrderProcessor:
    """
    OUT-OF-ORDER EXECUTION SIMULATION
    
    Real interview question: "How do you validate out-of-order pipelines?"
    
    CONCEPTS TESTED:
    - Register renaming
    - Instruction scheduling
    - Hazard detection
    - Speculation and recovery
    """
    
    def __init__(self, num_execution_units: int = 4, reorder_buffer_size: int = 16):
        """
        Initialize out-of-order processor
        
        COMPONENTS:
        - Reorder buffer: Maintains program order for commits
        - Reservation stations: Hold instructions waiting for operands
        - Register file: Architectural registers
        - Execution units: Functional units for computation
        """
        self.num_execution_units = num_execution_units
        self.reorder_buffer_size = reorder_buffer_size
        
        # Processor state
        self.reorder_buffer = deque()  # Instructions in program order
        self.reservation_stations = []  # Instructions waiting to execute
        self.execution_units = [None] * num_execution_units  # Currently executing
        self.register_file = [0] * 32  # 32 architectural registers
        self.register_busy = [False] * 32  # Register scoreboard
        
        # Statistics
        self.cycle = 0
        self.instructions_issued = 0
        self.instructions_completed = 0
        self.hazard_stalls = 0
    
    def issue_instruction(self, instruction: Instruction) -> bool:
        """
        INSTRUCTION ISSUE STAGE
        
        ALGORITHM:
        1. Check for structural hazards (reorder buffer full)
        2. Check for WAW hazards (write-after-write)
        3. Allocate reorder buffer entry
        4. Check for RAW hazards (read-after-write)
        5. If no hazards, issue to reservation station
        
        RETURNS: True if successfully issued, False if stalled
        """
        # Check structural hazard - reorder buffer full
        if len(self.reorder_buffer) >= self.reorder_buffer_size:
            self.hazard_stalls += 1
            return False
        
        # Check WAW hazard - destination register already busy
        if self.register_busy[instruction.dest_reg]:
            self.hazard_stalls += 1
            return False
        
        # Allocate reorder buffer entry
        self.reorder_buffer.append(instruction)
        
        # Mark destination register as busy
        self.register_busy[instruction.dest_reg] = True
        
        # Check RAW hazards - source registers busy
        ready_to_execute = True
        for src_reg in instruction.src_regs:
            if self.register_busy[src_reg]:
                ready_to_execute = False
                break
        
        # Issue instruction
        instruction.issued = True
        instruction.cycle_issued = self.cycle
        self.instructions_issued += 1
        
        if ready_to_execute:
            # Add to reservation station for immediate execution
            self.reservation_stations.append(instruction)
        
        return True
    
    def execute_cycle(self):
        """
        EXECUTE ONE PROCESSOR CYCLE
        
        PHASES:
        1. Commit completed instructions (in-order)
        2. Complete executing instructions
        3. Start new instructions on free execution units
        4. Update ready instructions in reservation stations
        """
        self.cycle += 1
        
        # PHASE 1: Commit completed instructions (head of reorder buffer)
        while (self.reorder_buffer and 
               self.reorder_buffer[0].completed):
            instruction = self.reorder_buffer.popleft()
            
            # Free destination register
            self.register_busy[instruction.dest_reg] = False
            
            # Update register file (simplified)
            if instruction.type != InstructionType.STORE:
                self.register_file[instruction.dest_reg] = instruction.immediate
        
        # PHASE 2: Complete instructions on execution units
        for i, instruction in enumerate(self.execution_units):
            if instruction is not None:
                # Simulate execution latency
                if self.cycle - instruction.cycle_issued >= self._get_latency(instruction.type):
                    instruction.completed = True
                    instruction.cycle_completed = self.cycle
                    self.instructions_completed += 1
                    self.execution_units[i] = None  # Free execution unit
        
        # PHASE 3: Start new instructions on free execution units
        ready_instructions = []
        for instruction in self.reservation_stations:
            # Check if all source operands are ready
            operands_ready = True
            for src_reg in instruction.src_regs:
                if self.register_busy[src_reg]:
                    operands_ready = False
                    break
            
            if operands_ready:
                ready_instructions.append(instruction)
        
        # Schedule ready instructions to free execution units
        for instruction in ready_instructions:
            # Find free execution unit
            for i, unit in enumerate(self.execution_units):
                if unit is None:
                    self.execution_units[i] = instruction
                    self.reservation_stations.remove(instruction)
                    break
    
    def _get_latency(self, inst_type: str) -> int:
        """Get execution latency for instruction type"""
        latencies = {
            InstructionType.ALU: 1,
            InstructionType.LOAD: 3,
            InstructionType.STORE: 1,
            InstructionType.BRANCH: 1,
            InstructionType.NOP: 1
        }
        return latencies.get(inst_type, 1)
    
    def validate_correctness(self, expected_results: Dict[int, int]) -> List[str]:
        """
        VALIDATE OUT-OF-ORDER EXECUTION CORRECTNESS
        
        CHECKS:
        1. Final register values match expected sequential execution
        2. No instruction was lost or duplicated  
        3. Dependencies were properly respected
        4. No deadlocks occurred
        """
        violations = []
        
        # Check final register values
        for reg, expected_value in expected_results.items():
            if self.register_file[reg] != expected_value:
                violations.append(f"Register R{reg}: expected {expected_value}, got {self.register_file[reg]}")
        
        # Check for deadlocks (instructions stuck in reservation stations)
        if self.reservation_stations:
            violations.append(f"Deadlock: {len(self.reservation_stations)} instructions stuck in reservation stations")
        
        # Check for incomplete execution
        incomplete = [inst for inst in self.reorder_buffer if not inst.completed]
        if incomplete:
            violations.append(f"Incomplete execution: {len(incomplete)} instructions not completed")
        
        return violations

# ============================================================================
# PART 4: TESTING AND VALIDATION SCENARIOS
# ============================================================================

def test_cache_coherency_validation():
    """Test cache coherency validation with MESI protocol"""
    print("TESTING CACHE COHERENCY VALIDATION")
    print("=" * 40)
    
    # Create 4-core system with cache coherency
    cache_system = CacheCoherencyValidator(num_cores=4, cache_size=16)
    
    # Simulate cache operations
    print("Simulating cache operations:")
    
    # Core 0 reads address 100
    data, state = cache_system.read_request(0, 100)
    print(f"Core 0 read addr 100: data={data}, state={state}")
    
    # Core 1 reads same address (should become shared)
    data, state = cache_system.read_request(1, 100)
    print(f"Core 1 read addr 100: data={data}, state={state}")
    
    # Core 0 writes to address 100 (should invalidate Core 1)
    state = cache_system.write_request(0, 100, 42)
    print(f"Core 0 write addr 100=42: state={state}")
    
    # Validate coherency
    violations = cache_system.validate_coherency()
    if violations:
        print("COHERENCY VIOLATIONS FOUND:")
        for violation in violations:
            print(f"  ❌ {violation}")
    else:
        print("✅ Cache coherency validated successfully")
    
    # Show bus transactions
    print("\nBus transaction log:")
    for transaction in cache_system.bus_transactions:
        print(f"  {transaction}")

def test_tlb_validation():
    """Test TLB validation with virtual memory"""
    print("\nTESTING TLB VALIDATION")
    print("=" * 25)
    
    # Create TLB validator
    tlb = TLBValidator(tlb_size=8)  # Small TLB for testing
    
    # Simulate memory accesses
    virtual_addresses = [0x1000, 0x2000, 0x1500, 0x3000, 0x1200, 0x4000, 0x2500, 0x5000, 0x1000]
    
    print("Virtual address translations:")
    for vaddr in virtual_addresses:
        paddr, status = tlb.translate_address(vaddr)
        print(f"  {vaddr:06x} → {paddr:06x} ({status})")
    
    # Show TLB statistics
    stats = tlb.get_statistics()
    print(f"\nTLB Performance:")
    print(f"  Hit rate: {stats['hit_rate']:.1f}%")
    print(f"  Miss rate: {stats['miss_rate']:.1f}%")
    print(f"  Page fault rate: {stats['page_fault_rate']:.1f}%")

def test_out_of_order_validation():
    """Test out-of-order processor validation"""
    print("\nTESTING OUT-OF-ORDER PROCESSOR")
    print("=" * 35)
    
    # Create processor
    processor = OutOfOrderProcessor(num_execution_units=2, reorder_buffer_size=8)
    
    # Create instruction sequence with dependencies
    instructions = [
        Instruction(InstructionType.LOAD, [0], 1, 10),    # R1 = MEM[R0] (load 10)
        Instruction(InstructionType.ALU, [1], 2, 5),      # R2 = R1 + 5 (depends on R1)
        Instruction(InstructionType.ALU, [0], 3, 20),     # R3 = R0 + 20 (independent)
        Instruction(InstructionType.ALU, [2, 3], 4, 0),   # R4 = R2 + R3 (depends on R2,R3)
    ]
    
    # Issue all instructions
    print("Issuing instructions:")
    for i, inst in enumerate(instructions):
        success = processor.issue_instruction(inst)
        print(f"  Instruction {i}: {'Issued' if success else 'Stalled'}")
    
    # Execute until completion
    print("\nExecution cycles:")
    max_cycles = 20
    cycle = 0
    while (processor.reorder_buffer or processor.reservation_stations or 
           any(unit is not None for unit in processor.execution_units)) and cycle < max_cycles:
        processor.execute_cycle()
        cycle += 1
        
        # Show processor state
        active_units = sum(1 for unit in processor.execution_units if unit is not None)
        print(f"  Cycle {processor.cycle}: {len(processor.reorder_buffer)} in ROB, "
              f"{len(processor.reservation_stations)} in RS, {active_units} executing")
    
    # Validate correctness
    expected_results = {1: 10, 2: 15, 3: 20, 4: 35}  # Expected final register values
    violations = processor.validate_correctness(expected_results)
    
    if violations:
        print("PROCESSOR VALIDATION VIOLATIONS:")
        for violation in violations:
            print(f"  ❌ {violation}")
    else:
        print("✅ Out-of-order execution validated successfully")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("HARDWARE VALIDATION DEEP CONCEPTS")
    print("=" * 45)
    print("Advanced topics for Apple/Nvidia silicon validation interviews")
    
    # Run validation tests
    test_cache_coherency_validation()
    test_tlb_validation()
    test_out_of_order_validation()
    
    print("\n" + "=" * 45)
    print("🎓 DEEP CONCEPTS MASTERY CHECKLIST:")
    print("✓ MESI cache coherency protocol and validation")
    print("✓ TLB operation and virtual memory translation")
    print("✓ Out-of-order execution and pipeline hazards")
    print("✓ Memory hierarchy and performance analysis")
    print("✓ Hardware validation methodologies")
    print("✓ Bus protocols and transaction logging")
    
    print("\n💡 INTERVIEW PREPARATION TIPS:")
    print("• Draw diagrams to explain cache states and transitions")
    print("• Understand the physics: transistors, capacitors, timing")
    print("• Know performance implications of each design choice")
    print("• Practice explaining complex concepts in simple terms")
    print("• Connect validation strategies to real silicon bugs")
    print("• Understand both pre-silicon and post-silicon validation")