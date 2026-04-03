
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)

res = supabase.table('kandang').select('id, name, populasi').execute()
print("KANDANG POPULATION STATUS:")
for k in res.data:
    print(f"- {k['name']}: {k['populasi']}")
