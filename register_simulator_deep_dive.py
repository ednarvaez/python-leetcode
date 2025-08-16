"""
REGISTER SIMULATOR DEEP DIVE
Essential bit-level operations for Apple Silicon Validation Engineers
"""

# ============================================================================
# PART 1: Register Fundamentals in Hardware
# ============================================================================

def explain_register_fundamentals():
    """
    Understanding registers and their role in computer architecture
    """
    print("REGISTER FUNDAMENTALS IN COMPUTER ARCHITECTURE")
    print("=" * 50)
    
    print("🔧 WHAT ARE REGISTERS?")
    print("• Fast storage locations in CPU/processor")
    print("• Hold data temporarily during instruction execution")
    print("• Closest memory to processing units (fastest access)")
    print("• Typically 32-bit or 64-bit wide in modern processors")
    
    print("\n📊 REGISTER HIERARCHY:")
    hierarchy = [
        ("CPU Registers", "~1 cycle", "32-128 registers", "Instructions, data, addresses"),
        ("Cache L1", "~3 cycles", "32KB-64KB", "Recently used data/instructions"),
        ("Cache L2", "~10 cycles", "256KB-1MB", "Less recently used data"),
        ("Cache L3", "~40 cycles", "8MB-32MB", "Shared between cores"),
        ("Main Memory", "~300 cycles", "GB range", "System memory")
    ]
    
    print("Storage Type  | Access Time | Capacity    | Purpose")
    print("-" * 60)
    for storage, time, capacity, purpose in hierarchy:
        print(f"{storage:13} | {time:11} | {capacity:11} | {purpose}")
    
    print("\n🎯 APPLE SILICON REGISTER TYPES:")
    apple_registers = [
        "General Purpose: X0-X30 (64-bit ARM registers)",
        "SIMD/Vector: V0-V31 (128-bit NEON registers)", 
        "Neural Engine: Custom ML acceleration registers",
        "Secure Enclave: Cryptographic operation registers",
        "GPU: Shader execution unit registers",
        "System: Control, status, and configuration registers"
    ]
    
    for reg_type in apple_registers:
        print(f"  • {reg_type}")

def register_operations_overview():
    """
    Core register operations essential for validation
    """
    print("\n\nCORE REGISTER OPERATIONS")
    print("=" * 30)
    
    print("🔧 FUNDAMENTAL BIT OPERATIONS:")
    operations = [
        ("Set Bit", "reg |= (1 << pos)", "Turn on specific bit"),
        ("Clear Bit", "reg &= ~(1 << pos)", "Turn off specific bit"),
        ("Toggle Bit", "reg ^= (1 << pos)", "Flip specific bit"),
        ("Test Bit", "reg & (1 << pos)", "Check if bit is set"),
        ("Extract Field", "reg & mask", "Get specific bit range"),
        ("Insert Field", "(reg & ~mask) | val", "Set specific bit range"),
        ("Shift Left", "reg << count", "Multiply by 2^count"),
        ("Shift Right", "reg >> count", "Divide by 2^count")
    ]
    
    print("Operation    | Code Pattern        | Purpose")
    print("-" * 55)
    for op, code, purpose in operations:
        print(f"{op:12} | {code:20} | {purpose}")
    
    print("\n⚡ WHY THESE OPERATIONS MATTER:")
    print("• Hardware control: Enable/disable features")
    print("• Status monitoring: Check error conditions")
    print("• Data manipulation: Extract/insert bit fields")
    print("• Performance optimization: Bit-level arithmetic")
    print("• Debug support: Set breakpoints, trace flags")

# ============================================================================
# PART 2: Comprehensive Register Simulator Implementation
# ============================================================================

def comprehensive_register_simulator():
    """
    Advanced register simulator with complete functionality
    """
    print("\n\nCOMPREHENSIVE REGISTER SIMULATOR")
    print("=" * 35)
    
    class AdvancedRegisterSimulator:
        """
        Professional-grade register simulator for hardware validation
        """
        
        def __init__(self, width=32, name="REG"):
            self.width = width
            self.name = name
            self.value = 0
            self.max_value = (1 << width) - 1
            self.history = []  # Track register changes
            self.breakpoints = set()  # Bit positions to monitor
            
        def set_bit(self, position):
            """Set bit at position (hardware SET operation)"""
            if not self._validate_position(position):
                return False
                
            old_value = self.value
            self.value |= (1 << position)
            self._log_operation("SET", position, old_value, self.value)
            self._check_breakpoints(position, "SET")
            return True
        
        def clear_bit(self, position):
            """Clear bit at position (hardware CLEAR operation)"""
            if not self._validate_position(position):
                return False
                
            old_value = self.value
            self.value &= ~(1 << position)
            self._log_operation("CLEAR", position, old_value, self.value)
            self._check_breakpoints(position, "CLEAR")
            return True
        
        def toggle_bit(self, position):
            """Toggle bit at position (hardware TOGGLE operation)"""
            if not self._validate_position(position):
                return False
                
            old_value = self.value
            self.value ^= (1 << position)
            self._log_operation("TOGGLE", position, old_value, self.value)
            self._check_breakpoints(position, "TOGGLE")
            return True
        
        def test_bit(self, position):
            """Test if bit is set (hardware TEST operation)"""
            if not self._validate_position(position):
                return False
            return bool(self.value & (1 << position))
        
        def extract_field(self, start_bit, width):
            """Extract bit field (common in hardware register specs)"""
            if start_bit + width > self.width:
                print(f"Error: Field extends beyond register width")
                return None
                
            mask = (1 << width) - 1
            return (self.value >> start_bit) & mask
        
        def insert_field(self, start_bit, width, value):
            """Insert value into bit field (hardware field update)"""
            if start_bit + width > self.width:
                print(f"Error: Field extends beyond register width")
                return False
                
            if value >= (1 << width):
                print(f"Error: Value too large for {width}-bit field")
                return False
            
            old_value = self.value
            mask = ((1 << width) - 1) << start_bit
            self.value = (self.value & ~mask) | (value << start_bit)
            self._log_operation("INSERT_FIELD", f"{start_bit}:{start_bit+width-1}", old_value, self.value)
            return True
        
        def rotate_left(self, count):
            """Rotate bits left (circular shift)"""
            count %= self.width  # Handle counts larger than width
            old_value = self.value
            
            # Rotate left: high bits move to low positions
            self.value = ((self.value << count) | (self.value >> (self.width - count))) & self.max_value
            self._log_operation("ROTATE_LEFT", count, old_value, self.value)
        
        def rotate_right(self, count):
            """Rotate bits right (circular shift)"""
            count %= self.width
            old_value = self.value
            
            # Rotate right: low bits move to high positions  
            self.value = ((self.value >> count) | (self.value << (self.width - count))) & self.max_value
            self._log_operation("ROTATE_RIGHT", count, old_value, self.value)
        
        def count_set_bits(self):
            """Count number of 1 bits (population count)"""
            count = 0
            temp = self.value
            while temp:
                count += 1
                temp &= (temp - 1)  # Brian Kernighan's algorithm
            return count
        
        def find_first_set(self):
            """Find position of first set bit (hardware FFS instruction)"""
            if self.value == 0:
                return -1
            
            position = 0
            temp = self.value
            while (temp & 1) == 0:
                temp >>= 1
                position += 1
            return position
        
        def find_last_set(self):
            """Find position of last set bit (most significant)"""
            if self.value == 0:
                return -1
            return self.value.bit_length() - 1
        
        def set_breakpoint(self, position):
            """Set breakpoint on bit position for debugging"""
            if self._validate_position(position):
                self.breakpoints.add(position)
                print(f"Breakpoint set on bit {position}")
        
        def clear_breakpoint(self, position):
            """Clear breakpoint on bit position"""
            self.breakpoints.discard(position)
            print(f"Breakpoint cleared on bit {position}")
        
        def get_binary_string(self, group_size=4):
            """Get formatted binary representation"""
            binary = format(self.value, f'0{self.width}b')
            if group_size > 1:
                # Group bits for readability
                groups = [binary[i:i+group_size] for i in range(0, len(binary), group_size)]
                return ' '.join(groups)
            return binary
        
        def get_status_report(self):
            """Get comprehensive register status"""
            report = []
            report.append(f"Register: {self.name} ({self.width}-bit)")
            report.append(f"Value: 0x{self.value:0{self.width//4}X} ({self.value})")
            report.append(f"Binary: {self.get_binary_string()}")
            report.append(f"Set bits: {self.count_set_bits()}")
            
            if self.value > 0:
                report.append(f"First set bit: {self.find_first_set()}")
                report.append(f"Last set bit: {self.find_last_set()}")
            
            if self.breakpoints:
                report.append(f"Breakpoints: {sorted(self.breakpoints)}")
            
            return '\n'.join(report)
        
        def _validate_position(self, position):
            """Validate bit position is within register width"""
            if not (0 <= position < self.width):
                print(f"Error: Bit position {position} out of range [0, {self.width-1}]")
                return False
            return True
        
        def _log_operation(self, operation, position, old_value, new_value):
            """Log register operations for debugging"""
            self.history.append({
                'operation': operation,
                'position': position,
                'old_value': old_value,
                'new_value': new_value,
                'old_binary': format(old_value, f'0{self.width}b'),
                'new_binary': format(new_value, f'0{self.width}b')
            })
        
        def _check_breakpoints(self, position, operation):
            """Check if operation triggers breakpoint"""
            if position in self.breakpoints:
                print(f"🔴 BREAKPOINT HIT: {operation} on bit {position}")
                print(f"   Register: {self.get_binary_string()}")
    
    return AdvancedRegisterSimulator

def demonstrate_register_simulator():
    """
    Demonstrate the advanced register simulator
    """
    print("\n\nREGISTER SIMULATOR DEMONSTRATION")
    print("=" * 35)
    
    # Create register simulator class
    AdvancedRegisterSimulator = comprehensive_register_simulator()
    
    # Create a 16-bit control register
    control_reg = AdvancedRegisterSimulator(16, "CTRL_REG")
    
    print("🔧 BASIC OPERATIONS:")
    print(control_reg.get_status_report())
    
    print("\n--- Setting individual bits ---")
    control_reg.set_bit(0)    # Enable bit
    control_reg.set_bit(4)    # Clock enable
    control_reg.set_bit(8)    # Interrupt enable
    control_reg.set_bit(15)   # Master enable
    
    print(control_reg.get_status_report())
    
    print("\n--- Field operations ---")
    # Set 3-bit mode field (bits 1-3) to value 5
    control_reg.insert_field(1, 3, 5)
    mode = control_reg.extract_field(1, 3)
    print(f"Mode field (bits 1-3): {mode}")
    
    print(control_reg.get_status_report())
    
    print("\n--- Advanced operations ---")
    control_reg.rotate_left(2)
    print("After rotate left by 2:")
    print(control_reg.get_status_report())
    
    # Set breakpoint and trigger it
    control_reg.set_breakpoint(7)
    print("\n--- Triggering breakpoint ---")
    control_reg.set_bit(7)  # This will trigger breakpoint

# ============================================================================
# PART 3: Hardware Register Types and Applications
# ============================================================================

def hardware_register_types():
    """
    Different types of registers in computer systems
    """
    print("\n\nHARDWARE REGISTER TYPES")
    print("=" * 25)
    
    register_types = [
        {
            "type": "Control Registers",
            "purpose": "Configure hardware behavior",
            "examples": ["CPU control register", "DMA control", "Timer control"],
            "common_fields": ["Enable bits", "Mode selection", "Priority levels"]
        },
        {
            "type": "Status Registers", 
            "purpose": "Report hardware state",
            "examples": ["Interrupt status", "Error flags", "FIFO status"],
            "common_fields": ["Ready flags", "Error bits", "Count values"]
        },
        {
            "type": "Data Registers",
            "purpose": "Hold data for processing",
            "examples": ["UART data", "ADC result", "GPIO input"],
            "common_fields": ["Data payload", "Validity bits", "Timestamp"]
        },
        {
            "type": "Address Registers",
            "purpose": "Specify memory locations",
            "examples": ["DMA address", "Page table base", "Stack pointer"],
            "common_fields": ["Base address", "Offset", "Size"]
        }
    ]
    
    for reg_info in register_types:
        print(f"\n🔧 {reg_info['type'].upper()}:")
        print(f"   Purpose: {reg_info['purpose']}")
        print(f"   Examples: {', '.join(reg_info['examples'])}")
        print(f"   Common fields: {', '.join(reg_info['common_fields'])}")

def apple_silicon_register_examples():
    """
    Specific register examples from Apple Silicon
    """
    print("\n\nAPPLE SILICON REGISTER EXAMPLES")
    print("=" * 35)
    
    # Create register simulator class
    AdvancedRegisterSimulator = comprehensive_register_simulator()
    
    print("🧠 NEURAL ENGINE CONTROL REGISTER (Simulated)")
    ne_control = AdvancedRegisterSimulator(32, "NE_CTRL")
    
    # Simulate Neural Engine configuration
    ne_control.set_bit(0)                    # Enable Neural Engine
    ne_control.insert_field(1, 2, 2)        # Precision mode (2 = INT8)
    ne_control.insert_field(4, 4, 8)        # Number of cores (8)
    ne_control.insert_field(8, 8, 100)      # Clock divider (100 MHz)
    ne_control.set_bit(31)                   # Debug enable
    
    print("Neural Engine Control Register Configuration:")
    print(f"  Enable: {ne_control.test_bit(0)}")
    print(f"  Precision: {ne_control.extract_field(1, 2)}")
    print(f"  Active cores: {ne_control.extract_field(4, 4)}")
    print(f"  Clock divider: {ne_control.extract_field(8, 8)}")
    print(f"  Debug mode: {ne_control.test_bit(31)}")
    print(f"  Binary: {ne_control.get_binary_string()}")
    
    print("\n⚡ GPU SHADER UNIT STATUS (Simulated)")
    gpu_status = AdvancedRegisterSimulator(32, "GPU_STATUS")
    
    # Simulate GPU status bits
    gpu_status.insert_field(0, 8, 64)       # Active shader units (64)
    gpu_status.set_bit(16)                   # Thermal throttling
    gpu_status.insert_field(24, 8, 85)      # Utilization percentage
    
    print("GPU Status Register:")
    print(f"  Active units: {gpu_status.extract_field(0, 8)}")
    print(f"  Thermal throttling: {gpu_status.test_bit(16)}")
    print(f"  Utilization: {gpu_status.extract_field(24, 8)}%")
    print(f"  Binary: {gpu_status.get_binary_string()}")
    
    print("\n🔒 SECURE ENCLAVE CONFIGURATION (Simulated)")
    se_config = AdvancedRegisterSimulator(64, "SE_CONFIG")
    
    # Simulate Secure Enclave settings
    se_config.set_bit(0)                     # Secure boot enabled
    se_config.insert_field(1, 3, 4)         # Key size (4 = 256-bit)
    se_config.set_bit(8)                     # Hardware RNG enabled
    se_config.insert_field(16, 16, 12345)   # Session ID
    
    print("Secure Enclave Configuration:")
    print(f"  Secure boot: {se_config.test_bit(0)}")
    print(f"  Key size: {se_config.extract_field(1, 3)} (256-bit)")
    print(f"  Hardware RNG: {se_config.test_bit(8)}")
    print(f"  Session ID: {se_config.extract_field(16, 16)}")

# ============================================================================
# PART 4: Register Validation Techniques
# ============================================================================

def register_validation_techniques():
    """
    Professional techniques for validating register operations
    """
    print("\n\nREGISTER VALIDATION TECHNIQUES")
    print("=" * 35)
    
    # Create register simulator class  
    AdvancedRegisterSimulator = comprehensive_register_simulator()
    
    print("🔍 TECHNIQUE 1: Reset Value Verification")
    
    def verify_reset_values():
        """Verify registers reset to expected values"""
        expected_resets = {
            "CTRL_REG": 0x0000,
            "STATUS_REG": 0x8000,  # Ready bit set
            "CONFIG_REG": 0x0001   # Default enable
        }
        
        print("Verifying reset values:")
        print("Register    | Expected | Actual | Result")
        print("-" * 45)
        
        for reg_name, expected in expected_resets.items():
            reg = AdvancedRegisterSimulator(16, reg_name)
            if reg_name == "STATUS_REG":
                reg.set_bit(15)  # Simulate ready bit
            elif reg_name == "CONFIG_REG":
                reg.set_bit(0)   # Simulate default enable
            
            actual = reg.value
            result = "PASS" if actual == expected else "FAIL"
            print(f"{reg_name:11} | 0x{expected:04X}   | 0x{actual:04X} | {result}")
    
    verify_reset_values()
    
    print("\n🔍 TECHNIQUE 2: Read-Write Testing")
    
    def test_register_rw_capabilities():
        """Test read-write capabilities of register fields"""
        test_reg = AdvancedRegisterSimulator(32, "TEST_REG")
        
        test_patterns = [0x00000000, 0xFFFFFFFF, 0xAAAAAAAA, 0x55555555]
        
        print("Read-Write Testing:")
        print("Pattern    | Written  | Read Back | Match?")
        print("-" * 45)
        
        for pattern in test_patterns:
            test_reg.value = pattern & test_reg.max_value
            readback = test_reg.value
            match = "YES" if readback == pattern else "NO"
            print(f"0x{pattern:08X} | 0x{pattern:08X} | 0x{readback:08X}  | {match}")
    
    test_register_rw_capabilities()
    
    print("\n🔍 TECHNIQUE 3: Field Isolation Testing")
    
    def test_field_isolation():
        """Test that register fields don't interfere with each other"""
        field_reg = AdvancedRegisterSimulator(16, "FIELD_REG")
        
        # Define fields: [start_bit, width, name]
        fields = [
            (0, 2, "MODE"),
            (2, 4, "COUNT"), 
            (8, 3, "PRIORITY"),
            (12, 4, "STATUS")
        ]
        
        print("Field Isolation Testing:")
        print("Setting each field independently...")
        
        for start, width, name in fields:
            # Clear register
            field_reg.value = 0
            
            # Set test pattern in this field only
            test_value = (1 << width) - 1  # All 1s for this field
            field_reg.insert_field(start, width, test_value)
            
            # Verify other fields are still 0
            interference = False
            for other_start, other_width, other_name in fields:
                if other_start != start:
                    other_value = field_reg.extract_field(other_start, other_width)
                    if other_value != 0:
                        interference = True
                        break
            
            result = "ISOLATED" if not interference else "INTERFERENCE"
            print(f"  {name:8} field: {result}")
    
    test_field_isolation()
    
    print("\n🔍 TECHNIQUE 4: Stress Testing")
    
    def stress_test_register():
        """Perform stress testing on register operations"""
        stress_reg = AdvancedRegisterSimulator(32, "STRESS_REG")
        
        print("Stress Testing (1000 random operations):")
        
        import random
        operations = 0
        errors = 0
        
        for i in range(1000):
            op_type = random.choice(['set', 'clear', 'toggle'])
            position = random.randint(0, 31)
            
            old_value = stress_reg.value
            
            if op_type == 'set':
                stress_reg.set_bit(position)
                expected_bit = 1
            elif op_type == 'clear':
                stress_reg.clear_bit(position)
                expected_bit = 0
            else:  # toggle
                expected_bit = 1 - stress_reg.test_bit(position)
                stress_reg.toggle_bit(position)
            
            # Verify operation worked
            actual_bit = stress_reg.test_bit(position)
            if actual_bit != expected_bit:
                errors += 1
            
            operations += 1
        
        print(f"  Operations: {operations}")
        print(f"  Errors: {errors}")
        print(f"  Success rate: {((operations-errors)/operations)*100:.2f}%")
    
    stress_test_register()

# ============================================================================
# PART 5: Apple Interview Problems
# ============================================================================

def apple_interview_problems():
    """
    Register simulation problems for Apple Silicon validation interviews
    """
    print("\n\nAPPLE SILICON VALIDATION INTERVIEW PROBLEMS")
    print("=" * 50)
    
    problems = [
        {
            "title": "Power Management Register Design",
            "problem": "Design a 32-bit power control register with fields for voltage (8 bits), frequency (12 bits), and control flags",
            "solution": "Use bit field operations to pack multiple values efficiently",
            "skills": "Bit manipulation, field extraction/insertion, validation",
            "code_snippet": "reg.insert_field(0, 8, voltage); reg.insert_field(8, 12, freq);"
        },
        {
            "title": "Neural Engine Register Validation",
            "problem": "Validate that Neural Engine configuration registers maintain consistency across power cycles",
            "solution": "Compare register snapshots before/after power events",
            "skills": "State preservation, register comparison, error detection",
            "code_snippet": "snapshot = reg.value; power_cycle(); assert reg.value == snapshot"
        },
        {
            "title": "GPU Shader Unit Status Monitoring",
            "problem": "Monitor GPU shader utilization through status registers and detect anomalies",
            "solution": "Track register changes over time, identify unusual patterns",
            "skills": "Pattern recognition, statistical analysis, register history",
            "code_snippet": "history.append(reg.extract_field(0, 8)); detect_anomaly(history)"
        },
        {
            "title": "Secure Enclave Key Register Protection",
            "problem": "Implement register access controls to protect cryptographic keys",
            "solution": "Add permission checks and audit trails to register operations",
            "skills": "Security validation, access control, audit logging",
            "code_snippet": "if check_permission(user): reg.set_bit(pos); log_access(user, op)"
        }
    ]
    
    for i, prob in enumerate(problems, 1):
        print(f"\n🎯 PROBLEM {i}: {prob['title']}")
        print(f"   Challenge: {prob['problem']}")
        print(f"   Approach: {prob['solution']}")
        print(f"   Key Skills: {prob['skills']}")
        print(f"   Code Pattern: {prob['code_snippet']}")

# ============================================================================
# PART 6: Advanced Register Concepts
# ============================================================================

def advanced_register_concepts():
    """
    Advanced concepts in register design and validation
    """
    print("\n\nADVANCED REGISTER CONCEPTS")
    print("=" * 30)
    
    print("🚀 CONCEPT 1: Memory-Mapped Registers")
    print("Registers accessible through memory addresses")
    
    class MemoryMappedRegister:
        """Simulate memory-mapped register access"""
        
        def __init__(self, base_address, size=32):
            self.base_address = base_address
            self.size = size
            self.value = 0
            
        def write(self, address, value):
            """Write to register via memory address"""
            if address == self.base_address:
                self.value = value & ((1 << self.size) - 1)
                print(f"Write 0x{value:08X} to address 0x{address:08X}")
            else:
                print(f"Error: Invalid address 0x{address:08X}")
        
        def read(self, address):
            """Read from register via memory address"""
            if address == self.base_address:
                print(f"Read 0x{self.value:08X} from address 0x{address:08X}")
                return self.value
            else:
                print(f"Error: Invalid address 0x{address:08X}")
                return 0
    
    # Demo memory-mapped register
    gpio_reg = MemoryMappedRegister(0x40020000)  # GPIO base address
    gpio_reg.write(0x40020000, 0x12345678)
    value = gpio_reg.read(0x40020000)
    
    print("\n🚀 CONCEPT 2: Register Banking")
    print("Multiple register sets for context switching")
    
    class RegisterBank:
        """Simulate register banking for context switching"""
        
        def __init__(self, num_banks=4, reg_per_bank=32):
            self.num_banks = num_banks
            self.reg_per_bank = reg_per_bank
            self.banks = [[0] * reg_per_bank for _ in range(num_banks)]
            self.active_bank = 0
        
        def switch_bank(self, bank_id):
            """Switch to different register bank"""
            if 0 <= bank_id < self.num_banks:
                print(f"Switching from bank {self.active_bank} to bank {bank_id}")
                self.active_bank = bank_id
            else:
                print(f"Error: Invalid bank {bank_id}")
        
        def write_register(self, reg_id, value):
            """Write to register in active bank"""
            if 0 <= reg_id < self.reg_per_bank:
                self.banks[self.active_bank][reg_id] = value
                print(f"Bank {self.active_bank}, Reg {reg_id}: 0x{value:08X}")
            
        def read_register(self, reg_id):
            """Read from register in active bank"""
            if 0 <= reg_id < self.reg_per_bank:
                value = self.banks[self.active_bank][reg_id]
                return value
            return 0
    
    # Demo register banking
    reg_bank = RegisterBank(4, 16)
    reg_bank.write_register(0, 0xDEADBEEF)
    reg_bank.switch_bank(1)
    reg_bank.write_register(0, 0xCAFEBABE)
    reg_bank.switch_bank(0)
    value = reg_bank.read_register(0)
    print(f"Bank 0, Reg 0 value: 0x{value:08X}")
    
    print("\n🚀 CONCEPT 3: Shadow Registers")
    print("Backup registers for atomic updates")
    
    class ShadowRegister:
        """Register with shadow backup for atomic operations"""
        
        def __init__(self, width=32):
            self.width = width
            self.main_value = 0
            self.shadow_value = 0
            self.update_pending = False
        
        def write_shadow(self, value):
            """Write to shadow register"""
            self.shadow_value = value & ((1 << self.width) - 1)
            self.update_pending = True
            print(f"Shadow write: 0x{value:08X}")
        
        def commit_shadow(self):
            """Atomically commit shadow to main register"""
            if self.update_pending:
                self.main_value = self.shadow_value
                self.update_pending = False
                print(f"Shadow committed: 0x{self.main_value:08X}")
        
        def read_main(self):
            """Read from main register"""
            return self.main_value
    
    # Demo shadow register
    shadow_reg = ShadowRegister()
    shadow_reg.write_shadow(0x12345678)
    print(f"Main register before commit: 0x{shadow_reg.read_main():08X}")
    shadow_reg.commit_shadow()
    print(f"Main register after commit: 0x{shadow_reg.read_main():08X}")

# ============================================================================
# PART 7: Practice Exercises
# ============================================================================

def practice_exercises():
    """
    Hands-on register simulation exercises
    """
    print("\n\nREGISTER SIMULATION PRACTICE EXERCISES")
    print("=" * 42)
    
    exercises = [
        {
            "problem": "Design UART Control Register",
            "description": "Create 16-bit register with baud rate (12 bits), parity (2 bits), stop bits (1 bit), enable (1 bit)",
            "hint": "Use bit fields: [15:4] baud, [3:2] parity, [1] stop, [0] enable",
            "validation": "Test all combinations of settings"
        },
        {
            "problem": "Implement DMA Status Register",
            "description": "32-bit status with transfer count (16 bits), error flags (8 bits), control flags (8 bits)",
            "hint": "Monitor transfer progress and error conditions",
            "validation": "Verify flags update correctly during DMA operations"
        },
        {
            "problem": "Create Timer Configuration Register",
            "description": "Support multiple timer modes, prescaler values, and interrupt enables",
            "hint": "Pack mode (3 bits), prescaler (8 bits), interrupts (4 bits), enable (1 bit)",
            "validation": "Test timer behavior with different configurations"
        },
        {
            "problem": "Design Cache Control Register",
            "description": "Control cache policies, coherency, and performance monitoring",
            "hint": "Include cache size, replacement policy, coherency protocol bits",
            "validation": "Verify cache behavior matches register settings"
        }
    ]
    
    print("💪 Master these register design challenges:")
    for i, ex in enumerate(exercises, 1):
        print(f"\n📝 EXERCISE {i}: {ex['problem']}")
        print(f"   Description: {ex['description']}")
        print(f"   Hint: {ex['hint']}")
        print(f"   Validation: {ex['validation']}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("REGISTER SIMULATOR MASTERY FOR APPLE SILICON VALIDATION")
    print("=" * 60)
    
    explain_register_fundamentals()
    register_operations_overview()
    demonstrate_register_simulator()
    hardware_register_types()
    apple_silicon_register_examples()
    register_validation_techniques()
    apple_interview_problems()
    advanced_register_concepts()
    practice_exercises()
    
    print("\n" + "=" * 60)
    print("🎓 REGISTER SIMULATION MASTERY CHECKLIST:")
    print("✓ Understand register hierarchy and access patterns")
    print("✓ Master fundamental bit operations (set, clear, toggle, test)")
    print("✓ Implement field extraction and insertion efficiently")
    print("✓ Know validation techniques: reset, read-write, isolation")
    print("✓ Design registers for Apple Silicon components")
    print("✓ Handle advanced concepts: memory mapping, banking, shadows")
    print("✓ Apply to real hardware: GPU, Neural Engine, Secure Enclave")
    print("✓ Debug register operations with breakpoints and history")