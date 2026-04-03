import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_anon_access_v2():
    url = os.environ.get("VITE_SUPABASE_URL")
    key = os.environ.get("VITE_SUPABASE_ANON_KEY")
    farm_id = 'f52834b6-a19e-4903-818f-7c15147be885'
    
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}"
    }
    
    # 1. Fetch units for the suspected active farm
    endpoint = f"{url}/rest/v1/kandang?farm_id=eq.{farm_id}&select=id,name"
    res = requests.get(endpoint, headers=headers)
    
    if res.status_code == 200:
        units = res.json()
        print(f"ANON ACCESS SUCCESS for Farm {farm_id}:")
        print(f"Found {len(units)} units")
        for u in units:
            print(f"  - {u['name']} (ID: {u['id']})")
    else:
        print(f"ANON ACCESS FAILED: {res.status_code} - {res.text}")

if __name__ == "__main__":
    check_anon_access_v2()
