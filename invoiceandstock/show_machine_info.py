"""
Script to show current machine information and authorized machines
"""

from machine_id_validator import MachineIDValidator
import subprocess
import platform

def get_mac_addresses():
    """Get MAC addresses using getmac command"""
    try:
        result = subprocess.run(['getmac'], capture_output=True, text=True, timeout=10)
        return result.stdout
    except Exception as e:
        return f"Error getting MAC addresses: {e}"

def show_machine_info():
    """Show comprehensive machine information"""
    validator = MachineIDValidator()
    
    print("=" * 80)
    print("🖥️  MACHINE INFORMATION & AUTHORIZATION STATUS")
    print("=" * 80)
    
    # Current machine ID
    current_id = validator.get_machine_id()
    is_authorized = validator.is_machine_authorized()
    
    print(f"Machine ID: {current_id}")
    print(f"Status: {'✅ AUTHORIZED' if is_authorized else '❌ NOT AUTHORIZED'}")
    print()
    
    # System information
    print("📋 SYSTEM INFORMATION:")
    print(f"Platform: {platform.platform()}")
    print(f"Processor: {platform.processor()}")
    print(f"Machine: {platform.machine()}")
    print(f"Node: {platform.node()}")
    print()
    
    # MAC addresses
    print("🌐 MAC ADDRESSES:")
    mac_info = get_mac_addresses()
    print(mac_info)
    
    # Authorized machines
    print("🔐 AUTHORIZED MACHINES:")
    machines = validator.list_authorized_machines()
    if machines:
        for i, machine in enumerate(machines, 1):
            status = "🟢 CURRENT" if machine['id'] == current_id else "🔵 OTHER"
            print(f"{i}. {machine['name']} {status}")
            print(f"   ID: {machine['id']}")
            print()
    else:
        print("No authorized machines found.")
    
    print("=" * 80)

if __name__ == "__main__":
    show_machine_info()
    input("\nPress Enter to exit...")
