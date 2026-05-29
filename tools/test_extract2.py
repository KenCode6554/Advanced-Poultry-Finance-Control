import sys
sys.path.append('c:/Users/ASUS/OneDrive/Documents/Adcanded Poultry Finance Control')
from tools.google_drive_tool import GoogleDriveTool
tool = GoogleDriveTool()
results = tool.drive_service.files().list(q="name contains 'Rec P. fajar kd 16'", fields='files(id, name)').execute()
file_id = results.get('files', [])[0]['id']
df = tool._read_dataout_via_sheets_api(file_id)
idx = tool._find_column_indices(df, '')
print(f'Idx mapping: {idx}')

if 'hd_act' in idx and 'date' in idx:
    for i in range(10, 50):
        try:
            row = df.iloc[i]
            date_val = row[idx['date']]
            hd_val = row[idx['hd_act']]
            print(f'Row {i}: Date={date_val}, HD={hd_val}')
        except Exception as e:
            pass
