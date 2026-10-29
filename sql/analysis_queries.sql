-- 1. Top 10 customers by revenue
SELECT 
    c.CustomerName, 
    SUM(f.Sales) as TotalRevenue
FROM FactSales f
JOIN DimCustomer c ON f.CustomerID = c.CustomerID
GROUP BY c.CustomerName
ORDER BY TotalRevenue DESC
LIMIT 10;

-- 2. Region-wise profit
SELECT 
    g.Region, 
    SUM(f.Profit) as TotalProfit
FROM FactSales f
JOIN DimGeography g ON f.GeographyID = g.GeographyID
GROUP BY g.Region
ORDER BY TotalProfit DESC;

-- 3. Monthly sales trend
SELECT 
    t.Year, 
    t.Month, 
    SUM(f.Sales) as MonthlySales
FROM FactSales f
JOIN DimTime t ON f.OrderDate = t.OrderDate
GROUP BY t.Year, t.Month
ORDER BY t.Year, t.Month;

-- 4. Loss-making products
SELECT 
    p.ProductName, 
    SUM(f.Profit) as TotalProfit
FROM FactSales f
JOIN DimProduct p ON f.ProductID = p.ProductID
GROUP BY p.ProductName
HAVING TotalProfit < 0
ORDER BY TotalProfit ASC
LIMIT 20;

-- 5. View for Executive Summary
CREATE VIEW IF NOT EXISTS View_ExecutiveSummary AS
SELECT 
    g.Region,
    g.Market,
    t.Year,
    t.Quarter,
    SUM(f.Sales) as TotalSales,
    SUM(f.Profit) as TotalProfit,
    AVG(f.ProfitMarginPercent) as AvgProfitMargin,
    AVG(f.DeliveryDelay) as AvgDeliveryDelay
FROM FactSales f
JOIN DimGeography g ON f.GeographyID = g.GeographyID
JOIN DimTime t ON f.OrderDate = t.OrderDate
GROUP BY g.Region, g.Market, t.Year, t.Quarter;

-- 6. Using Window Functions: RANK vs DENSE_RANK
-- Rank customers by sales globally
SELECT 
    c.CustomerName,
    SUM(f.Sales) as TotalSales,
    RANK() OVER (ORDER BY SUM(f.Sales) DESC) as SalesRank,
    DENSE_RANK() OVER (ORDER BY SUM(f.Sales) DESC) as SalesDenseRank
FROM FactSales f
JOIN DimCustomer c ON f.CustomerID = c.CustomerID
GROUP BY c.CustomerName
LIMIT 20;

-- 7. Using Window Functions: Region-wise Product Performance
SELECT 
    g.Region,
    p.Category,
    p.ProductName,
    SUM(f.Sales) as CategorySales,
    RANK() OVER (PARTITION BY g.Region, p.Category ORDER BY SUM(f.Sales) DESC) as ProductRankInRegion
FROM FactSales f
JOIN DimProduct p ON f.ProductID = p.ProductID
JOIN DimGeography g ON f.GeographyID = g.GeographyID
GROUP BY g.Region, p.Category, p.ProductName
LIMIT 30;
