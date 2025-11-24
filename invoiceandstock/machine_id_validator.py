import hashlib
import platform
import subprocess
import uuid
import os
import json

class MachineIDValidator:
    def __init__(self):
        self.config_file = "authorized_machines.json"
        # Hardcoded authorized machine IDs - client cannot see or change these
        self.hardcoded_machines = [
            "B1D1FC64C865533F",  # Your main development machine
            "63962CB948526976",  # Client machine (example)
            # Add more machine IDs here as needed
        ]
        self.authorized_machines = self.load_authorized_machines()
    
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
    
    def load_authorized_machines(self):
        """Load authorized machine IDs from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                # Create default config with current machine
                current_machine_id = self.get_machine_id()
                default_config = {
                    "authorized_machines": [current_machine_id],
                    "machine_names": {
                        current_machine_id: "Main Development Machine"
                    }
                }
                self.save_authorized_machines(default_config)
                return default_config
        except Exception as e:
            print(f"Error loading authorized machines: {e}")
            return {"authorized_machines": [], "machine_names": {}}
    
    def save_authorized_machines(self, config=None):
        """Save authorized machine IDs to config file"""
        try:
            if config is None:
                config = self.authorized_machines
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving authorized machines: {e}")
    
    def is_machine_authorized(self):
        """Check if current machine is authorized"""
        current_machine_id = self.get_machine_id()
        # Check both hardcoded machines and JSON file
        return (current_machine_id in self.hardcoded_machines or 
                current_machine_id in self.authorized_machines.get("authorized_machines", []))
    
    def add_machine(self, machine_id, machine_name="Unknown Machine"):
        """Add a new machine to authorized list"""
        if machine_id not in self.authorized_machines.get("authorized_machines", []):
            self.authorized_machines["authorized_machines"].append(machine_id)
            self.authorized_machines["machine_names"][machine_id] = machine_name
            self.save_authorized_machines()
            return True
        return False
    
    def remove_machine(self, machine_id):
        """Remove a machine from authorized list"""
        if machine_id in self.authorized_machines.get("authorized_machines", []):
            self.authorized_machines["authorized_machines"].remove(machine_id)
            if machine_id in self.authorized_machines.get("machine_names", {}):
                del self.authorized_machines["machine_names"][machine_id]
            self.save_authorized_machines()
            return True
        return False
    
    def get_machine_name(self, machine_id):
        """Get the name associated with a machine ID"""
        return self.authorized_machines.get("machine_names", {}).get(machine_id, "Unknown Machine")
    
    def list_authorized_machines(self):
        """Get list of all authorized machines"""
        machines = []
        for machine_id in self.authorized_machines.get("authorized_machines", []):
            machines.append({
                "id": machine_id,
                "name": self.get_machine_name(machine_id)
            })
        return machines

def validate_machine_access():
    """Main function to validate machine access"""
    validator = MachineIDValidator()
    
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
    validator = MachineIDValidator()
    current_id = validator.get_machine_id()
    print(f"Current Machine ID: {current_id}")
    print(f"Is Authorized: {validator.is_machine_authorized()}")
    print(f"Authorized Machines: {validator.list_authorized_machines()}")
