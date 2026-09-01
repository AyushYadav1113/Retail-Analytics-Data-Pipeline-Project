-- Star Schema Design for Retail Analytics

-- Dimension: Customer
CREATE TABLE IF NOT EXISTS DimCustomer (
    CustomerID VARCHAR(50) PRIMARY KEY,
    CustomerName VARCHAR(255),
    Segment VARCHAR(50),
    CustomerSegment VARCHAR(50)
);

-- Dimension: Product
CREATE TABLE IF NOT EXISTS DimProduct (
    ProductID VARCHAR(50) PRIMARY KEY,
    ProductName VARCHAR(255),
    Category VARCHAR(50),
    SubCategory VARCHAR(50)
);

-- Dimension: Geography
CREATE TABLE IF NOT EXISTS DimGeography (
    GeographyID INTEGER PRIMARY KEY AUTOINCREMENT,
    City VARCHAR(100),
    State VARCHAR(100),
    Country VARCHAR(100),
    Market VARCHAR(50),
    Region VARCHAR(50)
);

-- Dimension: Time
CREATE TABLE IF NOT EXISTS DimTime (
    OrderDate DATE PRIMARY KEY,
    Day INTEGER,
    Month INTEGER,
    Year INTEGER,
    Quarter INTEGER,
    DayOfWeek VARCHAR(20)
);

-- Fact: Sales
CREATE TABLE IF NOT EXISTS FactSales (
    RowID INTEGER PRIMARY KEY,
    OrderID VARCHAR(50),
    CustomerID VARCHAR(50),
    ProductID VARCHAR(50),
    GeographyID INTEGER,
    OrderDate DATE,
    Sales FLOAT,
    Quantity INTEGER,
    Discount FLOAT,
    Profit FLOAT,
    ShippingCost FLOAT,
    ProfitMarginPercent FLOAT,
    DeliveryDelay INTEGER,
    DiscountBucket VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES DimCustomer(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES DimProduct(ProductID),
    FOREIGN KEY (GeographyID) REFERENCES DimGeography(GeographyID),
    FOREIGN KEY (OrderDate) REFERENCES DimTime(OrderDate)
);

-- Audit Table
CREATE TABLE IF NOT EXISTS AuditLog (
    LoadID INTEGER PRIMARY KEY AUTOINCREMENT,
    LoadTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Status VARCHAR(50),
    RecordsProcessed INTEGER,
    ErrorMessage TEXT
);
