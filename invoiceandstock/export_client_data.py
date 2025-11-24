"""
Client Data Export Tool
Exports client machine data in multiple formats (JSON, CSV, Excel)
"""

import json
import csv
import pandas as pd
from datetime import datetime
import os
from machine_id_validator import MachineIDValidator

class ClientDataExporter:
    def __init__(self):
        self.validator = MachineIDValidator()
        self.export_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def get_client_data(self):
        """Get all client machine data"""
        try:
            machines = self.validator.list_authorized_machines()
            client_data = []
            
            for machine in machines:
                client_data.append({
                    'machine_id': machine['id'],
                    'machine_name': machine['name'],
                    'export_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'status': 'Authorized'
                })
            
            return client_data
        except Exception as e:
            print(f"❌ Error getting client data: {str(e)}")
            return []
    
    def export_to_json(self, data, filename=None):
        """Export client data to JSON format"""
        if not filename:
            filename = f"client_data_export_{self.export_timestamp}.json"
        
        try:
            export_data = {
                'export_info': {
                    'export_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'total_clients': len(data),
                    'exported_by': 'Pharmacy System'
                },
                'clients': data
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            
            print(f"✅ JSON export successful: {filename}")
            return filename
        except Exception as e:
            print(f"❌ JSON export failed: {str(e)}")
            return None
    
    def export_to_csv(self, data, filename=None):
        """Export client data to CSV format"""
        if not filename:
            filename = f"client_data_export_{self.export_timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if data:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
            
            print(f"✅ CSV export successful: {filename}")
            return filename
        except Exception as e:
            print(f"❌ CSV export failed: {str(e)}")
            return None
    
    def export_to_excel(self, data, filename=None):
        """Export client data to Excel format"""
        if not filename:
            filename = f"client_data_export_{self.export_timestamp}.xlsx"
        
        try:
            df = pd.DataFrame(data)
            
            # Create Excel writer with multiple sheets
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Main data sheet
                df.to_excel(writer, sheet_name='Client_Data', index=False)
                
                # Summary sheet
                summary_data = {
                    'Export_Date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    'Total_Clients': [len(data)],
                    'Export_Format': ['Excel'],
                    'System': ['Pharmacy Invoice Generator']
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Export_Summary', index=False)
            
            print(f"✅ Excel export successful: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Excel export failed: {str(e)}")
            return None
    
    def export_all_formats(self):
        """Export client data in all available formats"""
        print("=" * 60)
        print("📊 CLIENT DATA EXPORT")
        print("=" * 60)
        
        # Get client data
        client_data = self.get_client_data()
        
        if not client_data:
            print("❌ No client data found to export!")
            return
        
        print(f"📋 Found {len(client_data)} client(s) to export")
        print("\nExporting in multiple formats...")
        
        # Export to all formats
        json_file = self.export_to_json(client_data)
        csv_file = self.export_to_csv(client_data)
        excel_file = self.export_to_excel(client_data)
        
        # Show export summary
        print("\n" + "=" * 60)
        print("📁 EXPORT SUMMARY")
        print("=" * 60)
        
        exported_files = []
        if json_file:
            exported_files.append(json_file)
        if csv_file:
            exported_files.append(csv_file)
        if excel_file:
            exported_files.append(excel_file)
        
        if exported_files:
            print("✅ Successfully exported to:")
            for file in exported_files:
                file_path = os.path.abspath(file)
                print(f"   📄 {file_path}")
        else:
            print("❌ No files were exported successfully")
        
        return exported_files
    
    def show_client_list(self):
        """Display current client list"""
        print("=" * 60)
        print("👥 CURRENT CLIENT LIST")
        print("=" * 60)
        
        client_data = self.get_client_data()
        
        if not client_data:
            print("❌ No clients found!")
            return
        
        for i, client in enumerate(client_data, 1):
            print(f"{i}. {client['machine_name']}")
            print(f"   Machine ID: {client['machine_id']}")
            print(f"   Status: {client['status']}")
            print()
    
    def export_specific_format(self, format_type):
        """Export in specific format only"""
        client_data = self.get_client_data()
        
        if not client_data:
            print("❌ No client data found to export!")
            return
        
        if format_type.lower() == 'json':
            return self.export_to_json(client_data)
        elif format_type.lower() == 'csv':
            return self.export_to_csv(client_data)
        elif format_type.lower() == 'excel':
            return self.export_to_excel(client_data)
        else:
            print("❌ Invalid format. Use: json, csv, or excel")
            return None

def main():
    """Main menu for client data export"""
    exporter = ClientDataExporter()
    
    while True:
        print("\n" + "=" * 60)
        print("📊 CLIENT DATA EXPORT TOOL")
        print("=" * 60)
        print("1. Show current client list")
        print("2. Export all formats (JSON, CSV, Excel)")
        print("3. Export JSON only")
        print("4. Export CSV only")
        print("5. Export Excel only")
        print("6. Exit")
        print("=" * 60)
        
        choice = input("Select option (1-6): ").strip()
        
        if choice == "1":
            exporter.show_client_list()
        elif choice == "2":
            exporter.export_all_formats()
        elif choice == "3":
            exporter.export_specific_format('json')
        elif choice == "4":
            exporter.export_specific_format('csv')
        elif choice == "5":
            exporter.export_specific_format('excel')
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
