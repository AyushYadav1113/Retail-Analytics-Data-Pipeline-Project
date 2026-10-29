import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import sqlite3
from sqlalchemy import create_engine
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/logs/advanced_analytics.log"),
        logging.StreamHandler()
    ]
)

DB_PATH = "/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/data/retail_analytics.db"
engine = create_engine(f'sqlite:///{DB_PATH}')

def customer_segmentation():
    logging.info("Starting Customer Segmentation (K-Means)...")
    # Load RFM data from FactSales
    query = """
    SELECT 
        CustomerID,
        SUM(Sales) as Monetary,
        COUNT(OrderID) as Frequency,
        CAST(JULIANDAY('2015-01-01') - JULIANDAY(MAX(OrderDate)) AS INTEGER) as Recency
    FROM FactSales
    GROUP BY CustomerID
    """
    df_rfm = pd.read_sql(query, engine)
    
    # Preprocess
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(df_rfm[['Monetary', 'Frequency', 'Recency']])
    
    # K-Means
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df_rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)
    
    # Map clusters to labels
    # Cluster characteristics vary, but let's label them based on mean Monetary
    cluster_centers = df_rfm.groupby('Cluster')['Monetary'].mean().sort_values(ascending=False)
    cluster_map = cluster_centers.index
    labels = {cluster_map[0]: 'High Value', cluster_map[1]: 'Loyal', cluster_map[2]: 'At Risk', cluster_map[3]: 'Hibernating'}
    df_rfm['Advanced_Segment'] = df_rfm['Cluster'].map(labels)
    
    # Save back to SQL
    df_rfm[['CustomerID', 'Advanced_Segment']].to_sql('CustomerAnalytics', engine, if_exists='replace', index=False)
    logging.info("Customer segmentation saved to 'CustomerAnalytics' table.")

def sales_forecasting():
    logging.info("Starting Sales Forecasting...")
    query = "SELECT OrderDate, Sales FROM FactSales"
    df = pd.read_sql(query, engine)
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    
    # Resample to monthly
    monthly_sales = df.set_index('OrderDate')['Sales'].resample('MS').sum()
    
    # Simple Exponential Smoothing
    model = ExponentialSmoothing(monthly_sales, seasonal='add', seasonal_periods=12).fit()
    forecast = model.forecast(12)
    
    # Save forecast to SQL
    df_forecast = pd.DataFrame({
        'ForecastMonth': forecast.index.astype(str),
        'ForecastedSales': forecast.values
    })
    df_forecast.to_sql('SalesForecast', engine, if_exists='replace', index=False)
    logging.info("Sales forecast saved to 'SalesForecast' table.")

def identify_risks():
    logging.info("Identifying high-risk regions...")
    query = """
    SELECT 
        g.Region, 
        g.Country, 
        SUM(f.Profit) as TotalProfit,
        AVG(f.ProfitMarginPercent) as AvgMargin
    FROM FactSales f
    JOIN DimGeography g ON f.GeographyID = g.GeographyID
    GROUP BY g.Region, g.Country
    HAVING TotalProfit < 0
    ORDER BY TotalProfit ASC
    """
    df_risks = pd.read_sql(query, engine)
    df_risks.to_sql('RiskAnalysis', engine, if_exists='replace', index=False)
    logging.info(f"Identified {len(df_risks)} loss-making country-region pairs.")

if __name__ == "__main__":
    customer_segmentation()
    sales_forecasting()
    identify_risks()
