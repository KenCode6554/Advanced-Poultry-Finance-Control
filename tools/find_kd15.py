import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def find_kd15():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    supabase: Client = create_client(url, key)
    
    res = supabase.table('kandang').select('id, name, farm_id').ilike('name', '%15%').execute()
    print("Kandang entries matching '15':")
    for r in res.data:
        print(f"  ID: {r['id']} | Name: {r['name']} | FarmID: {r['farm_id']}")

if __name__ == "__main__":
    find_kd15()
