"""
Simple script to add client MAC ID to authorized machines
"""

from machine_id_validator import MachineIDValidator
import hashlib

def add_client_mac():
    """Add client machine using MAC address from WhatsApp"""
    validator = MachineIDValidator()
    
    print("=" * 60)
    print("📱 ADD CLIENT MAC ID FROM WHATSAPP")
    print("=" * 60)
    
    # Get MAC address from user
    print("Paste the MAC ID that client sent you via WhatsApp:")
    print("Example: 34-F3-9A-F5-1B-8F")
    print()
    
    mac_address = input("MAC Address: ").strip()
    
    if not mac_address:
        print("❌ No MAC address entered!")
        return
    
    # Get machine name
    machine_name = input("Enter client name (e.g., Client Laptop): ").strip()
    if not machine_name:
        machine_name = "Client Machine"
    
    # Create machine ID from MAC address
    machine_id = hashlib.sha256(mac_address.encode()).hexdigest()[:16].upper()
    
    print(f"\nGenerated Machine ID: {machine_id}")
    
    # Add to authorized list
    if validator.add_machine(machine_id, machine_name):
        print(f"✅ Client machine '{machine_name}' added successfully!")
        print(f"Machine ID: {machine_id}")
        print(f"MAC Address: {mac_address}")
        
        # Show updated list
        print("\n📋 Updated Authorized Machines:")
        machines = validator.list_authorized_machines()
        for i, machine in enumerate(machines, 1):
            print(f"{i}. {machine['name']} ({machine['id']})")
    else:
        print("❌ Machine already exists or failed to add.")

if __name__ == "__main__":
    add_client_mac()
    input("\nPress Enter to exit...")
