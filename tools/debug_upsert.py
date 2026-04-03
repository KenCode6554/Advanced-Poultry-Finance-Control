import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)

kandang_id = '21471e32-253e-4123-9eaf-c5f5f8b2f5de' # KD 15

payload = {
    'kandang_id': kandang_id,
    'week_end_date': '2026-03-22',
    'usia_minggu': 49,
    'hd_actual': 85.5,
    'hd_std': 85.0
}

print(f"Testing UPSERT for Kandang {kandang_id}...")
try:
    res = supabase.table('weekly_production').upsert(payload, on_conflict='kandang_id,week_end_date').execute()
    print("Success!")
    print(res.data)
except Exception as e:
    print(f"Error: {e}")
