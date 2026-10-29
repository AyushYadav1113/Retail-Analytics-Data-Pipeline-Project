import sqlite3
import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/logs/sql_analysis.log"),
        logging.StreamHandler()
    ]
)

DB_PATH = "/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/data/retail_analytics.db"
OUTPUT_DIR = "/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/outputs/analytics"

def run_analysis():
    if not os.path.exists(DB_PATH):
        logging.error("Database not found. Please run the ETL pipeline first.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    
    queries = {
        "top_10_customers": """
            SELECT c.CustomerName, SUM(f.Sales) as TotalRevenue
            FROM FactSales f
            JOIN DimCustomer c ON f.CustomerID = c.CustomerID
            GROUP BY c.CustomerName
            ORDER BY TotalRevenue DESC
            LIMIT 10;
        """,
        "region_wise_profit": """
            SELECT g.Region, SUM(f.Profit) as TotalProfit
            FROM FactSales f
            JOIN DimGeography g ON f.GeographyID = g.GeographyID
            GROUP BY g.Region
            ORDER BY TotalProfit DESC;
        """,
        "monthly_sales_trend": """
            SELECT t.Year, t.Month, SUM(f.Sales) as MonthlySales
            FROM FactSales f
            JOIN DimTime t ON f.OrderDate = t.OrderDate
            GROUP BY t.Year, t.Month
            ORDER BY t.Year, t.Month;
        """,
        "loss_making_products": """
            SELECT p.ProductName, SUM(f.Profit) as TotalProfit
            FROM FactSales f
            JOIN DimProduct p ON f.ProductID = p.ProductID
            GROUP BY p.ProductName
            HAVING TotalProfit < 0
            ORDER BY TotalProfit ASC
            LIMIT 20;
        """,
        "rank_vs_dense_rank": """
            SELECT c.CustomerName, SUM(f.Sales) as TotalSales,
                   RANK() OVER (ORDER BY SUM(f.Sales) DESC) as SalesRank,
                   DENSE_RANK() OVER (ORDER BY SUM(f.Sales) DESC) as SalesDenseRank
            FROM FactSales f
            JOIN DimCustomer c ON f.CustomerID = c.CustomerID
            GROUP BY c.CustomerName
            LIMIT 20;
        """,
        "regional_product_performance": """
            SELECT g.Region, p.Category, p.ProductName, SUM(f.Sales) as CategorySales,
                   RANK() OVER (PARTITION BY g.Region, p.Category ORDER BY SUM(f.Sales) DESC) as ProductRankInRegion
            FROM FactSales f
            JOIN DimProduct p ON f.ProductID = p.ProductID
            JOIN DimGeography g ON f.GeographyID = g.GeographyID
            GROUP BY g.Region, p.Category, p.ProductName
            LIMIT 30;
        """
    }

    logging.info("Running SQL Analysis queries and saving results...")
    
    for name, query in queries.items():
        try:
            df = pd.read_sql_query(query, conn)
            output_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
            df.to_csv(output_path, index=False)
            logging.info(f"Saved: {output_path}")
        except Exception as e:
            logging.error(f"Error running query '{name}': {e}")
            
    conn.close()
    logging.info("SQL Analysis completed successfully.")

if __name__ == "__main__":
    run_analysis()
