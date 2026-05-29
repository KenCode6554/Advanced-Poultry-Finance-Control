import os
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv

# Setup credentials
load_dotenv()
creds_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

if not creds_path or not os.path.exists(creds_path):
    raise ValueError(f"Service account file not found: {creds_path}")

creds = service_account.Credentials.from_service_account_file(
    creds_path, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)
service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1nfzrnlDrtor-x4gj1DZ8a-4fmWrIAfUw8W4dU2wcN94'
RANGE_NAME = 'Data_Out!A1:Z150'

result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
rows = result.get('values', [])

if not rows:
    print('No data found.')
else:
    # Handle rows with different lengths by padding with None
    max_len = max(len(row) for row in rows)
    padded_rows = [row + [None] * (max_len - len(row)) for row in rows]
    
    df = pd.DataFrame(padded_rows[1:], columns=padded_rows[0])
    print(df.tail(15))
