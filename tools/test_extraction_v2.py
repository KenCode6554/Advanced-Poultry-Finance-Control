import io
import json
import pandas as pd
from google_drive_tool import GoogleDriveTool

def test_local_extraction():
    tool = GoogleDriveTool()
    file_path = 'c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\temp_debug.xlsx'
    
    with open(file_path, 'rb') as f:
        content = f.read()
    
    extracted = tool.extract_data_from_excel(io.BytesIO(content), "Kandang BBK", "Rec P. fajar kd 6A BBK.xlsx")
    
    # Print sample of extracted weekly data
    print(f"Extracted {len(extracted['weekly'])} weeks.")
    if extracted['weekly']:
        print("First week sample:")
        print(json.dumps(extracted['weekly'][0], indent=2))
        print("Last week sample:")
        print(json.dumps(extracted['weekly'][-1], indent=2))

if __name__ == "__main__":
    test_local_extraction()
