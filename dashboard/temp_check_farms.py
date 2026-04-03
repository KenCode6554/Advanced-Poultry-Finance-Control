import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL') or os.getenv('VITE_SUPABASE_URL')
key = os.getenv('SUPABASE_KEY') or os.getenv('VITE_SUPABASE_ANON_KEY')

if url and key:
    client = create_client(url, key)
    res = client.table('farms').select('*').execute()
    with open('farms_output2.json', 'w') as f:
        json.dump(res.data, f, indent=2)
else:
    print("No URL or api key found")
