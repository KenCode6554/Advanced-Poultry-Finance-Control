import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

kandang_id = '21471e32-253e-4123-9eaf-c5f5f8b2f5de'
res = supabase.table('weekly_production').select('*', count='exact').eq('kandang_id', kandang_id).execute()

print(f"Standalone Client Found: {res.count} records")
for r in res.data:
    print(f"  Date: {r.get('week_end_date')} | Week: {r.get('usia_minggu')}")
