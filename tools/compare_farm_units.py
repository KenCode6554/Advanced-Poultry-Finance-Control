import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def compare_farm_units():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    farm_ids = [
        '8f589dc0-2111-4831-b322-fb46f943eae3', # User sees this (22 units)
        'f52834b6-a19e-4903-818f-7c15147be885'  # Ghost farm (14/15 units)
    ]
    
    for fid in farm_ids:
        units = supabase.table('kandang').select('name').eq('farm_id', fid).execute().data
        unit_names = sorted([u['name'] for u in units])
        print(f"\nFarm ID: {fid}")
        print(f"Total Units: {len(unit_names)}")
        print(f"Names: {', '.join(unit_names)}")

if __name__ == "__main__":
    compare_farm_units()
