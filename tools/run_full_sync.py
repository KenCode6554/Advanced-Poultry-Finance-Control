import os
import sys
from google_drive_tool import GoogleDriveTool
from db_sync import DbSync
from run_gap_analysis import run_gap_analysis
from dotenv import load_dotenv

def run_orchestration():
    load_dotenv()
    # Support basic filtering via command line arguments
    name_filter = sys.argv[1] if len(sys.argv) > 1 else None
    
    print(f"Starting PoultryPilot Full Sync Orchestration...{' (Filter: ' + name_filter + ')' if name_filter else ''}")
    
    drive_tool = GoogleDriveTool()
    db_sync = DbSync()
    
    if not drive_tool.drive_service or not db_sync.client:
        print("Error: Missing credentials for Drive or Supabase.")
        return

    root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")
    
    # 1. Extraction from Google Drive
    print(f"Phase 1: Extracting data from Root Folder ({root_id})...")
    farms_data = drive_tool.run_sync(root_id, filter_name=name_filter)
    print(f"Extracted data from {len(farms_data)} kandang files.")
    
    # 2. Sync to Supabase
    print("Phase 2: Syncing to Supabase...")
    for farm_data in farms_data:
        farm_name = farm_data['farm']
        kandang_name = farm_data['kandang']
        weekly_records = farm_data['weekly']
        
        # Apply filter if provided
        if name_filter and name_filter.upper() not in kandang_name.upper() and name_filter.upper() not in farm_name.upper():
            continue

        print(f"  Syncing {farm_name} > {kandang_name} ({len(weekly_records)} records)...")
        try:
            kandang_id = db_sync.get_kandang_id(farm_name, kandang_name)
            
            if farm_data.get('populasi', 0) > 0:
                print(f"    Updating population to {farm_data['populasi']}...")
                db_sync.update_kandang_population(kandang_id, farm_data['populasi'])
                
            db_sync.sync_weekly_production(kandang_id, weekly_records)
        except Exception as e:
            print(f"    Error syncing {kandang_name}: {e}")

    # 3. Trigger Gap Analysis
    print("\nPhase 3: Running Gap Analysis...")
    run_gap_analysis()
    
    print("\nFull Sync Orchestration Complete!")

if __name__ == "__main__":
    run_orchestration()
