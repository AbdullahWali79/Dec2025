"""
Secure way to add client machine ID - for development only
This script helps you add client machine IDs to the hardcoded list
"""

from secure_machine_validator import SecureMachineValidator
import hashlib

def add_client_machine():
    """Add client machine ID to hardcoded list"""
    print("=" * 60)
    print("🔒 ADD CLIENT MACHINE ID (SECURE METHOD)")
    print("=" * 60)
    
    print("Enter client machine details:")
    client_name = input("Client Name: ").strip()
    if not client_name:
        client_name = "Client Machine"
    
    print("\nChoose method:")
    print("1. By Machine ID (recommended)")
    print("2. By MAC Address")
    
    choice = input("Select option (1-2): ").strip()
    
    if choice == "1":
        machine_id = input("Enter Machine ID: ").strip().upper()
        if machine_id:
            print(f"\nMachine ID: {machine_id}")
            print("Client Name: {client_name}")
            
            # Show the code to add to secure_machine_validator.py
            print("\n" + "=" * 60)
            print("📝 ADD THIS LINE TO secure_machine_validator.py:")
            print("=" * 60)
            print(f'            "{machine_id}",  # {client_name}')
            print("=" * 60)
            
            print("\nSteps to add:")
            print("1. Open secure_machine_validator.py")
            print("2. Find the authorized_machine_ids list")
            print("3. Add the line above")
            print("4. Save the file")
            print("5. Rebuild the executable")
            
        else:
            print("❌ Invalid Machine ID.")
    
    elif choice == "2":
        mac_address = input("Enter MAC Address: ").strip()
        if mac_address:
            machine_id = hashlib.sha256(mac_address.encode()).hexdigest()[:16].upper()
            print(f"\nGenerated Machine ID: {machine_id}")
            print("Client Name: {client_name}")
            
            # Show the code to add to secure_machine_validator.py
            print("\n" + "=" * 60)
            print("📝 ADD THIS LINE TO secure_machine_validator.py:")
            print("=" * 60)
            print(f'            "{machine_id}",  # {client_name}')
            print("=" * 60)
            
            print("\nSteps to add:")
            print("1. Open secure_machine_validator.py")
            print("2. Find the authorized_machine_ids list")
            print("3. Add the line above")
            print("4. Save the file")
            print("5. Rebuild the executable")
            
        else:
            print("❌ Invalid MAC Address.")
    
    else:
        print("❌ Invalid option.")

if __name__ == "__main__":
    add_client_machine()
    input("\nPress Enter to exit...")
