"""
Secure Machine ID Validator - Hardcoded machine IDs
Client cannot see or modify these machine IDs
"""

import hashlib
import platform
import subprocess
import uuid
import os

class SecureMachineValidator:
    def __init__(self):
        # HARDCODED MACHINE IDs - CLIENT CANNOT SEE OR CHANGE THESE
        # These IDs are embedded in the code and cannot be modified by client
        self.authorized_machine_ids = [
            "B1D1FC64C865533F",  # Main development machine
            "63962CB948526976",  # Client machine 1
            "AC090693E5",        # MacBook Client (ac:c9:06:09:93:e5)
            # Additional machine IDs can only be added by developer
        ]
    
    def get_machine_id(self):
        """Generate a unique machine ID based on hardware characteristics"""
        try:
            # Get system information
            system_info = {
                'platform': platform.platform(),
                'processor': platform.processor(),
                'machine': platform.machine(),
                'node': platform.node(),
            }
            
            # Get MAC address
            mac = uuid.getnode()
            mac_str = ':'.join(['{:02x}'.format((mac >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
            
            # Get CPU ID (Windows)
            cpu_id = ""
            try:
                if platform.system() == "Windows":
                    result = subprocess.run(['wmic', 'cpu', 'get', 'ProcessorId', '/value'], 
                                          capture_output=True, text=True, timeout=10)
                    for line in result.stdout.split('\n'):
                        if 'ProcessorId' in line:
                            cpu_id = line.split('=')[1].strip()
                            break
            except:
                pass
            
            # Get motherboard serial (Windows)
            motherboard_serial = ""
            try:
                if platform.system() == "Windows":
                    result = subprocess.run(['wmic', 'baseboard', 'get', 'serialnumber', '/value'], 
                                          capture_output=True, text=True, timeout=10)
                    for line in result.stdout.split('\n'):
                        if 'SerialNumber' in line:
                            motherboard_serial = line.split('=')[1].strip()
                            break
            except:
                pass
            
            # Combine all information
            machine_string = f"{system_info['platform']}-{system_info['processor']}-{system_info['machine']}-{system_info['node']}-{mac_str}-{cpu_id}-{motherboard_serial}"
            
            # Create hash
            machine_id = hashlib.sha256(machine_string.encode()).hexdigest()[:16]
            return machine_id.upper()
            
        except Exception as e:
            # Fallback to basic machine ID
            return hashlib.sha256(f"{platform.node()}-{uuid.getnode()}".encode()).hexdigest()[:16].upper()
    
    def is_machine_authorized(self):
        """Check if current machine is authorized"""
        current_machine_id = self.get_machine_id()
        return current_machine_id in self.authorized_machine_ids
    
    def get_current_machine_id(self):
        """Get current machine ID for display purposes"""
        return self.get_machine_id()

def validate_machine_access():
    """Main function to validate machine access"""
    validator = SecureMachineValidator()
    
    if not validator.is_machine_authorized():
        current_machine_id = validator.get_machine_id()
        print("=" * 60)
        print("🚫 UNAUTHORIZED MACHINE ACCESS")
        print("=" * 60)
        print(f"Machine ID: {current_machine_id}")
        print("This application is not authorized to run on this machine.")
        print("Please contact the administrator to add this machine.")
        print("=" * 60)
        input("Press Enter to exit...")
        return False
    
    return True

if __name__ == "__main__":
    # Test the machine ID system
    validator = SecureMachineValidator()
    current_id = validator.get_machine_id()
    print(f"Current Machine ID: {current_id}")
    print(f"Is Authorized: {validator.is_machine_authorized()}")
    print(f"Authorized Machines: {len(validator.authorized_machine_ids)} machines")
