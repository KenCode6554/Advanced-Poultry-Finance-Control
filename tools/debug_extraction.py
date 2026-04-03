import os
from google_drive_tool import GoogleDriveTool
import io
import pandas as pd

tool = GoogleDriveTool()
folder_id = os.getenv("GOOGLE_DRIVE_ROOT_ID") # Or farm folder ID
files = tool.list_xlsx_files('1K8-8z-wR7_2L-9-zW7-z-8-z-8-z-8') # Use a dummy or root to find 15
# Actually I'll just find the file ID directly via a quick search
query = "name contains '15 BBK' and trashed = false"
res = tool.drive_service.files().list(q=query, fields="files(id, name)").execute().get('files', [])
if not res:
    print("File not found!")
    exit()

f = res[0]
print(f"Testing extraction for {f['name']} ({f['id']})...")

content = tool.download_file(f['id'])
# Test extraction
extracted = tool.extract_data_from_excel(io.BytesIO(content.getvalue()), "Kandang BBK", f['name'])
print(f"Extracted {len(extracted['weekly'])} records.")
for r in extracted['weekly'][:5]:
    print(r)

# Debug: Inspect raw headers
df = pd.read_excel(io.BytesIO(content.getvalue()), sheet_name='Data_Out', header=None)
print("\nRaw Headers (Row 7-10):")
print(df.iloc[7:11, :40]) # View 40 columns
