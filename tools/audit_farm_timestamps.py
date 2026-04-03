import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def audit_farm_timestamps():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    farms = supabase.table('farms').select('id, name, created_at').eq('name', 'Kandang BBK').execute().data
    print("Kandang BBK Entities Audit:")
    for f in farms:
        count = supabase.table('kandang').select('id', count='exact').eq('farm_id', f['id']).execute().count
        print(f"ID: {f['id']} | Created: {f['created_at']} | Units: {count}")

if __name__ == "__main__":
    audit_farm_timestamps()
