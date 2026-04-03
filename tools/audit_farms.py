import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def audit_farms():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    res = supabase.table('farms').select('id, name').ilike('name', '%BBK%').execute()
    print("Farms matching 'BBK':")
    for r in res.data:
        print(f"  ID: {r['id']} | Name: {r['name']}")

if __name__ == "__main__":
    audit_farms()
