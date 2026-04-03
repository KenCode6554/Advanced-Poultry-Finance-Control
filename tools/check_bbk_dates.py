"""
check_bbk_dates.py
Check BBK file dates.
"""
import os
from google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()
folders = tool.get_farm_folders(os.getenv('GOOGLE_DRIVE_ROOT_ID'))
bbk_folder = next(f for f in folders if 'BBK' in f['name'].upper())
files = tool.list_xlsx_files(bbk_folder['id'])

for f in files:
    print(f"File: {f['name']:50} | Modified: {f['modifiedTime']}")
