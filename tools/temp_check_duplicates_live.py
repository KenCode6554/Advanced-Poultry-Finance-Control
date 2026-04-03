
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)

res = supabase.table('kandang').select('id, name, farm_id').execute()
print("KANDANG LIST:")
for k in res.data:
    print(f"- {k['name']} (ID: {k['id']})")
