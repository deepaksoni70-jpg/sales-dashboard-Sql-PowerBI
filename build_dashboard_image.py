"""
build_dashboard_image.py
Builds a static multi-panel PNG that mimics the look of the Power BI
regional sales dashboard (KPI cards + charts), using the SQL-joined data.
Use this as the dashboard screenshot for your GitHub README / portfolio.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sales = pd.read_csv("data/sales_transactions.csv")
product = pd.read_csv("data/dim_product.csv")
returns = pd.read_csv("data/returns.csv")

sales["OrderDate"] = pd.to_datetime(sales["OrderDate"])
sales["OrderMonth"] = sales["OrderDate"].dt.to_period("M").astype(str)
df = sales.merge(product, on="ProductID")

total_sales = df["SalesAmount"].sum()
total_orders = len(df)
avg_order = df["SalesAmount"].mean()
return_rate = 100 * df["TransactionID"].isin(returns["TransactionID"]).sum() / total_orders

fig = plt.figure(figsize=(15, 9), facecolor="#F4F6F8")
gs = gridspec.GridSpec(4, 4, figure=fig, hspace=0.75, wspace=0.4)

# --- Title bar ---
fig.suptitle("Regional Sales Performance Dashboard", fontsize=20, fontweight="bold", color="#1F2A44", x=0.02, ha="left")
fig.text(0.02, 0.935, "FY2025  |  All Regions  |  12 Months", fontsize=11, color="#5A6472")

# --- KPI cards ---
kpis = [
    ("Total Sales", f"₹{total_sales/1e7:.2f} Cr"),
    ("Total Orders", f"{total_orders:,}"),
    ("Avg Order Value", f"₹{avg_order:,.0f}"),
    ("Return Rate", f"{return_rate:.1f}%"),
]
for i, (label, value) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor("white")
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor="white", edgecolor="#D8DEE6", linewidth=1))
    ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=18, fontweight="bold", color="#1F2A44")
    ax.text(0.5, 0.25, label, ha="center", va="center", fontsize=11, color="#5A6472")

# --- Monthly sales trend ---
ax1 = fig.add_subplot(gs[1:3, 0:3])
monthly = df.groupby("OrderMonth")["SalesAmount"].sum() / 1e7
monthly.plot(ax=ax1, marker="o", color="#2E5EAA", linewidth=2)
ax1.set_title("Monthly Sales Trend (₹ Cr)", fontsize=12, fontweight="bold", loc="left", color="#1F2A44")
ax1.set_xlabel(""); ax1.set_ylabel("₹ Cr")
ax1.tick_params(axis="x", rotation=45)
ax1.grid(alpha=0.3)

# --- Sales by region ---
ax2 = fig.add_subplot(gs[1, 3])
region_sales = df.groupby("Region")["SalesAmount"].sum().sort_values(ascending=False) / 1e7
region_sales.plot.bar(ax=ax2, color="#4C8BF5")
ax2.set_title("Sales by Region (₹ Cr)", fontsize=11, fontweight="bold", loc="left", color="#1F2A44")
ax2.set_xlabel(""); ax2.tick_params(axis="x", rotation=30)
ax2.grid(alpha=0.3, axis="y")

# --- Sales by category ---
ax3 = fig.add_subplot(gs[2, 3])
cat_sales = df.groupby("Category")["SalesAmount"].sum().sort_values(ascending=False) / 1e7
cat_sales.plot.barh(ax=ax3, color="#7CA5E8")
ax3.set_title("Sales by Category (₹ Cr)", fontsize=11, fontweight="bold", loc="left", color="#1F2A44")
ax3.grid(alpha=0.3, axis="x")

# --- South region monthly trend (highlighting post-festival dip) ---
ax4 = fig.add_subplot(gs[3, 0:2])
south = df[df["Region"] == "South"].groupby("OrderMonth")["SalesAmount"].sum() / 1e7
south.plot(ax=ax4, marker="o", color="#D9534F", linewidth=2)
ax4.axvspan(9, 10, color="#D9534F", alpha=0.1)
ax4.set_title("South Region: Post-Festival Dip Detected (Oct -> Nov)", fontsize=11, fontweight="bold", loc="left", color="#1F2A44")
ax4.tick_params(axis="x", rotation=45)
ax4.grid(alpha=0.3)

# --- Return reasons ---
ax5 = fig.add_subplot(gs[3, 2:4])
reason_counts = returns["Reason"].value_counts()
reason_counts.plot.bar(ax=ax5, color="#F0AD4E")
ax5.set_title("Return Reasons Breakdown", fontsize=11, fontweight="bold", loc="left", color="#1F2A44")
ax5.tick_params(axis="x", rotation=20)
ax5.grid(alpha=0.3, axis="y")

plt.savefig("images/dashboard_overview.png", dpi=140, bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved images/dashboard_overview.png")
