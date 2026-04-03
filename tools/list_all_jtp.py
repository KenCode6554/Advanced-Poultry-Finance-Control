"""
list_all_jtp.py
List ALL files in the JTP folder to see if there are Google Sheets versions.
"""
import os
from google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()
root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")
folders = tool.get_farm_folders(root_id)
jtp_folder = next(f for f in folders if 'JTP' in f['name'].upper())

query = f"'{jtp_folder['id']}' in parents and trashed = false"
results = tool.drive_service.files().list(
    q=query, 
    fields='files(id, name, mimeType, modifiedTime)'
).execute()

for f in results.get('files', []):
    print(f"File: {f['name']:50} | Mime: {f['mimeType']:40} | Modified: {f['modifiedTime']}")
