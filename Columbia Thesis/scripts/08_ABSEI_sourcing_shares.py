
from pathlib import Path
import pandas as pd

source = Path("data/raw/absei-2000-2024-all-results.xlsx")
output = Path("data/processed/absei_sourcing_shares.csv")

indicators = {
    10: "irish_materials_share",
    13: "irish_services_share"
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
    df = pd.read_excel(source, sheet_name=ownership, header=None)

    for table_number, indicator in indicators.items():
        matches = df.index[
            df.iloc[:, 1].astype(str).str.match(
                rf"^Table {table_number}:"
            )
        ]

        if len(matches) != 1:
            raise ValueError(
                f"Cannot identify Table {table_number} in {ownership}"
            )

        start = matches[0]

        next_tables = df.index[
            (df.index > start) &
            df.iloc[:, 1].astype(str).str.match(r"^Table \d+:")
        ]

        end = next_tables[0] if len(next_tables) else len(df)
        section = df.iloc[start:end]

        year_rows = section.index[
            section.eq(2000).any(axis=1)
        ]

        if len(year_rows) == 0:
            raise ValueError("Year header not found")

        header_row = year_rows[0]

        year_columns = {}

        for col in df.columns:
            year = df.iloc[header_row, col]

            if isinstance(year, (int, float)) and 2000 <= year <= 2024:
                year_columns[col] = int(year)

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

shares = pd.DataFrame(records)

keys = ["year", "ownership", "sector", "indicator"]

if shares.duplicated(keys).any():
    raise ValueError("Duplicate observations detected")

shares = shares.sort_values(keys).reset_index(drop=True)
shares.to_csv(output, index=False)

print("\nSOURCING SHARE DATASET CREATED")
print("Observations:", len(shares))
print("Missing values:", shares["value"].isna().sum())

print("\nValue ranges:")
print(
    shares.groupby(["ownership", "indicator"])["value"]
    .agg(["min", "max", "count"])
)

print("\n2024 FOREIGN-OWNED SOURCING SHARES")
print(
    shares[
        (shares["year"] == 2024) &
        (shares["ownership"] == "FOREIGN")
    ].pivot(
        index="sector",
        columns="indicator",
        values="value"
    ).to_string()
)

print("\nSaved to:", output)
