
import os
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()
tool = GoogleDriveTool()

target_files = [
    "Rec P. fajar kd 17 BBK (AL 1001).xlsx",
    "Rec P. fajar kd 3A+3B (AL 1001).xlsx"
]

root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")
folders = tool.get_farm_folders(root_id)

for folder in folders:
    files = tool.list_xlsx_files(folder['id'])
    for f in files:
        if f['name'] in target_files:
            print(f"\nTesting {f['name']}...")
            res = tool.get_computed_population(f['id'], f['name'])
            print(f"RESULT: {res}")
