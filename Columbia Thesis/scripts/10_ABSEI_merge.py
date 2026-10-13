
from pathlib import Path
import pandas as pd

data_dir = Path("data/processed")

main = pd.read_csv(
    data_dir / "absei_sector_panel_long.csv"
)

shares = pd.read_csv(
    data_dir / "absei_sourcing_shares.csv"
)

combined = pd.concat(
    [main, shares],
    ignore_index=True
)

keys = ["year", "ownership", "sector", "indicator"]

if combined.duplicated(keys).any():
    raise ValueError("Duplicate observations detected")

panel = combined.pivot(
    index=["year", "ownership", "sector"],
    columns="indicator",
    values="value"
).reset_index()

panel.columns.name = None

output = data_dir / "absei_master_panel.csv"
panel.to_csv(output, index=False)

print("\nMASTER PANEL CREATED")
print("Rows:", len(panel))
print("Columns:", len(panel.columns))

print("\nVARIABLES:")
print(panel.columns.tolist())

print("\nMISSING VALUES:")
print(panel.isna().sum())

print("\nPREVIEW:")
print(panel.head(10).to_string(index=False))

print("\nSaved to:", output)
