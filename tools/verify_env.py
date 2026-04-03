import os
from dotenv import load_dotenv

def test_connections():
    load_dotenv()
    
    services = [
        "SUPABASE_URL", "SUPABASE_ANON_KEY", 
        "ANTHROPIC_API_KEY", 
        "NOTION_TOKEN", 
        "GOOGLE_APPLICATION_CREDENTIALS"
    ]
    
    results = {}
    for service in services:
        results[service] = "✅ Set" if os.getenv(service) else "❌ Missing"
        
    print("--- Connection Verification ---")
    for service, status in results.items():
        print(f"{service}: {status}")

if __name__ == "__main__":
    test_connections()
