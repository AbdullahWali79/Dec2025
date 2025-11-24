"""
Script to automatically add current machine to authorized list
"""

from machine_id_validator import MachineIDValidator

def add_current_machine():
    """Add current machine to authorized list"""
    validator = MachineIDValidator()
    
    # Get current machine ID
    current_id = validator.get_machine_id()
    
    print("=" * 60)
    print("🖥️  ADDING CURRENT MACHINE TO AUTHORIZED LIST")
    print("=" * 60)
    print(f"Machine ID: {current_id}")
    
    # Check if already authorized
    if validator.is_machine_authorized():
        print("✅ This machine is already authorized!")
        return True
    
    # Add machine with a descriptive name
    machine_name = "Main Development Machine"
    if validator.add_machine(current_id, machine_name):
        print(f"✅ Machine '{machine_name}' added successfully!")
        print(f"Machine ID: {current_id}")
        
        # Show updated list
        print("\n📋 Updated Authorized Machines:")
        machines = validator.list_authorized_machines()
        for i, machine in enumerate(machines, 1):
            print(f"{i}. {machine['name']} ({machine['id']})")
        
        return True
    else:
        print("❌ Failed to add machine.")
        return False

if __name__ == "__main__":
    add_current_machine()
    input("\nPress Enter to exit...")
