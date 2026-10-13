
from pathlib import Path
import pandas as pd

# Locate the data
data_dir = Path("data/raw")
files = list(data_dir.glob("*.xlsx")) + list(data_dir.glob("*.xls"))

if not files:
    raise FileNotFoundError("No Excel file found in data/raw/")

print("Excel files found:")
for file in files:
    print(" -", file.name)

# Open the first workbook
file_path = Path("data/raw/absei-2000-2024-all-results.xlsx")
workbook = pd.ExcelFile(file_path)

print("\nWORKBOOK SHEETS")
for i, sheet in enumerate(workbook.sheet_names, start=1):
    print(f"{i:02d}. {sheet}")

# Preview the first 12 rows of every sheet
for sheet in workbook.sheet_names:
    df = pd.read_excel(
        file_path,
        sheet_name=sheet,
        header=None,
        nrows=12
    )

    print(f"\n{'=' * 65}")
    print(f"SHEET: {sheet}")
    print(f"{'=' * 65}")
    print(df.to_string(index=False, header=False))
