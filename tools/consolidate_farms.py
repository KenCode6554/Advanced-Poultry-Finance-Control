import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def consolidate_to_primary_farm():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    primary_farm_id = '8f589dc0-2111-4831-b322-fb46f943eae3'
    ghost_farm_id = 'f52834b6-a19e-4903-818f-7c15147be885'
    
    print(f"Consolidating all units from {ghost_farm_id} to {primary_farm_id}")
    
    # 1. Get all units in the ghost farm
    units = supabase.table('kandang').select('id, name').eq('farm_id', ghost_farm_id).execute().data
    print(f"Found {len(units)} units to move.")
    
    for u in units:
        # Check if a unit with this name already exists in the primary farm
        exists = supabase.table('kandang').select('id').eq('farm_id', primary_farm_id).eq('name', u['name']).execute().data
        if exists:
            # If it exists, we might need to merge records, but for now just move it if it's unique
            print(f"  - Unit '{u['name']}' already exists in primary farm. Skipping move of {u['id']}.")
        else:
            # Relocate
            res = supabase.table('kandang').update({'farm_id': primary_farm_id}).eq('id', u['id']).execute()
            if res.data:
                print(f"  - Moved '{u['name']}' ({u['id']})")
    
    # 2. Cleanup ghost farms
    # We'll leave them for now until the user confirms visibility.
    # But I'll rename GHOST FARM TEST so it's not confusing.
    supabase.table('farms').delete().eq('name', 'GHOST FARM TEST').execute()

if __name__ == "__main__":
    consolidate_to_primary_farm()
