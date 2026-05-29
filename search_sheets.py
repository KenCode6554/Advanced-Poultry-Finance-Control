from tools.google_drive_tool import GoogleDriveTool
import os
from dotenv import load_dotenv
load_dotenv()
tool = GoogleDriveTool()
query = "mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false"
res = tool.drive_service.files().list(q=query, fields='files(id, name, mimeType, modifiedTime, parents)').execute()
print(f"Found {len(res.get('files', []))} Google Sheets total.")
for f in res.get('files', []):
    print(f"{f['name']} | {f['id']} | {f.get('parents', 'None')} | {f['modifiedTime']}")
