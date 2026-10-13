
from pathlib import Path
import pandas as pd

file_path = Path("data/raw/absei-2000-2024-all-results.xlsx")

workbook = pd.ExcelFile(file_path)

# Find the sheet regardless of extra spaces
index_sheet = next(
    name for name in workbook.sheet_names
    if name.strip() == "List of Tables"
)

index = pd.read_excel(
    file_path,
    sheet_name=index_sheet,
    header=None
)

print("\nAVAILABLE ABSEI INDICATORS\n")

for _, row in index.iterrows():
    for value in row:
        if isinstance(value, str) and value.strip().startswith("Table "):
            print(value.strip())

# Find table headings in the three ownership sheets
for sheet in ["ALL", "FOREIGN", "IRISH"]:
    df = pd.read_excel(
        file_path,
        sheet_name=sheet,
        header=None
    )

    print(f"\n{'=' * 60}")
    print(f"{sheet}: {len(df)} rows")
    print(f"{'=' * 60}")

    for row_number, row in df.iterrows():
        for value in row:
            if isinstance(value, str) and value.strip().startswith("Table "):
                print(f"Excel row {row_number + 1}: {value.strip()}")
