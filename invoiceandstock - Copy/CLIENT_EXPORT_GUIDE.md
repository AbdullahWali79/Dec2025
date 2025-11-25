# 📊 Client Data Export Guide

## Overview
The client data export functionality allows you to export all authorized client machine information in multiple formats (JSON, CSV, Excel).

## How to Use

### Method 1: From Main Application
1. Open the Pharmacy Invoice Generator application
2. Click the **"📊 Export Clients (F7)"** button
3. Select your preferred export format:
   - **All Formats**: Exports JSON, CSV, and Excel files
   - **JSON Only**: Exports structured JSON data
   - **CSV Only**: Exports comma-separated values
   - **Excel Only**: Exports Excel spreadsheet with multiple sheets
4. Click **"📊 Export Data"** to create the files

### Method 2: Standalone Export Script
1. Run the standalone export script:
   ```bash
   python export_client_data.py
   ```
2. Choose from the menu options:
   - **1**: Show current client list
   - **2**: Export all formats (JSON, CSV, Excel)
   - **3**: Export JSON only
   - **4**: Export CSV only
   - **5**: Export Excel only
   - **6**: Exit

## Export Formats

### JSON Format
- **File**: `client_data_export_YYYYMMDD_HHMMSS.json`
- **Structure**: Includes export metadata and client array
- **Use Case**: API integration, data processing

### CSV Format
- **File**: `client_data_export_YYYYMMDD_HHMMSS.csv`
- **Structure**: Comma-separated values with headers
- **Use Case**: Spreadsheet import, data analysis

### Excel Format
- **File**: `client_data_export_YYYYMMDD_HHMMSS.xlsx`
- **Structure**: Multiple sheets (Client_Data, Export_Summary)
- **Use Case**: Professional reports, data presentation

## Exported Data Fields

Each client record includes:
- **machine_id**: Unique machine identifier
- **machine_name**: Human-readable machine name
- **export_date**: Date and time of export
- **status**: Authorization status (Authorized)

## Keyboard Shortcuts

- **F7**: Open export dialog (from main application)
- **Enter**: Confirm export
- **Escape**: Cancel export

## File Locations

Exported files are saved in the same directory as the application:
```
📁 Application Directory/
├── client_data_export_YYYYMMDD_HHMMSS.json
├── client_data_export_YYYYMMDD_HHMMSS.csv
└── client_data_export_YYYYMMDD_HHMMSS.xlsx
```

## Troubleshooting

### No Client Data Found
- Ensure you have authorized machines in the system
- Check that `authorized_machines.json` exists and contains valid data

### Export Failed
- Verify you have write permissions in the application directory
- Ensure required Python modules are installed (pandas, openpyxl)

### Import Errors
- Make sure all required dependencies are installed:
  ```bash
  pip install pandas openpyxl
  ```

## Example Usage

### Quick Export (All Formats)
```python
from export_client_data import ClientDataExporter
exporter = ClientDataExporter()
exporter.export_all_formats()
```

### Show Client List
```python
from export_client_data import ClientDataExporter
exporter = ClientDataExporter()
exporter.show_client_list()
```

## Features

✅ **Multiple Export Formats**: JSON, CSV, Excel  
✅ **Timestamped Files**: Automatic timestamp in filename  
✅ **User-Friendly Interface**: Easy-to-use GUI and CLI  
✅ **Data Validation**: Checks for valid client data  
✅ **Error Handling**: Comprehensive error messages  
✅ **Keyboard Shortcuts**: Quick access via F7 key  

---

**Note**: This export functionality is designed to work with the existing machine authorization system. Make sure your `authorized_machines.json` file is properly configured before exporting.
