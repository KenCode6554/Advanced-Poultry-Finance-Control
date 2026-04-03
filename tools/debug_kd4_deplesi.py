import io
import pandas as pd
from google_drive_tool import GoogleDriveTool

def debug_kd4():
    tool = GoogleDriveTool()
    file_id = "1Fh-n_AomM_f8U4q_V5A6WcZ-YI6aY4eN" # KD 4
    print(f"Downloading KD 4: {file_id}")
    content = tool.download_file(file_id)
    
    # Read Data_Out
    df = pd.read_excel(io.BytesIO(content.getvalue()), sheet_name="Data_Out", header=None)
    
    # Print headers around row 10 (where deplesi usually is)
    print("\nInspecting rows 8-15 for headers:")
    for i in range(7, 15):
        row = [str(x) for x in df.iloc[i].tolist()]
        print(f"Row {i+1}: {row[:15]}")
        
    # Find '% CUM' column
    col_idx = tool.find_col(df, '% CUM')
    print(f"\nDetected '% CUM' column index: {col_idx}")
    
    # Find 'Week' column
    week_col = tool.find_col(df, 'akhir mg') or tool.find_col(df, 'mg ke')
    print(f"Detected Week column index: {week_col}")
    
    if col_idx is not None and week_col is not None:
        print("\nValues for Week 85 (if found):")
        for i in range(15, len(df)):
            try:
                w_val = str(df.iloc[i, week_col]).strip()
                if w_val == "85":
                    val = df.iloc[i, col_idx]
                    print(f"Row {i+1}, Week 85, % CUM: {val}")
            except: continue

if __name__ == "__main__":
    debug_kd4()
