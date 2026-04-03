"""
check_mimetype.py
Check MIME type of JTP files.
"""
import os
from google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()
root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")
folders = tool.get_farm_folders(root_id)
jtp_folder = next(f for f in folders if 'JTP' in f['name'].upper())
# Need to use the tool's drive_service directly to list with mimeType
query = f"'{jtp_folder['id']}' in parents"
results = tool.drive_service.files().list(
    q=query,
    fields="files(id, name, mimeType, modifiedTime)"
).execute()
files = results.get('files', [])

for file in files:
    print(f"File: {file['name']} | ID: {file['id']} | Mime: {file.get('mimeType')} | Modified: {file.get('modifiedTime')}")
