import os
from supabase import create_client, Client
from gap_engine import GapEngine
from db_sync import DbSync
from datetime import datetime
from dotenv import load_dotenv

def run_gap_analysis():
    load_dotenv()
    print("Running PoultryPilot Revised Gap Analysis...")
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    supabase = create_client(url, key)
    
    engine = GapEngine()
    db_sync = DbSync()

    today = datetime.now().date().strftime('%Y-%m-%d')
    print(f"Date threshold: {today}")

    # 0. Cleanup: Delete future warnings
    # This handles any leftovers from previous "future data" leaks
    print("  Cleaning up future-dated warnings...")
    supabase.table('gap_warnings').delete().gt('week_date', today).execute()

    # 1. Fetch available kandangs
    kandangs_res = supabase.table('kandang').select('id, name').execute()
    kandangs = kandangs_res.data
    
    print(f"Processing {len(kandangs)} kandangs...")

    for k in kandangs:
        kandang_id = k['id']
        kandang_name = k['name']
        
        # 2. Fetch weekly records for this kandang ordered by date (up to today)
        records_res = supabase.table('weekly_production')\
            .select('*')\
            .eq('kandang_id', kandang_id)\
            .lte('week_end_date', today)\
            .order('week_end_date', desc=False)\
            .execute()
        
        records = records_res.data
        if not records:
            continue
            
        print(f"  Analyzing {kandang_name} ({len(records)} records)...")

        # 3. Process Actual vs Standard (Per record)
        total_std_warnings = 0
        for r in records:
            std_warnings = engine.process_actual_vs_std(r)
            if std_warnings:
                total_std_warnings += len(std_warnings)
                db_sync.sync_gap_warnings(std_warnings)
        
        if total_std_warnings:
            print(f"    - Found {total_std_warnings} total Actual vs Std warnings")
        
        # 4. Process Actual vs Actual (Week over Week)
        total_aoa_warnings = 0
        for i in range(1, len(records)):
            prev = records[i-1]
            curr = records[i]
            
            aoa_warnings = engine.process_actual_vs_actual(prev, curr)
            if aoa_warnings:
                total_aoa_warnings += len(aoa_warnings)
                db_sync.sync_gap_warnings(aoa_warnings)
        
        if total_aoa_warnings:
            print(f"    - Found {total_aoa_warnings} total Actual vs Actual warnings")

    print("\nGap Analysis Complete!")

if __name__ == "__main__":
    run_gap_analysis()
