import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def audit_all_units():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    farm_id = 'f3bd01ea-64ef-4bbd-aacc-8787f71a0670'
    res = supabase.table('kandang').select('id, name').eq('farm_id', farm_id).execute()
    print(f"Units for Kandang BBK (ID: {farm_id}):")
    for r in res.data:
        print(f"  {r['name']} (ID: {r['id']})")

if __name__ == "__main__":
    audit_all_units()
