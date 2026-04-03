import os
import pandas as pd
from datetime import datetime, date
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv
import json

load_dotenv()

def deep_inspect_graphics():
    tool = GoogleDriveTool()
    root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    
    # Just check one JTP and one BBK for reference
    targets = [
        ("Kandang JTP", "REC KD 7 JTP (AL 1001).xlsx"),
        ("Kandang BBK", "Rec P. fajar kd 7A BBK.xlsx")
    ]
    
    results = {}

    farms = tool.get_farm_folders(root_id)
    for farm_name, file_name in targets:
        farm_folder = next((f for f in farms if farm_name.split()[-1] in f['name'].upper()), None)
        if not farm_folder: continue
        
        files = tool.list_xlsx_files(farm_folder['id'])
        target_file = next((f for f in files if f['name'] == file_name), None)
        if not target_file: continue
        
        print(f"Deep inspecting {file_name}...")
        content = tool.download_file(target_file['id'])
        xl = pd.ExcelFile(content, engine='openpyxl')
        
        if 'Graphic' in xl.sheet_names:
            df = xl.parse('Graphic', header=None)
            # Find the row where data starts. Usually "Usia (mgg)" is in the X-axis
            # In the screenshot, Usia (mgg) is at the bottom.
            # Let's look for rows with values 19, 20, 21...
            
            data_sample = {
                "head": df.head(50).values.tolist(),
                "tail": df.tail(50).values.tolist()
            }
            results[file_name] = data_sample
            
            # Also check Data_Out to see if it matches
            if 'Data_Out' in xl.sheet_names:
                df_out = xl.parse('Data_Out', header=None)
                results[file_name + "_Data_Out"] = df_out.head(30).values.tolist()

    def default_serializer(obj):
        if isinstance(obj, (datetime, date, pd.Timestamp)):
            return obj.isoformat()
        return str(obj)

    with open('.tmp/deep_graphic_inspect.json', 'w') as f:
        json.dump(results, f, indent=2, default=default_serializer)
    print("Results saved to .tmp/deep_graphic_inspect.json")

if __name__ == "__main__":
    deep_inspect_graphics()
