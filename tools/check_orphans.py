import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def check_orphans():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    # Check if any weekly_production records exist without a valid kandang_id reference or for the IDs we just deleted
    ids = ['dc5d64ed-7389-42b7-8488-82ea466f8595', '21471e32-253e-4123-9eaf-c5f5f8b2f5de']
    
    res = supabase.table('weekly_production').select('id, kandang_id').in_('kandang_id', ids).execute()
    print(f"Remaining weekly records for KD 15 IDs: {len(res.data)}")
    
    # Also check if there are many records with the old generic search name
    res = supabase.table('kandang').select('id, name').ilike('name', '%15%').execute()
    print(f"Remaining kandang entries matching '15': {res.data}")

if __name__ == "__main__":
    check_orphans()
