import io
import os
import sys
import openpyxl
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def debug_jantan_headers():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    
    file_id = '1_AVPCyEuVLUulSeUzPYehCqkpZQFrRw0' # Jantan JTP
    content = tool.download_file(file_id)
    
    wb = openpyxl.load_workbook(io.BytesIO(content.getvalue()), data_only=True)
    ws = wb['Data_Out']
    
    print("Inspecting Jantan JTP Data_Out (Rows 1-10):")
    for r in range(1, 11):
        row_vals = [ws.cell(r, c).value for c in range(1, 40)]
        # Filter out sequences of None to make it readable
        readable = [f"{i+1}:{v}" for i, v in enumerate(row_vals) if v is not None]
        print(f"Row {r}: {' | '.join(readable)}")

if __name__ == "__main__":
    debug_jantan_headers()
