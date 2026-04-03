import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def test_anon_fetch():
    url = "https://naghbsnosdsrcokveqeu.supabase.co"
    # Using the anon key from dashboard/.env.local
    anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5hZ2hic25vc2RzcmNva3ZlcWV1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMzMTIzOTMsImV4cCI6MjA4ODg4ODM5M30.G7iSsr7XvL-FSzhlKoaHXVasWmV3EMitvYfp8JpU5pk"
    
    supabase: Client = create_client(url, anon_key)
    
    fid = '8f589dc0-2111-4831-b322-fb46f943eae3'
    res = supabase.table('kandang').select('id, name').eq('farm_id', fid).execute()
    print(f"Units visible to ANON key for farm {fid}:")
    for r in res.data:
        print(f"  {r['name']} (ID: {r['id']})")
    
    if any(r['name'] == '15 BBK' for r in res.data):
        print("SUCCESS: 15 BBK is visible to ANON key.")
    else:
        print("FAILURE: 15 BBK is NOT visible to ANON key.")

if __name__ == "__main__":
    test_anon_fetch()
