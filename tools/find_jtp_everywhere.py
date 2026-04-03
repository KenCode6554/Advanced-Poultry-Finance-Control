"""
find_jtp_everywhere.py
Search for any JTP related files/folders across the whole Drive.
"""
import os
from google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()

# Search for folders
print("--- Searching for JTP Folders ---")
q = "mimeType = 'application/vnd.google-apps.folder' and name contains 'JTP' and trashed = false"
res = tool.drive_service.files().list(q=q, fields='files(id, name, parents)').execute()
for f in res.get('files', []):
    print(f"Folder: {f['name']:30} | ID: {f['id']} | Parents: {f.get('parents')}")

# Search for files with JTP in name
print("\n--- Searching for JTP Files ---")
q = "name contains 'JTP' and trashed = false"
res = tool.drive_service.files().list(q=q, fields='files(id, name, mimeType, modifiedTime, parents)', pageSize=50).execute()
for f in res.get('files', []):
    p_id = f.get('parents', ['None'])[0]
    # Get parent name
    try:
        p_name = tool.drive_service.files().get(fileId=p_id, fields='name').execute().get('name')
    except:
        p_name = "Unknown"
    print(f"File: {f['name']:50} | Mime: {f['mimeType']:30} | Modified: {f['modifiedTime']} | Parent: {p_name}")
