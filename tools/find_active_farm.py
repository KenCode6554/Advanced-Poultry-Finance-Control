import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def find_active_farm_by_units():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    # Target units from screenshot
    target_names = [
        "2 BBK", "6A BBK (AL 1001)", "6B BBK (AL 1001)", "7A BBK", "7B BBK", 
        "12 BBK", "14 B4 BBK", "16 BBK TQ988", "BBK Kd 9a AL1001", "BBK Kd 9b AL1001", 
        "BBK Kd 11 AL1001 (01)", "17 BBK (AL 1001)", "3A+3B (AL 1001)", "1A BBK (AL 1002)"
    ]
    
    farms = supabase.table('farms').select('id, name').execute().data
    print(f"Auditing {len(farms)} farms...")
    
    for f in farms:
        units = supabase.table('kandang').select('name').eq('farm_id', f['id']).execute().data
        unit_names = [u['name'] for u in units]
        
        # Check how many target names are in this farm
        matches = [name for name in target_names if name in unit_names]
        if len(matches) > 0:
            print(f"\nFarm: '{f['name']}' (ID: {f['id']})")
            print(f"  Match count: {len(matches)} / {len(target_names)}")
            print(f"  Total units in this farm: {len(unit_names)}")
            if len(matches) == len(target_names):
                print("  !!! THIS IS THE ACTIVE FARM !!!")

if __name__ == "__main__":
    find_active_farm_by_units()
