# Sales Dashboard for Regional Performance | SQL, Power BI

Queried and joined **3 sales-related tables** covering **25,000+ rows across 12 months and 5 regions** using optimized SQL joins to create consistent, analysis-ready datasets. Built **10 dynamic measures/KPIs** to track regional sales, return trends, and product performance. Detected a **~14% sales drop post-festival in the South region** — used as input to a marketing recovery plan.

## What this project does
- 3 relational tables: `sales_transactions`, `returns`, `dim_product`
- SQL schema + joins + 10 KPI/measure queries (total sales, return rate, MoM growth, top products, regional trend, etc.)
- Dashboard visuals: a static dashboard-style PNG (drop straight into your Power BI report as reference) **and** a live interactive HTML dashboard (Chart.js) you can open directly or host on GitHub Pages
- Surfaces the key insight: South region sales dipped after the festival month, visible in the "South Region — Post-Festival Dip" panel

## Tech stack
SQL (SQLite-compatible), Python (Pandas for data prep + validation), Chart.js (interactive dashboard)

## Repo structure
```
sales-dashboard-sql-powerbi/
├── data/
│   ├── sales_transactions.csv     # 25,000+ rows
│   ├── returns.csv
│   └── dim_product.csv
├── sql/
│   ├── 01_schema.sql              # table definitions + indexes
│   └── 02_queries_and_kpis.sql    # join view + 10 KPI queries
├── dashboard/
│   ├── index.html                 # interactive Chart.js dashboard
│   └── dashboard_data.json        # pre-aggregated data feeding the dashboard
├── images/
│   └── dashboard_overview.png     # static dashboard screenshot (use in README/portfolio)
├── generate_data.py                # builds the 3 CSVs
├── build_dashboard_image.py        # builds the static dashboard PNG
└── README.md
```

## How to run
```bash
pip install pandas numpy matplotlib
python generate_data.py            # creates the 3 CSVs in /data
python build_dashboard_image.py    # creates images/dashboard_overview.png
```
Open `dashboard/index.html` directly in a browser (or host the `dashboard/` folder on GitHub Pages) for the live interactive version.

Load `sql/01_schema.sql` and `sql/02_queries_and_kpis.sql` into any SQL engine (SQLite, PostgreSQL, MySQL — minor syntax tweaks for date functions may be needed outside SQLite) against the 3 CSVs to reproduce every KPI.

## Dashboard preview
![Dashboard overview](images/dashboard_overview.png)


The `dashboard/index.html` (Chart.js) and `images/dashboard_overview.png` in this repo are **preview/reference
only** — useful for a quick look at the layout in your browser or GitHub README, but they are not a substitute
for the actual Power BI report. Build the real `.pbix` using the guide before linking it as your Power BI project.

## Data note
The data is synthetically generated (`generate_data.py`) to match the scale and pattern described in the
project write-up (25,000+ rows, 12 months, 5 regions, ~14% South region post-festival dip).
