-- Indexing Strategy for Retail Analytics Database
-- Purpose: Optimize join performance and speed up common filtering/aggregation operations.

-- 1. Foreign Key Indexes on Fact Table
-- These are critical for speeding up JOINs between Fact and Dimension tables.
CREATE INDEX IF NOT EXISTS idx_fact_customer ON FactSales(CustomerID);
CREATE INDEX IF NOT EXISTS idx_fact_product ON FactSales(ProductID);
CREATE INDEX IF NOT EXISTS idx_fact_geography ON FactSales(GeographyID);
CREATE INDEX IF NOT EXISTS idx_fact_date ON FactSales(OrderDate);

-- 2. Filtering and Sorting Indexes
-- Optimize common WHERE clause filters and ORDER BY operations.
CREATE INDEX IF NOT EXISTS idx_fact_sales_profit ON FactSales(Profit); -- For loss analysis
CREATE INDEX IF NOT EXISTS idx_fact_discount ON FactSales(Discount); -- For discount impact analysis

-- 3. Dimension Table Indexes
-- Optimize lookups and filtering on dimension attributes.
CREATE INDEX IF NOT EXISTS idx_dim_customer_segment ON DimCustomer(Segment);
CREATE INDEX IF NOT EXISTS idx_dim_product_cat ON DimProduct(Category, SubCategory);
CREATE INDEX IF NOT EXISTS idx_dim_geo_region ON DimGeography(Region, Market);
CREATE INDEX IF NOT EXISTS idx_dim_time_year_month ON DimTime(Year, Month);

-- 4. Composite Indexes for Common Groupings
-- Useful for the Executive Summary and Monthly Trend reports.
CREATE INDEX IF NOT EXISTS idx_fact_composite_report ON FactSales(OrderDate, GeographyID, Sales);

-- Verify Indexes
-- SELECT name FROM sqlite_master WHERE type='index';
