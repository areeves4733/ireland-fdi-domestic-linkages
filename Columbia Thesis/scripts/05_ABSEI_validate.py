
from pathlib import Path
import pandas as pd

file_path = Path("data/processed/absei_sector_panel_long.csv")
df = pd.read_csv(file_path)

print("\nMISSING VALUES BY INDICATOR AND OWNERSHIP")
print(
    df.groupby(["ownership", "indicator"])["value"]
    .apply(lambda x: x.isna().sum())
    .to_string()
)

print("\nMISSING VALUES BY YEAR")
print(
    df.groupby("year")["value"]
    .apply(lambda x: x.isna().sum())
    .to_string()
)

print("\nMISSING VALUES BY SECTOR")
print(
    df.groupby("sector")["value"]
    .apply(lambda x: x.isna().sum())
    .to_string()
)

print("\n2024 VALUES")
latest = df[df["year"] == 2024]

print(
    latest.pivot_table(
        index=["sector", "ownership"],
        columns="indicator",
        values="value",
        dropna=False
    ).to_string()
)

print("\nDATA VALIDATION")
print("Years:", df["year"].min(), "to", df["year"].max())
print("Duplicate rows:", df.duplicated(
    ["year", "ownership", "sector", "indicator"]
).sum())
print("Negative values:", (df["value"] < 0).sum())
