import os
import json
from dotenv import load_dotenv

def get_service_account_email():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_path or not os.path.exists(creds_path):
        print("Service account file not found.")
        return
    
    with open(creds_path, 'r') as f:
        data = json.load(f)
        print(f"Service Account Email: {data.get('client_email')}")

if __name__ == "__main__":
    get_service_account_email()
