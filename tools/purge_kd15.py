import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def purge_kd15():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    ids = ['dc5d64ed-7389-42b7-8488-82ea466f8595', '21471e32-253e-4123-9eaf-c5f5f8b2f5de']
    
    print("Purging production data for KD 15...")
    for kid in ids:
        # Delete weekly production
        res = supabase.table('weekly_production').delete().eq('kandang_id', kid).execute()
        print(f"  Deleted {len(res.data) if res.data else 0} weekly records for {kid}")
        # Delete daily production
        res = supabase.table('daily_production').delete().eq('kandang_id', kid).execute()
        print(f"  Deleted {len(res.data) if res.data else 0} daily records for {kid}")

    # Delete the duplicate kandang (the one without AL101 in name if possible, or just merge them)
    # Actually I'll delete BOTH and let the sync recreate one clean one
    print("Deleting kandang entries...")
    for kid in ids:
        try:
            res = supabase.table('kandang').delete().eq('id', kid).execute()
            print(f"  Deleted kandang {kid}")
        except Exception as e:
            print(f"  Error deleting kandang {kid}: {e}")

if __name__ == "__main__":
    purge_kd15()
