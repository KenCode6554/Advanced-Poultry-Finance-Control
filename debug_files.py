from tools.google_drive_tool import GoogleDriveTool
import os
from dotenv import load_dotenv
load_dotenv()
tool = GoogleDriveTool()
folder_id = os.getenv('GOOGLE_DRIVE_BBK_IDS').split(',')[0]
res = tool.drive_service.files().list(
    q=f"'{folder_id}' in parents and trashed = false", 
    fields='files(id, name, mimeType, modifiedTime)'
).execute()
for f in res.get('files', []):
    print(f"{f['name']} | {f['mimeType']} | {f['modifiedTime']}")
