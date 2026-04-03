import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def compare_kd2():
    tool = GoogleDriveTool()
    # Find 2 BBK file
    folder_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    files = tool.list_files(folder_id)
    target = None
    for f in files:
        if '2' in f['name'] and 'BBK' in f['name']:
            target = f
            break
            
    if target:
        print(f"Comparing with: {target['name']} ({target['id']})")
        fh = tool.download_file(target['id'])
        xl = pd.ExcelFile(fh)
        print(f"Sheet names: {xl.sheet_names}")
        if 'Data_Out' in xl.sheet_names:
            df = pd.read_excel(xl, 'Data_Out', header=None)
            print("Data_Out Head (first 10 rows):")
            print(df.iloc[:10, :10])
    else:
        print("Kandang 2 file not found.")

if __name__ == "__main__":
    compare_kd2()
