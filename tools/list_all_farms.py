import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def list_all_farms():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    res = supabase.table('farms').select('id, name').execute()
    print("All Farms in DB:")
    for r in res.data:
        # Also count kandangs per farm
        kc = supabase.table('kandang').select('id', count='exact').eq('farm_id', r['id']).execute()
        print(f"  ID: {r['id']} | Name: {r['name']} | Units: {kc.count}")

if __name__ == "__main__":
    list_all_farms()
