import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

def calibrate():
    load_dotenv()
    tool = GoogleDriveTool()
    
    # Target a specific file from discovery (BBK Kd 2)
    # File ID for "Rec P. fajar kd 2 BBK.xlsx" from the previous run
    # Let's search for it in the tool's discovery result if we had id
    # For now, I'll list and find it manually since I don't have the JSON read yet
    
    target_name = "Rec P. fajar kd 2 BBK.xlsx"
    target_id = None
    
    # Find the ID
    root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")
    farms = tool.get_farm_folders(root_id)
    for farm in farms:
        files = tool.list_xlsx_files(farm['id'])
        for f in files:
            if f['name'] == target_name:
                target_id = f['id']
                break
        if target_id: break
        
    if not target_id:
        print(f"❌ Could not find {target_name}")
        return

    print(f"📥 Downloading {target_name} for calibration...")
    content = tool.download_file(target_id)
    
    xl = pd.ExcelFile(content, engine='openpyxl')
    print(f"📋 Sheets found: {xl.sheet_names}")
    
    if 'Data_Out' in xl.sheet_names:
        print("\n🔍 Inspecting 'Data_Out' (Rows 0-50, Selected Columns):")
        df = xl.parse('Data_Out', header=None) # No header to keep index consistent with Excel letters
        
        # Columns of interest: A(0), C(2), D(3), E(4), K(10), L(11), W(22), X(23), AB(27), AE(30), AF(31), AH(33), AI(34)
        cols_to_view = [0, 2, 3, 4, 10, 11, 22, 23, 27, 30, 31, 33, 34]
        subset = df.iloc[0:50, cols_to_view]
        print(subset.to_string())
    else:
        print("❌ 'Data_Out' sheet not found.")


if __name__ == "__main__":
    calibrate()
