import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

def debug_extraction():
    load_dotenv()
    tool = GoogleDriveTool()
    
    target_name = "Rec P. fajar kd 2 BBK.xlsx"
    target_id = None
    
    root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")
    farms = tool.get_farm_folders(root_id)
    for farm in farms:
        files = tool.list_xlsx_files(farm['id'])
        for f in files:
            if f['name'] == target_name:
                target_id = f['id']
                break
        if target_id: break
        
    print(f"📥 Downloading {target_name}...")
    content = tool.download_file(target_id)
    
    xl = pd.ExcelFile(content, engine='openpyxl')
    df = xl.parse('Data_Out', header=None)
    
    print(f"Rows found: {len(df)}")
    print("Checking Row 9 logic:")
    
    for i in range(7, 20): # Check a wider range
        row = df.iloc[i]
        val = row[0]
        v_type = type(val)
        is_na = pd.isna(val)
        print(f"Row {i}: Val={val}, Type={v_type}, IsNA={is_na}")

if __name__ == "__main__":
    debug_extraction()
