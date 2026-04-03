import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def audit_gaps():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    kid = 'b7f0d9c4-0692-4917-8e47-e2f47de0a39c'
    res = supabase.table('gap_warnings').select('id, variable, health_signal').eq('kandang_id', kid).execute()
    print(f"Gap warnings for KD 15 ({kid}): {len(res.data)}")
    for r in res.data[:5]:
        print(f"  {r['variable']}: {r['health_signal']}")

if __name__ == "__main__":
    audit_gaps()
