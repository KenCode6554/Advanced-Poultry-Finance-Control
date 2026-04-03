
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)

res = supabase.table('farms').select('id, name').execute()
print("FARMS LIST:")
for f in res.data:
    print(f"- {f['name']} (ID: {f['id']})")
