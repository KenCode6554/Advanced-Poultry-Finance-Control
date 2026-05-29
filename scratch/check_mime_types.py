
from tools.google_drive_tool import GoogleDriveTool
import json

def check_files():
    g = GoogleDriveTool()
    folders = g.get_farm_folders('1eMc4RBPCZQj0GI4nZSxiTzyaXoK8IKV-')
    for f in folders:
        print(f"Folder: {f['name']} ({f['id']})")
        results = g.drive_service.files().list(
            q=f"'{f['id']}' in parents and trashed = false",
            fields='files(id, name, mimeType)'
        ).execute()
        for file in results.get('files', []):
            print(f"  - {file['name']} | {file['mimeType']}")

if __name__ == '__main__':
    check_files()
