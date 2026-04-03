"""
find_recent_files.py
Search for any recently modified files on Drive.
"""
import os
from datetime import datetime, timedelta
from google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()
two_days_ago = (datetime.utcnow() - timedelta(days=2)).isoformat() + 'Z'

print(f"--- Files modified since {two_days_ago} ---")
q = f"modifiedTime > '{two_days_ago}' and trashed = false"
res = tool.drive_service.files().list(
    q=q, 
    fields='files(id, name, mimeType, modifiedTime, parents)', 
    orderBy='modifiedTime desc'
).execute()

for f in res.get('files', []):
    p_id = f.get('parents', ['None'])[0]
    try:
        p_name = tool.drive_service.files().get(fileId=p_id, fields='name').execute().get('name')
    except:
        p_name = "Unknown"
    print(f"File: {f['name']:50} | Mime: {f['mimeType']:30} | Modified: {f['modifiedTime']} | Parent: {p_name}")
