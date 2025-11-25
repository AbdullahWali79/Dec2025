"""
Script to add 20 sample medicines with all required fields:
- Medicine Name
- MG (milligrams)
- Rack Number
- Price per Tablet
- Actual Price (for billing)
- Stock Quantity
"""

import pandas as pd
import os

# Sample medicines data
sample_medicines = [
    {"Medicine_Name": "Paracetamol", "MG": "500mg", "Rack_Number": "R001", "Price": 10.50, "Actual_Price": 10.50, "Stock": 100},
    {"Medicine_Name": "Ibuprofen", "MG": "400mg", "Rack_Number": "R002", "Price": 15.00, "Actual_Price": 15.00, "Stock": 80},
    {"Medicine_Name": "Aspirin", "MG": "100mg", "Rack_Number": "R003", "Price": 5.50, "Actual_Price": 5.50, "Stock": 150},
    {"Medicine_Name": "Amoxicillin", "MG": "250mg", "Rack_Number": "R004", "Price": 25.00, "Actual_Price": 25.00, "Stock": 60},
    {"Medicine_Name": "Ciprofloxacin", "MG": "500mg", "Rack_Number": "R005", "Price": 30.00, "Actual_Price": 30.00, "Stock": 45},
    {"Medicine_Name": "Metformin", "MG": "500mg", "Rack_Number": "R006", "Price": 8.00, "Actual_Price": 8.00, "Stock": 120},
    {"Medicine_Name": "Omeprazole", "MG": "20mg", "Rack_Number": "R007", "Price": 12.50, "Actual_Price": 12.50, "Stock": 90},
    {"Medicine_Name": "Atorvastatin", "MG": "10mg", "Rack_Number": "R008", "Price": 18.00, "Actual_Price": 18.00, "Stock": 70},
    {"Medicine_Name": "Amlodipine", "MG": "5mg", "Rack_Number": "R009", "Price": 9.50, "Actual_Price": 9.50, "Stock": 85},
    {"Medicine_Name": "Losartan", "MG": "50mg", "Rack_Number": "R010", "Price": 11.00, "Actual_Price": 11.00, "Stock": 75},
    {"Medicine_Name": "Levothyroxine", "MG": "50mcg", "Rack_Number": "R011", "Price": 7.50, "Actual_Price": 7.50, "Stock": 110},
    {"Medicine_Name": "Metoprolol", "MG": "25mg", "Rack_Number": "R012", "Price": 10.00, "Actual_Price": 10.00, "Stock": 95},
    {"Medicine_Name": "Furosemide", "MG": "40mg", "Rack_Number": "R013", "Price": 6.00, "Actual_Price": 6.00, "Stock": 130},
    {"Medicine_Name": "Warfarin", "MG": "5mg", "Rack_Number": "R014", "Price": 14.00, "Actual_Price": 14.00, "Stock": 55},
    {"Medicine_Name": "Simvastatin", "MG": "20mg", "Rack_Number": "R015", "Price": 16.50, "Actual_Price": 16.50, "Stock": 65},
    {"Medicine_Name": "Pantoprazole", "MG": "40mg", "Rack_Number": "R016", "Price": 13.00, "Actual_Price": 13.00, "Stock": 88},
    {"Medicine_Name": "Citalopram", "MG": "20mg", "Rack_Number": "R017", "Price": 20.00, "Actual_Price": 20.00, "Stock": 50},
    {"Medicine_Name": "Sertraline", "MG": "50mg", "Rack_Number": "R018", "Price": 22.00, "Actual_Price": 22.00, "Stock": 48},
    {"Medicine_Name": "Tramadol", "MG": "50mg", "Rack_Number": "R019", "Price": 17.50, "Actual_Price": 17.50, "Stock": 40},
    {"Medicine_Name": "Diclofenac", "MG": "50mg", "Rack_Number": "R020", "Price": 9.00, "Actual_Price": 9.00, "Stock": 105},
]

def add_sample_medicines():
    """Add sample medicines to the Excel file"""
    excel_file = 'medicines.xlsx'
    
    # Check if file exists
    if os.path.exists(excel_file):
        # Read existing data
        try:
            df = pd.read_excel(excel_file)
            print(f"Found existing file with {len(df)} medicines.")
            
            # Check if new columns exist, if not add them
            required_columns = ['Medicine_Name', 'Price', 'Stock', 'MG', 'Rack_Number', 'Actual_Price']
            for col in required_columns:
                if col not in df.columns:
                    if col == 'Actual_Price':
                        df[col] = df['Price']  # Default to Price
                    else:
                        df[col] = ''
            
            # Add sample medicines (only if they don't exist)
            new_medicines = []
            existing_names = df['Medicine_Name'].str.lower().tolist()
            
            for med in sample_medicines:
                if med['Medicine_Name'].lower() not in existing_names:
                    new_medicines.append(med)
                else:
                    print(f"Medicine '{med['Medicine_Name']}' already exists, skipping...")
            
            if new_medicines:
                new_df = pd.DataFrame(new_medicines)
                df = pd.concat([df, new_df], ignore_index=True)
                print(f"Added {len(new_medicines)} new medicines.")
            else:
                print("All sample medicines already exist in the file.")
                
        except Exception as e:
            print(f"Error reading existing file: {e}")
            print("Creating new file with sample medicines...")
            df = pd.DataFrame(sample_medicines)
    else:
        # Create new file
        print("Creating new medicines.xlsx file with 20 sample medicines...")
        df = pd.DataFrame(sample_medicines)
    
    # Save to Excel
    df.to_excel(excel_file, index=False)
    print(f"\nSuccessfully saved {len(df)} medicines to {excel_file}")
    print("\nSample medicines added:")
    for i, med in enumerate(sample_medicines[:5], 1):
        print(f"  {i}. {med['Medicine_Name']} ({med['MG']}) - Rack: {med['Rack_Number']}")
    print("  ... and 15 more medicines")
    print(f"\nTotal medicines in file: {len(df)}")

if __name__ == "__main__":
    add_sample_medicines()

