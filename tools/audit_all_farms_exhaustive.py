import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def audit_all_farms_exhaustive():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    res = supabase.table('farms').select('id, name').execute()
    print("Exhaustive Farm List:")
    for r in res.data:
        print(f"  Name: '{r['name']}' | ID: {r['id']}")

if __name__ == "__main__":
    audit_all_farms_exhaustive()
