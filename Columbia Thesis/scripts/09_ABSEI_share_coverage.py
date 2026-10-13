
import pandas as pd

df = pd.read_csv(
    "data/processed/absei_sourcing_shares.csv"
)

print("\nAVAILABLE YEARS BY INDICATOR")
for (ownership, indicator), group in df.groupby(
    ["ownership", "indicator"]
):
    years = sorted(
        group.loc[group["value"].notna(), "year"].unique()
    )
    print(f"\n{ownership} | {indicator}")
    print(years)

print("\nMISSING VALUES BY SECTOR AND INDICATOR")
print(
    df.groupby(["sector", "ownership", "indicator"])["value"]
    .apply(lambda x: x.isna().sum())
    .to_string()
)

print("\nFOREIGN-OWNED SOURCING SHARES: 2014 AND 2024")

comparison = df[
    (df["ownership"] == "FOREIGN") &
    (df["year"].isin([2014, 2024]))
]

print(
    comparison.pivot_table(
        index=["sector", "indicator"],
        columns="year",
        values="value",
        dropna=False
    ).to_string()
)
