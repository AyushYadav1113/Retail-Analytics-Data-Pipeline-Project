import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import logging
import os
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/logs/etl_pipeline.log"),
        logging.StreamHandler()
    ]
)

DB_PATH = "/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/data/retail_analytics.db"
engine = create_engine(f'sqlite:///{DB_PATH}')

def run_sql_script(script_path):
    logging.info(f"Executing SQL script: {script_path}")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            with open(script_path, 'r') as f:
                sql_script = f.read()
            conn.executescript(sql_script)
        logging.info("SQL script executed successfully.")
    except Exception as e:
        logging.error(f"Error executing SQL script: {e}")

def log_audit(status, records=0, error=""):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO AuditLog (Status, RecordsProcessed, ErrorMessage) VALUES (?, ?, ?)",
                (status, records, error)
            )
    except Exception as e:
        logging.error(f"Failed to log audit: {e}")

def etl_process():
    processed_parquet = "/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/data/processed/cleaned_retail_data.parquet"
    
    if not os.path.exists(processed_parquet):
        logging.error("Processed data not found. Run data_engineering.py first.")
        return

    try:
        logging.info("Extracting data from Parquet...")
        df = pd.read_parquet(processed_parquet)
        
        # Transform: Prepare Dimension Tables
        logging.info("Transforming data for dimensions...")
        
        # DimCustomer
        dim_customer = df[['Customer ID', 'Customer Name', 'Segment', 'Customer Segment']].drop_duplicates(subset=['Customer ID'])
        dim_customer.columns = ['CustomerID', 'CustomerName', 'Segment', 'CustomerSegment']
        
        # DimProduct
        dim_product = df[['Product ID', 'Product Name', 'Category', 'Sub-Category']].drop_duplicates(subset=['Product ID'])
        dim_product.columns = ['ProductID', 'ProductName', 'Category', 'SubCategory']
        
        # DimGeography
        dim_geo = df[['City', 'State', 'Country', 'Market', 'Region']].drop_duplicates()
        dim_geo = dim_geo.reset_index(drop=True)
        dim_geo['GeographyID'] = dim_geo.index + 1
        
        # DimTime
        dim_time = pd.DataFrame({'OrderDate': df['Order Date'].unique()})
        dim_time['Day'] = dim_time['OrderDate'].dt.day
        dim_time['Month'] = dim_time['OrderDate'].dt.month
        dim_time['Year'] = dim_time['OrderDate'].dt.year
        dim_time['Quarter'] = dim_time['OrderDate'].dt.quarter
        dim_time['DayOfWeek'] = dim_time['OrderDate'].dt.day_name()
        
        # FactSales - Join with DimGeography to get GeographyID
        logging.info("Preparing FactSales table...")
        fact_sales = df.merge(dim_geo, on=['City', 'State', 'Country', 'Market', 'Region'], how='left')
        fact_sales = fact_sales[[
            'Row ID', 'Order ID', 'Customer ID', 'Product ID', 'GeographyID', 
            'Order Date', 'Sales', 'Quantity', 'Discount', 'Profit', 
            'Shipping Cost', 'Profit Margin %', 'Delivery Delay', 'Discount Bucket'
        ]]
        fact_sales.columns = [
            'RowID', 'OrderID', 'CustomerID', 'ProductID', 'GeographyID', 
            'OrderDate', 'Sales', 'Quantity', 'Discount', 'Profit', 
            'ShippingCost', 'ProfitMarginPercent', 'DeliveryDelay', 'DiscountBucket'
        ]
        
        # Load into SQL
        logging.info("Loading data into SQL database...")
        
        # Load Dimensions (using 'replace' for simplicity in this demo, but could be 'append' with logic)
        dim_customer.to_sql('DimCustomer', engine, if_exists='replace', index=False)
        dim_product.to_sql('DimProduct', engine, if_exists='replace', index=False)
        dim_geo.to_sql('DimGeography', engine, if_exists='replace', index=False)
        dim_time.to_sql('DimTime', engine, if_exists='replace', index=False)
        
        # Load Fact (Incremental Simulation: Check existing RowIDs)
        try:
            existing_ids = pd.read_sql("SELECT RowID FROM FactSales", engine)['RowID'].tolist()
            fact_sales = fact_sales[~fact_sales['RowID'].isin(existing_ids)]
        except:
            pass # Table might not exist yet
            
        fact_sales.to_sql('FactSales', engine, if_exists='append', index=False)
        
        logging.info(f"ETL completed. {len(fact_sales)} new records loaded.")
        log_audit("SUCCESS", len(fact_sales))
        
    except Exception as e:
        logging.error(f"ETL failed: {e}")
        log_audit("FAILED", 0, str(e))

if __name__ == "__main__":
    # Ensure database schema is ready
    run_sql_script("/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/sql/schema_design.sql")
    etl_process()
