import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def exhaustive_inventory():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    # Fetch all farms
    farms = supabase.table('farms').select('id, name').execute().data
    print(f"Total Farms found: {len(farms)}")
    
    for f in farms:
        units = supabase.table('kandang').select('id, name').eq('farm_id', f['id']).execute().data
        print(f"\nFarm: '{f['name']}' (ID: {f['id']}) - Units: {len(units)}")
        for u in units:
            print(f"  Unit: '{u['name']}' (ID: {u['id']})")

if __name__ == "__main__":
    exhaustive_inventory()
