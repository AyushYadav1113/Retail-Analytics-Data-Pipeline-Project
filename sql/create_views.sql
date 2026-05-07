-- SQL Views for Retail Analytics

-- 1. Executive Summary View
-- Provides a high-level overview of sales, profit, and efficiency across regions and time.
CREATE VIEW IF NOT EXISTS View_ExecutiveSummary AS
SELECT 
    g.Region,
    g.Market,
    t.Year,
    t.Quarter,
    t.Month,
    SUM(f.Sales) as TotalSales,
    SUM(f.Profit) as TotalProfit,
    (SUM(f.Profit) / SUM(f.Sales)) * 100 as ProfitMarginPercent,
    AVG(f.DeliveryDelay) as AvgDeliveryDelay,
    COUNT(DISTINCT f.OrderID) as TotalOrders
FROM FactSales f
JOIN DimGeography g ON f.GeographyID = g.GeographyID
JOIN DimTime t ON f.OrderDate = t.OrderDate
GROUP BY g.Region, g.Market, t.Year, t.Quarter, t.Month;

-- 2. Customer Performance View
-- Analyzes customer behavior and segments.
CREATE VIEW IF NOT EXISTS View_CustomerPerformance AS
SELECT 
    c.CustomerID,
    c.CustomerName,
    c.Segment,
    c.CustomerSegment as RFM_Segment,
    COUNT(f.OrderID) as TotalOrders,
    SUM(f.Sales) as LifetimeValue,
    SUM(f.Profit) as LifetimeProfit,
    MAX(f.OrderDate) as LastOrderDate
FROM DimCustomer c
LEFT JOIN FactSales f ON c.CustomerID = f.CustomerID
GROUP BY c.CustomerID, c.CustomerName, c.Segment, c.CustomerSegment;

-- 3. Product Performance View
-- Identifies best and worst performing products and categories.
CREATE VIEW IF NOT EXISTS View_ProductPerformance AS
SELECT 
    p.Category,
    p.SubCategory,
    p.ProductName,
    SUM(f.Sales) as TotalSales,
    SUM(f.Profit) as TotalProfit,
    SUM(f.Quantity) as UnitsSold,
    AVG(f.Discount) as AvgDiscount
FROM DimProduct p
JOIN FactSales f ON p.ProductID = f.ProductID
GROUP BY p.Category, p.SubCategory, p.ProductName;

-- 4. Regional Loss Analysis View
-- Specifically focuses on regions and countries with negative profits.
CREATE VIEW IF NOT EXISTS View_RegionalLossAnalysis AS
SELECT 
    g.Market,
    g.Region,
    g.Country,
    SUM(f.Sales) as TotalSales,
    SUM(f.Profit) as TotalProfit,
    AVG(f.Discount) as AvgDiscount,
    COUNT(f.RowID) as NumberOfLossMakingTransactions
FROM DimGeography g
JOIN FactSales f ON g.GeographyID = f.GeographyID
WHERE f.Profit < 0
GROUP BY g.Market, g.Region, g.Country;

-- 5. Shipping Efficiency View
-- Analyzes delivery performance by market.
CREATE VIEW IF NOT EXISTS View_ShippingEfficiency AS
SELECT 
    g.Market,
    f.DiscountBucket,
    AVG(f.DeliveryDelay) as AvgDelayDays,
    SUM(f.ShippingCost) as TotalShippingCost,
    SUM(f.Sales) as TotalSales
FROM FactSales f
JOIN DimGeography g ON f.GeographyID = g.GeographyID
GROUP BY g.Market, f.DiscountBucket;
