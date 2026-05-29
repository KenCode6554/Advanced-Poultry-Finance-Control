import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
sb = create_client(url, key)

res = sb.table('kandang').select('name, populasi, farms(name)').order('name').execute()
for r in res.data:
   print(f"{r['farms']['name']} / {r['name']}: {r['populasi']}")
