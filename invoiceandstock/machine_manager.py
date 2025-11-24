"""
Machine ID Management Tool
This tool helps manage authorized machines for the Pharmacy Invoice Generator
"""

import json
import os
from machine_id_validator import MachineIDValidator

class MachineManager:
    def __init__(self):
        self.validator = MachineIDValidator()
    
    def show_current_machine_info(self):
        """Display current machine information"""
        current_id = self.validator.get_machine_id()
        is_authorized = self.validator.is_machine_authorized()
        
        print("=" * 60)
        print("🖥️  CURRENT MACHINE INFORMATION")
        print("=" * 60)
        print(f"Machine ID: {current_id}")
        print(f"Status: {'✅ AUTHORIZED' if is_authorized else '❌ NOT AUTHORIZED'}")
        print("=" * 60)
        
        return current_id, is_authorized
    
    def list_authorized_machines(self):
        """List all authorized machines"""
        machines = self.validator.list_authorized_machines()
        
        print("=" * 60)
        print("📋 AUTHORIZED MACHINES")
        print("=" * 60)
        
        if not machines:
            print("No authorized machines found.")
        else:
            for i, machine in enumerate(machines, 1):
                print(f"{i}. {machine['name']}")
                print(f"   ID: {machine['id']}")
                print()
        
        print("=" * 60)
        return machines
    
    def add_current_machine(self, machine_name=None):
        """Add current machine to authorized list"""
        current_id = self.validator.get_machine_id()
        
        if machine_name is None:
            machine_name = input("Enter a name for this machine: ").strip()
            if not machine_name:
                machine_name = "Unknown Machine"
        
        if self.validator.add_machine(current_id, machine_name):
            print(f"✅ Machine '{machine_name}' added successfully!")
            print(f"Machine ID: {current_id}")
        else:
            print("❌ Machine already exists in authorized list.")
    
    def add_remote_machine(self):
        """Add a remote machine by ID"""
        print("Enter the Machine ID of the remote machine:")
        machine_id = input("Machine ID: ").strip().upper()
        
        if not machine_id:
            print("❌ Invalid Machine ID.")
            return
        
        machine_name = input("Enter a name for this machine: ").strip()
        if not machine_name:
            machine_name = "Remote Machine"
        
        if self.validator.add_machine(machine_id, machine_name):
            print(f"✅ Remote machine '{machine_name}' added successfully!")
            print(f"Machine ID: {machine_id}")
        else:
            print("❌ Machine already exists in authorized list.")
    
    def remove_machine(self):
        """Remove a machine from authorized list"""
        machines = self.validator.list_authorized_machines()
        
        if not machines:
            print("❌ No authorized machines to remove.")
            return
        
        print("Select machine to remove:")
        for i, machine in enumerate(machines, 1):
            print(f"{i}. {machine['name']} ({machine['id']})")
        
        try:
            choice = int(input("Enter number: ")) - 1
            if 0 <= choice < len(machines):
                machine = machines[choice]
                if self.validator.remove_machine(machine['id']):
                    print(f"✅ Machine '{machine['name']}' removed successfully!")
                else:
                    print("❌ Failed to remove machine.")
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Invalid input.")
    
    def export_machine_list(self):
        """Export machine list to a text file"""
        machines = self.validator.list_authorized_machines()
        
        filename = "authorized_machines_export.txt"
        with open(filename, 'w') as f:
            f.write("AUTHORIZED MACHINES LIST\n")
            f.write("=" * 50 + "\n\n")
            
            for i, machine in enumerate(machines, 1):
                f.write(f"{i}. {machine['name']}\n")
                f.write(f"   Machine ID: {machine['id']}\n\n")
        
        print(f"✅ Machine list exported to {filename}")
    
    def main_menu(self):
        """Display main menu and handle user input"""
        while True:
            print("\n" + "=" * 60)
            print("🔧 MACHINE ID MANAGEMENT TOOL")
            print("=" * 60)
            print("1. Show current machine info")
            print("2. List authorized machines")
            print("3. Add current machine")
            print("4. Add remote machine")
            print("5. Remove machine")
            print("6. Export machine list")
            print("7. Exit")
            print("=" * 60)
            
            choice = input("Select option (1-7): ").strip()
            
            if choice == '1':
                self.show_current_machine_info()
            elif choice == '2':
                self.list_authorized_machines()
            elif choice == '3':
                self.add_current_machine()
            elif choice == '4':
                self.add_remote_machine()
            elif choice == '5':
                self.remove_machine()
            elif choice == '6':
                self.export_machine_list()
            elif choice == '7':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option. Please try again.")
            
            input("\nPress Enter to continue...")

def main():
    """Main function"""
    manager = MachineManager()
    manager.main_menu()

if __name__ == "__main__":
    main()
