
from pathlib import Path
import pandas as pd

file_path = Path("data/raw/absei-2000-2024-all-results.xlsx")
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

# Indicators to extract
indicators = {
    9: "irish_materials",
    12: "irish_services",
    14: "value_added",
    15: "value_added_per_employee"
}

sectors = [
    "Food, Drink & Primary Production",
    "Traditional Manufacturing",
    "Modern Manufacturing",
    "Energy, Water, Waste & Construction",
    "Information & Communication Services",
    "Business, Financial & Other Services"
]

records = []

for ownership in ["FOREIGN", "IRISH"]:

    df = pd.read_excel(
        file_path,
        sheet_name=ownership,
        header=None
    )

    # Locate each table dynamically
    for table_number, indicator in indicators.items():

        matches = df.index[
            df.iloc[:, 1].astype(str).str.match(
                rf"^Table {table_number}:"
            )
        ]

        if len(matches) != 1:
            raise ValueError(
                f"Could not uniquely identify Table {table_number} "
                f"in {ownership}"
            )

        start = matches[0]
        end = len(df)

        # Stop at the next table
        for i in range(start + 1, len(df)):
            cell = str(df.iloc[i, 1])
            if cell.startswith("Table "):
                end = i
                break

        section = df.iloc[start:end]

        # Identify the year-header row
        year_rows = [
            i for i in section.index
            if 2000 in section.loc[i].values
        ]

        if not year_rows:
            raise ValueError(
                f"No year header found in {ownership} Table {table_number}"
            )

        header_row = year_rows[0]

        # Map columns to years
        year_columns = {}

        for col in range(df.shape[1]):
            value = df.iloc[header_row, col]

            if isinstance(value, (int, float)) and 2000 <= value <= 2024:
                year_columns[col] = int(value)

        # Extract sector observations
        for i in range(header_row + 1, end):
            sector = str(df.iloc[i, 1]).strip()

            if sector not in sectors:
                continue

            for col, year in year_columns.items():
                value = pd.to_numeric(
                    df.iloc[i, col],
                    errors="coerce"
                )

                records.append({
                    "year": year,
                    "ownership": ownership,
                    "sector": sector,
                    "indicator": indicator,
                    "value": value
                })

clean = pd.DataFrame(records)

# Check for accidental duplicate observations
keys = ["year", "ownership", "sector", "indicator"]

if clean.duplicated(keys).any():
    raise ValueError("Duplicate observations detected!")

clean = clean.sort_values(keys).reset_index(drop=True)

output_path = output_dir / "absei_sector_panel_long.csv"
clean.to_csv(output_path, index=False)

print("\nDATASET CREATED")
print("Observations:", len(clean))
print("Missing values:", clean["value"].isna().sum())
print("\nObservations by indicator:")
print(clean.groupby(["ownership", "indicator"]).size())
print("\nPreview:")
print(clean.head(12).to_string(index=False))
print("\nSaved to:", output_path)
