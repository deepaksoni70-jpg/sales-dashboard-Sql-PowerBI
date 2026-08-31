-- Sales Dashboard for Regional Performance | SQL
-- Queries and joins 3 sales-related tables (25,000+ rows, 12 months, 5 regions)
-- to build 10 dynamic measures / KPIs for the Power BI dashboard.

-- =====================================================================
-- 0. Master analysis-ready view (joins all 3 tables)
-- =====================================================================
CREATE VIEW vw_sales_master AS
SELECT
    s.TransactionID,
    s.OrderDate,
    STRFTIME('%Y-%m', s.OrderDate) AS OrderMonth,
    s.Region,
    p.ProductID,
    p.ProductName,
    p.Category,
    s.Quantity,
    s.UnitPrice,
    s.DiscountPct,
    s.SalesAmount,
    CASE WHEN r.ReturnID IS NOT NULL THEN 1 ELSE 0 END AS IsReturned,
    r.Reason AS ReturnReason
FROM sales_transactions s
JOIN dim_product p       ON s.ProductID = p.ProductID
LEFT JOIN returns r      ON s.TransactionID = r.TransactionID;

-- =====================================================================
-- KPI 1: Total Sales
-- =====================================================================
SELECT SUM(SalesAmount) AS TotalSales FROM sales_transactions;

-- =====================================================================
-- KPI 2: Total Orders
-- =====================================================================
SELECT COUNT(*) AS TotalOrders FROM sales_transactions;

-- =====================================================================
-- KPI 3: Average Order Value
-- =====================================================================
SELECT ROUND(AVG(SalesAmount), 2) AS AvgOrderValue FROM sales_transactions;

-- =====================================================================
-- KPI 4: Return Rate (%)
-- =====================================================================
SELECT
    ROUND(100.0 * COUNT(DISTINCT r.TransactionID) / COUNT(DISTINCT s.TransactionID), 2) AS ReturnRatePct
FROM sales_transactions s
LEFT JOIN returns r ON s.TransactionID = r.TransactionID;

-- =====================================================================
-- KPI 5: Sales by Region
-- =====================================================================
SELECT Region, SUM(SalesAmount) AS RegionSales
FROM sales_transactions
GROUP BY Region
ORDER BY RegionSales DESC;

-- =====================================================================
-- KPI 6: Sales by Product Category
-- =====================================================================
SELECT p.Category, SUM(s.SalesAmount) AS CategorySales
FROM sales_transactions s
JOIN dim_product p ON s.ProductID = p.ProductID
GROUP BY p.Category
ORDER BY CategorySales DESC;

-- =====================================================================
-- KPI 7: Month-over-Month Sales Trend
-- =====================================================================
SELECT
    STRFTIME('%Y-%m', OrderDate) AS OrderMonth,
    SUM(SalesAmount) AS MonthlySales
FROM sales_transactions
GROUP BY OrderMonth
ORDER BY OrderMonth;

-- =====================================================================
-- KPI 8: Top 5 Best-Selling Products by Revenue
-- =====================================================================
SELECT p.ProductName, SUM(s.SalesAmount) AS Revenue, SUM(s.Quantity) AS UnitsSold
FROM sales_transactions s
JOIN dim_product p ON s.ProductID = p.ProductID
GROUP BY p.ProductName
ORDER BY Revenue DESC
LIMIT 5;

-- =====================================================================
-- KPI 9: Regional Month-over-Month % Growth (used to detect the South dip)
-- =====================================================================
WITH monthly_region AS (
    SELECT Region, STRFTIME('%Y-%m', OrderDate) AS OrderMonth, SUM(SalesAmount) AS Sales
    FROM sales_transactions
    GROUP BY Region, OrderMonth
)
SELECT
    Region,
    OrderMonth,
    Sales,
    LAG(Sales) OVER (PARTITION BY Region ORDER BY OrderMonth) AS PrevMonthSales,
    ROUND(100.0 * (Sales - LAG(Sales) OVER (PARTITION BY Region ORDER BY OrderMonth))
        / LAG(Sales) OVER (PARTITION BY Region ORDER BY OrderMonth), 2) AS MoM_GrowthPct
FROM monthly_region
ORDER BY Region, OrderMonth;

-- =====================================================================
-- KPI 10: Return Reasons Breakdown
-- =====================================================================
SELECT Reason, COUNT(*) AS ReturnCount
FROM returns
GROUP BY Reason
ORDER BY ReturnCount DESC;

-- =====================================================================
-- Insight query: South region post-festival dip (Oct -> Nov)
-- =====================================================================
SELECT
    STRFTIME('%Y-%m', OrderDate) AS OrderMonth,
    SUM(SalesAmount) AS SouthSales
FROM sales_transactions
WHERE Region = 'South'
  AND STRFTIME('%m', OrderDate) IN ('10', '11')
GROUP BY OrderMonth
ORDER BY OrderMonth;
