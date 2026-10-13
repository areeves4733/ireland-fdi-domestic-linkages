
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/processed/absei_sector_panel_long.csv"
)

output = Path("outputs/figures")
output.mkdir(parents=True, exist_ok=True)

sectors = [
    "Traditional Manufacturing",
    "Modern Manufacturing",
    "Information & Communication Services"
]

# FIGURE 1: Foreign-owned domestic purchasing
foreign = df[
    (df["ownership"] == "FOREIGN") &
    (df["indicator"].isin([
        "irish_materials",
        "irish_services"
    ])) &
    (df["sector"].isin(sectors))
]

purchases = foreign.pivot_table(
    index=["year", "sector"],
    columns="indicator",
    values="value"
)

# Require both components before adding them
purchases["total_domestic_purchases"] = purchases[
    ["irish_materials", "irish_services"]
].sum(axis=1, min_count=2)

purchases = purchases.reset_index()

plt.figure(figsize=(11, 6))

for sector in sectors:
    subset = purchases[purchases["sector"] == sector]

    plt.plot(
        subset["year"],
        subset["total_domestic_purchases"],
        marker="o",
        markersize=3,
        label=sector
    )

plt.title("Domestic Purchases by Foreign-Owned Enterprises")
plt.xlabel("Year")
plt.ylabel("Irish-sourced materials and services (€ millions, nominal)")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    output / "foreign_domestic_purchases.png",
    dpi=300
)
plt.close()

# FIGURE 2: Irish-owned value added per employee
irish = df[
    (df["ownership"] == "IRISH") &
    (df["indicator"] == "value_added_per_employee") &
    (df["sector"].isin(sectors))
]

plt.figure(figsize=(11, 6))

for sector in sectors:
    subset = irish[irish["sector"] == sector]

    plt.plot(
        subset["year"],
        subset["value"],
        marker="o",
        markersize=3,
        label=sector
    )

plt.title("Value Added per Employee in Irish-Owned Enterprises")
plt.xlabel("Year")
plt.ylabel("Value added per employee (€ thousands, nominal)")
plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    output / "irish_productivity.png",
    dpi=300
)
plt.close()

print("Figures saved to:", output)
