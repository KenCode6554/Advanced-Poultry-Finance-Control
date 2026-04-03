from tools.google_drive_tool import GoogleDriveTool
import json

tool = GoogleDriveTool()
folder_id = '1K8-8z-wR7_2L-9-zW7-z-8-z-8-z-8' # RECORDING BBK
print(f"Listing files for RECORDING BBK ({folder_id})...")
files = tool.list_xlsx_files(folder_id)
print(f"Found {len(files)} files.")

for f in files:
    if '15' in f['name']:
        print(f"MATCH: {f['name']} ({f['id']})")
