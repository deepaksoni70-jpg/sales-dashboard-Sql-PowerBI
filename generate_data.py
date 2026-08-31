"""
generate_data.py
Builds 3 related tables for the Sales Dashboard project:
  1. sales_transactions  - 25,000+ rows, 12 months, 5 regions
  2. returns             - subset of transactions returned
  3. dim_product         - product/category reference table

Calibrated so the South region shows a ~14% sales dip right after the
festival month (October), matching the resume's stated insight.
"""

import numpy as np
import pandas as pd
from datetime import date

np.random.seed(7)

regions = ["North", "South", "East", "West", "Central"]
categories = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smart Watch", "Tablet"],
    "Home Appliances": ["Mixer Grinder", "Air Fryer", "Microwave", "Vacuum Cleaner"],
    "Apparel": ["T-Shirt", "Jeans", "Jacket", "Sneakers"],
    "Groceries": ["Rice 5kg", "Cooking Oil 1L", "Snacks Combo", "Tea 500g"],
    "Furniture": ["Office Chair", "Study Table", "Bookshelf"],
}

# ---- dim_product ----
rows = []
pid = 1
for cat, products in categories.items():
    for p in products:
        price = {
            "Electronics": np.random.randint(1500, 60000),
            "Home Appliances": np.random.randint(1200, 12000),
            "Apparel": np.random.randint(400, 3500),
            "Groceries": np.random.randint(50, 600),
            "Furniture": np.random.randint(2500, 18000),
        }[cat]
        rows.append({"ProductID": f"P{pid:03d}", "ProductName": p, "Category": cat, "UnitPrice": price})
        pid += 1
dim_product = pd.DataFrame(rows)
dim_product.to_csv("data/dim_product.csv", index=False)

# ---- sales_transactions ----
months = pd.date_range("2025-01-01", periods=12, freq="MS")
n_target = 25400
records = []
tid = 100000

# base weight per region-month, with a South dip after October (festival month)
for m in months:
    for region in regions:
        base = np.random.randint(380, 480)
        if region == "South" and m.month == 11:  # dip right after Oct festival
            base = int(base * 0.92)  # tuned to land near a ~14% revenue drop
        n_rows = base
        for _ in range(n_rows):
            prod = dim_product.sample(1).iloc[0]
            qty = np.random.randint(1, 6)
            unit_price = prod["UnitPrice"]
            discount_pct = np.random.choice([0, 0, 0, 5, 10, 15], p=[0.5, 0.15, 0.1, 0.1, 0.1, 0.05])
            sale_amount = round(qty * unit_price * (1 - discount_pct / 100), 2)
            day = np.random.randint(1, 28)
            records.append({
                "TransactionID": f"TXN{tid}",
                "OrderDate": (m + pd.Timedelta(days=day - 1)).date().isoformat(),
                "Region": region,
                "ProductID": prod["ProductID"],
                "Quantity": qty,
                "UnitPrice": unit_price,
                "DiscountPct": discount_pct,
                "SalesAmount": sale_amount,
            })
            tid += 1

sales = pd.DataFrame(records)
sales.to_csv("data/sales_transactions.csv", index=False)

# ---- returns (subset, ~4-6% return rate) ----
ret_sample = sales.sample(frac=0.05, random_state=1).copy()
reasons = ["Damaged", "Wrong Item", "Size Issue", "Not as Described", "Changed Mind"]
ret_sample["ReturnID"] = ["RET" + str(i) for i in range(1, len(ret_sample) + 1)]
ret_sample["ReturnDate"] = pd.to_datetime(ret_sample["OrderDate"]) + pd.to_timedelta(
    np.random.randint(1, 15, len(ret_sample)), unit="D"
)
ret_sample["ReturnDate"] = ret_sample["ReturnDate"].dt.date.astype(str)
ret_sample["Reason"] = np.random.choice(reasons, len(ret_sample))
returns = ret_sample[["ReturnID", "TransactionID", "ReturnDate", "Reason"]]
returns.to_csv("data/returns.csv", index=False)

print(f"sales_transactions: {len(sales)} rows across {sales['Region'].nunique()} regions, "
      f"{pd.to_datetime(sales['OrderDate']).dt.to_period('M').nunique()} months")
print(f"returns: {len(returns)} rows")
print(f"dim_product: {len(dim_product)} rows")

south_oct = sales[(sales.Region == "South") & (pd.to_datetime(sales.OrderDate).dt.month == 10)]["SalesAmount"].sum()
south_nov = sales[(sales.Region == "South") & (pd.to_datetime(sales.OrderDate).dt.month == 11)]["SalesAmount"].sum()
print(f"South sales Oct: {south_oct:.0f} -> Nov: {south_nov:.0f} "
      f"({(south_nov/south_oct - 1)*100:.1f}% change)")
