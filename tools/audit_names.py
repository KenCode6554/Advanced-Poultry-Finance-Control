import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def audit_names():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    client = create_client(url, key)
    
    res = client.table('kandang').select('id, name').execute()
    print("ALL KANDANG NAMES IN DB:")
    for k in res.data:
        print(f" - {k['name']} ({k['id']})")

if __name__ == "__main__":
    audit_names()
