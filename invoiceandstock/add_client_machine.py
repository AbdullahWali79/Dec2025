"""
Script to add client machine by MAC ID or Machine ID
"""

from machine_id_validator import MachineIDValidator
import hashlib

def add_client_by_mac():
    """Add client machine using MAC address"""
    validator = MachineIDValidator()
    
    print("=" * 60)
    print("👥 ADD CLIENT MACHINE")
    print("=" * 60)
    
    print("Enter client machine details:")
    machine_name = input("Machine Name (e.g., Client Laptop): ").strip()
    if not machine_name:
        machine_name = "Client Machine"
    
    print("\nChoose method to add machine:")
    print("1. By Machine ID (recommended)")
    print("2. By MAC Address")
    
    choice = input("Select option (1-2): ").strip()
    
    if choice == "1":
        # Add by Machine ID
        machine_id = input("Enter Machine ID: ").strip().upper()
        if machine_id:
            if validator.add_machine(machine_id, machine_name):
                print(f"✅ Client machine '{machine_name}' added successfully!")
                print(f"Machine ID: {machine_id}")
            else:
                print("❌ Machine already exists or failed to add.")
        else:
            print("❌ Invalid Machine ID.")
    
    elif choice == "2":
        # Add by MAC address
        mac_address = input("Enter MAC Address (e.g., 34-F3-9A-F5-1B-8F): ").strip()
        if mac_address:
            # Create a simple machine ID from MAC
            machine_id = hashlib.sha256(mac_address.encode()).hexdigest()[:16].upper()
            print(f"Generated Machine ID: {machine_id}")
            
            if validator.add_machine(machine_id, machine_name):
                print(f"✅ Client machine '{machine_name}' added successfully!")
                print(f"Machine ID: {machine_id}")
            else:
                print("❌ Machine already exists or failed to add.")
        else:
            print("❌ Invalid MAC Address.")
    
    else:
        print("❌ Invalid option.")
        return
    
    # Show updated list
    print("\n📋 Updated Authorized Machines:")
    machines = validator.list_authorized_machines()
    for i, machine in enumerate(machines, 1):
        print(f"{i}. {machine['name']} ({machine['id']})")

def show_current_machine_id():
    """Show current machine ID for sharing"""
    validator = MachineIDValidator()
    current_id = validator.get_machine_id()
    
    print("=" * 60)
    print("🖥️  YOUR MACHINE ID")
    print("=" * 60)
    print(f"Machine ID: {current_id}")
    print("\nShare this ID with the administrator to authorize this machine.")
    print("=" * 60)

def main():
    """Main menu"""
    while True:
        print("\n" + "=" * 60)
        print("👥 CLIENT MACHINE MANAGEMENT")
        print("=" * 60)
        print("1. Add client machine")
        print("2. Show my machine ID")
        print("3. List authorized machines")
        print("4. Exit")
        print("=" * 60)
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == "1":
            add_client_by_mac()
        elif choice == "2":
            show_current_machine_id()
        elif choice == "3":
            validator = MachineIDValidator()
            machines = validator.list_authorized_machines()
            print("\n📋 Authorized Machines:")
            for i, machine in enumerate(machines, 1):
                print(f"{i}. {machine['name']} ({machine['id']})")
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
