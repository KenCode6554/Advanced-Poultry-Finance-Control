import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def audit_templates():
    tool = GoogleDriveTool()
    # List a few units
    targets = [
        ('15 BBK', '10iHIouFlnEe-lbAVz7sz-UdHtZaNSAb6'),
        ('3A BBK', '1mYf1uF_W-8b2z-7aUqYFvV0s3Kx1pYX'), # Parent folder, I'll find specific ones
    ]
    
    # Actually just search for all BBK files and check Row 9
    files = tool.list_xlsx_files('1mYf1uF_W-8b2z-7aUqYFvV0s3Kx1pYX')
    for f in files[:5]: # Check first 5
        print(f"\n--- {f['name']} ---")
        try:
            fh = tool.download_file(f['id'])
            df = pd.read_excel(fh, 'Data_Out', header=None)
            header = [str(x).lower() for x in df.iloc[9].tolist()[:40]]
            # Check if 'hd' is at col 9
            if 'hd' in header and header.index('hd') == 9:
                print("MATCHES KD 15 Template (HD at col 9)")
            else:
                print(f"Standard/Other Template (HD at {header.index('hd') if 'hd' in header else 'NOT FOUND'})")
        except:
            print("Error reading Data_Out")

if __name__ == "__main__":
    audit_templates()
