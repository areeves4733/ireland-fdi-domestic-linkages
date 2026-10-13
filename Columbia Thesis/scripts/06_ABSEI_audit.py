
from pathlib import Path
import pandas as pd

source = Path("data/raw/absei-2000-2024-all-results.xlsx")
panel = pd.read_csv("data/processed/absei_sector_panel_long.csv")

indicators = {
    "irish_materials": 9,
    "irish_services": 12,
    "value_added": 14,
    "value_added_per_employee": 15
}

print("\nNEGATIVE OBSERVATIONS")
print(panel.loc[panel["value"] < 0].to_string(index=False))

print("\nMISSING OBSERVATIONS BY YEAR AND SECTOR")
missing = panel[panel["value"].isna()]

print(
    missing.groupby(["sector", "year"])
    .size()
    .to_string()
)

print("\nORIGINAL EXCEL CELL CONTENTS FOR MISSING VALUES")

for ownership in ["FOREIGN", "IRISH"]:
    raw = pd.read_excel(source, sheet_name=ownership, header=None)

    for indicator, table_number in indicators.items():
        matches = raw.index[
            raw.iloc[:, 1].astype(str).str.startswith(
                f"Table {table_number}:"
            )
        ]

        if len(matches) != 1:
            continue

        start = matches[0]

        next_tables = raw.index[
            (raw.index > start) &
            raw.iloc[:, 1].astype(str).str.match(r"^Table \d+:")
        ]

        end = next_tables[0] if len(next_tables) else len(raw)
        section = raw.iloc[start:end]

        # Find the year header
        year_rows = section.index[
            section.eq(2000).any(axis=1)
        ]

        if len(year_rows) == 0:
            continue

        year_row = year_rows[0]

        for _, observation in missing[
            (missing["ownership"] == ownership) &
            (missing["indicator"] == indicator)
        ].iterrows():

            year = observation["year"]
            sector = observation["sector"]

            year_cols = section.columns[
                section.loc[year_row].eq(year)
            ]

            sector_rows = section.index[
                section.iloc[:, 1].eq(sector)
            ]

            if len(year_cols) and len(sector_rows):
                value = raw.iloc[
                    sector_rows[0],
                    year_cols[0]
                ]

                print(
                    f"{ownership} | {indicator} | "
                    f"{sector} | {year}: {repr(value)}"
                )
