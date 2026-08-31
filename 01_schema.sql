-- Schema for the Sales Dashboard project
-- 3 related tables: sales_transactions, returns, dim_product

CREATE TABLE dim_product (
    ProductID   VARCHAR(10)   PRIMARY KEY,
    ProductName VARCHAR(100)  NOT NULL,
    Category    VARCHAR(50)   NOT NULL,
    UnitPrice   DECIMAL(10,2) NOT NULL
);

CREATE TABLE sales_transactions (
    TransactionID VARCHAR(15)   PRIMARY KEY,
    OrderDate     DATE          NOT NULL,
    Region        VARCHAR(20)   NOT NULL,
    ProductID     VARCHAR(10)   NOT NULL REFERENCES dim_product(ProductID),
    Quantity      INT           NOT NULL,
    UnitPrice     DECIMAL(10,2) NOT NULL,
    DiscountPct   DECIMAL(5,2)  NOT NULL,
    SalesAmount   DECIMAL(12,2) NOT NULL
);

CREATE TABLE returns (
    ReturnID      VARCHAR(15)  PRIMARY KEY,
    TransactionID VARCHAR(15)  NOT NULL REFERENCES sales_transactions(TransactionID),
    ReturnDate    DATE         NOT NULL,
    Reason        VARCHAR(50)  NOT NULL
);

-- Helpful indexes for dashboard-style filtering
CREATE INDEX idx_sales_region ON sales_transactions(Region);
CREATE INDEX idx_sales_date   ON sales_transactions(OrderDate);
CREATE INDEX idx_sales_product ON sales_transactions(ProductID);
CREATE INDEX idx_returns_txn  ON returns(TransactionID);
