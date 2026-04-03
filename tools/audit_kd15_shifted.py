import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def audit_kd15_shifted():
    tool = GoogleDriveTool()
    file_id = '10iHIouFlnEe-lbAVz7sz-UdHtZaNSAb6' # KD 15
    fh = tool.download_file(file_id)
    df = pd.read_excel(fh, 'Data_Out', header=None)
    
    print("KD 15 Data_Out Pattern Audit (Rows 20-30):")
    # We suspect a shift. Let's look at all columns for these rows.
    for i in range(20, 31):
        row = df.iloc[i].tolist()
        # Find where the week number is (usually in early columns)
        week = row[1]
        print(f"Row {i} (Week {week}):")
        # Print non-nan values with indices
        values = [(idx, val) for idx, val in enumerate(row) if not pd.isna(val)]
        print(f"  Values: {values}")

if __name__ == "__main__":
    audit_kd15_shifted()
