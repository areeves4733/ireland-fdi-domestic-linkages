
from pathlib import Path
import pandas as pd

file_path = Path("data/raw/absei-2000-2024-all-results.xlsx")

# Table locations identified from your workbook
table_rows = {
    "FOREIGN": {
        9: 191,
        12: 263,
        14: 312,
        15: 338,
    },
    "IRISH": {
        9: 196,
        12: 272,
        14: 322,
        15: 348,
    }
}

for sheet, tables in table_rows.items():
    df = pd.read_excel(
        file_path,
        sheet_name=sheet,
        header=None
    )

    for table_number, excel_row in tables.items():
        print("\n" + "=" * 75)
        print(f"{sheet} | TABLE {table_number}")
        print("=" * 75)

        # Convert Excel row number to pandas index
        start = excel_row - 1

        # Display first 13 rows and first 8 columns
        preview = df.iloc[start:start + 13, :8]

        print(preview.to_string(
            index=False,
            header=False
        ))
