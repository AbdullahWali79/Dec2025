"""
Simple script - just paste MAC ID here
"""

from machine_id_validator import MachineIDValidator
import hashlib

print("=" * 50)
print("CLIENT MAC ID ADD KARNE KA SIMPLE TARIKA")
print("=" * 50)

# Yahan client ka MAC ID paste karo
client_mac = "34-F3-9A-F5-1B-8F"  # <-- YAHAN PASTE KARO

# Client ka naam
client_name = "Client Laptop"  # <-- YAHAN CLIENT KA NAAM LIKHO

print(f"Client MAC ID: {client_mac}")
print(f"Client Name: {client_name}")

# Machine ID banate hain
validator = MachineIDValidator()
machine_id = hashlib.sha256(client_mac.encode()).hexdigest()[:16].upper()

print(f"Generated Machine ID: {machine_id}")

# Add karte hain
if validator.add_machine(machine_id, client_name):
    print("✅ SUCCESS! Client machine added!")
    
    # Updated list show karte hain
    print("\nAuthorized Machines:")
    machines = validator.list_authorized_machines()
    for i, machine in enumerate(machines, 1):
        print(f"{i}. {machine['name']} ({machine['id']})")
else:
    print("❌ Failed to add machine")

print("\n" + "=" * 50)
print("AB CLIENT KO YE FILES SEND KARO:")
print("1. PharmacyInvoiceGenerator.exe")
print("2. medicines.xlsx") 
print("3. authorized_machines.json")
print("=" * 50)
