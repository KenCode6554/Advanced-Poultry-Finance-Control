import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def inventory():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    fid = 'f3bd01ea-64ef-4bbd-aacc-8787f71a0670'
    res = supabase.table('kandang').select('id, name').eq('farm_id', fid).execute()
    print(f"Inventory for farm {fid}:")
    for r in res.data:
        print(f"  {r['name']} (ID: {r['id']})")

if __name__ == "__main__":
    inventory()
