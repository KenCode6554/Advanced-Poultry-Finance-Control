import io
import os
import sys
import openpyxl
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def check_hidden_sheets_3a3b():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    wb = openpyxl.load_workbook(io.BytesIO(content.getvalue()))
    
    print("All Sheets in Workbook:")
    for sheet in wb.worksheets:
        print(f"  Name: {sheet.title}, Visibility: {sheet.sheet_state}")

if __name__ == "__main__":
    check_hidden_sheets_3a3b()
