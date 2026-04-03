import os
import json
from google_drive_tool import GoogleDriveTool
from db_sync import DbSync
from dotenv import load_dotenv

load_dotenv()

def final_sync():
    print("=== STARTING FINAL DATA RESTORATION (KD 15 FOCUS) ===")
    tool = GoogleDriveTool()
    db = DbSync()
    
    # 1. Run full extraction from explicit IDs
    results = tool.run_sync_multi()
    
    # 2. Sync to DB
    total_records = 0
    for res in results:
        farm = res['farm_name']
        kandang = res['kandang_name']
        strain = res.get('strain')
        
        print(f"\nProcessing {kandang} ({farm}) [Strain: {strain}]...")
        
        k_id = db.get_kandang_id(farm, kandang, strain)
        
        if 'populasi' in res:
            db.update_kandang_population(k_id, res['populasi'])
            
        if 'weekly' in res and res['weekly']:
            count = len(res['weekly'])
            print(f"  Inserting {count} production records...")
            db.sync_weekly_production(k_id, res['weekly'])
            total_records += count
            
    print(f"\n=== SYNC COMPLETE ===")
    print(f"Total production records across all units: {total_records}")

if __name__ == "__main__":
    final_sync()
