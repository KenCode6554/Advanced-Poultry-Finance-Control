import os
import sys
import argparse
from google_drive_tool import GoogleDriveTool

def auto_convert_procedure(dry_run=True):
    """
    Automates the conversion of .xlsx files to Google Sheets and archives originals.
    """
    drive_tool = GoogleDriveTool()
    if not drive_tool.drive_service:
        print("ERROR: Could not initialize Google Drive service. Check credentials.")
        return

    # Folder IDs from environment
    bbk_ids = os.getenv('GOOGLE_DRIVE_BBK_IDS', "").split(',')
    jtp_ids = os.getenv('GOOGLE_DRIVE_JTP_IDS', "").split(',')
    
    target_folders = [f.strip() for f in bbk_ids + jtp_ids if f.strip()]
    
    if not target_folders:
        print("ERROR: No target folders found in GOOGLE_DRIVE_BBK_IDS or GOOGLE_DRIVE_JTP_IDS.")
        return

    print(f"\n{'[DRY RUN] ' if dry_run else '[LIVE MODE] '}Starting conversion procedure...")
    print("-" * 60)

    for folder_id in target_folders:
        print(f"\nScanning folder: {folder_id}")
        
        # 1. List .xlsx files
        xlsx_files = drive_tool.list_binary_xlsx_files(folder_id)
        if not xlsx_files:
            print("   No binary .xlsx files found.")
            continue
            
        print(f"   Found {len(xlsx_files)} .xlsx files.")

        # 2. Setup Archive folder
        archive_folder_id = None
        
        # Search for existing Archive folder
        query = f"'{folder_id}' in parents and name = 'Archive' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        results = drive_tool.drive_service.files().list(q=query, fields="files(id)").execute()
        files = results.get('files', [])
        
        if files:
            archive_folder_id = files[0]['id']
            print(f"   Using existing Archive folder: {archive_folder_id}")
        else:
            if not dry_run:
                file_metadata = {
                    'name': 'Archive',
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [folder_id]
                }
                folder = drive_tool.drive_service.files().create(body=file_metadata, fields='id').execute()
                archive_folder_id = folder.get('id')
                print(f"   Created new Archive folder: {archive_folder_id}")
            else:
                print("   [DRY RUN] Would create 'Archive' folder.")

        # 3. Process each file
        for f in xlsx_files:
            file_name = f['name']
            file_id = f['id']
            
            print(f"\n   Processing: {file_name}")
            
            # 3a. Convert to Google Sheet
            if not dry_run:
                try:
                    # Copy file with mimeType change (this trigger conversion)
                    copy_metadata = {
                        'name': file_name.replace('.xlsx', '').replace('.XLSX', ''),
                        'mimeType': 'application/vnd.google-apps.spreadsheet',
                        'parents': [folder_id]
                    }
                    new_file = drive_tool.drive_service.files().copy(
                        fileId=file_id, 
                        body=copy_metadata
                    ).execute()
                    print(f"      CONVERTED: Created Sheet '{copy_metadata['name']}' (ID: {new_file.get('id')})")
                    
                    # 3b. Move original to Archive
                    # Retrieve the existing parents to remove
                    file_info = drive_tool.drive_service.files().get(fileId=file_id, fields='parents').execute()
                    previous_parents = ",".join(file_info.get('parents'))
                    
                    drive_tool.drive_service.files().update(
                        fileId=file_id,
                        addParents=archive_folder_id,
                        removeParents=previous_parents,
                        fields='id, parents'
                    ).execute()
                    print(f"      ARCHIVED: Moved original .xlsx to Archive.")
                    
                except Exception as e:
                    print(f"      FAILED: {e}")
            else:
                print(f"      [DRY RUN] Would convert '{file_name}' to Google Sheet and move to Archive.")

    print("\n" + "="*60)
    if dry_run:
        print("DRY RUN COMPLETE. No changes were made.")
        print("Run with --execute to perform actual migration.")
    else:
        print("LIVE CONVERSION COMPLETE.")
    print("="*60 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-convert poultry .xlsx files to Google Sheets.")
    parser.add_argument("--execute", action="store_true", help="Perform actual conversion and move operations.")
    args = parser.parse_args()
    
    auto_convert_procedure(dry_run=not args.execute)
