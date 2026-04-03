
import os
from dotenv import load_dotenv
from google_drive_tool import GoogleDriveTool

load_dotenv()
tool = GoogleDriveTool()

spreadsheet_id = "1608MM-CjyuabLvAGWUwNhSLNJ6zyqR8GqnXjpew0o8w"
range_name = "'Kandang 5'!A:E"

print(f"Fetching {range_name} from {spreadsheet_id}...")
result = tool.sheets_service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range=range_name
).execute()

values = result.get('values', [])
print(f"Total rows found: {len(values)}")
if values:
    for row in values[-10:]:
        print(row)
