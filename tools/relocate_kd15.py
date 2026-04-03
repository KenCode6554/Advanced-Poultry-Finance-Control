import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def relocate_kd15():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    # Active Farm ID
    active_fid = '8f589dc0-2111-4831-b322-fb46f943eae3'
    # Duplicate Farm ID
    duplicate_fid = 'f3bd01ea-64ef-4bbd-aacc-8787f71a0670'
    # KD 15 ID
    kid = 'b7f0d9c4-0692-4917-8e47-e2f47de0a39c'
    
    print(f"Relocating KD 15 {kid} to active farm {active_fid}...")
    res = supabase.table('kandang').update({'farm_id': active_fid}).eq('id', kid).execute()
    if res.data:
        print(f"  Success: Linked to {active_fid}")
    else:
        print("  Failed to relocate KD 15")

    # Double check if any other units are in the duplicate farm
    res = supabase.table('kandang').select('id, name').eq('farm_id', duplicate_fid).execute()
    if not res.data:
        print(f"Duplicate farm {duplicate_fid} is now empty. Deleting...")
        try:
            supabase.table('farms').delete().eq('id', duplicate_fid).execute()
            print("  Farm deleted.")
        except Exception as e:
            print(f"  Error deleting farm: {e}")
    else:
        print(f"WARNING: Duplicate farm still has units: {[r['name'] for r in res.data]}")

if __name__ == "__main__":
    relocate_kd15()
