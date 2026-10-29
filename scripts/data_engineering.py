import pandas as pd
import numpy as np
import os
import json
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/logs/data_engineering.log"),
        logging.StreamHandler()
    ]
)

def load_data(csv_path, json_path):
    logging.info("Loading CSV data...")
    try:
        df_retail = pd.read_csv(csv_path, encoding='latin1')
        logging.info(f"Retail data loaded with {len(df_retail)} records.")
    except Exception as e:
        logging.error(f"Error loading CSV: {e}")
        return None, None

    logging.info("Loading JSON data...")
    try:
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        df_json = pd.DataFrame.from_dict(json_data, orient='index')
        logging.info(f"JSON data loaded with {len(df_json)} records.")
    except Exception as e:
        logging.error(f"Error loading JSON: {e}")
        df_json = pd.DataFrame()

    return df_retail, df_json

def clean_data(df):
    logging.info("Cleaning retail data...")
    
    # Handle Missing Values
    # Postal Code has many nulls, fill with 0 or 'Unknown'
    df['Postal Code'] = df['Postal Code'].fillna(0).astype(int).astype(str)
    
    # Data Type Corrections
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y', errors='coerce')
    
    # Drop Duplicates
    initial_len = len(df)
    df = df.drop_duplicates()
    logging.info(f"Dropped {initial_len - len(df)} duplicate records.")
    
    return df

def feature_engineering(df):
    logging.info("Performing feature engineering...")
    
    # 1. Profit Margin %
    df['Profit Margin %'] = (df['Profit'] / df['Sales']) * 100
    
    # 2. Delivery Delay (Ship Date - Order Date)
    df['Delivery Delay'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    # 3. Discount Buckets
    def get_discount_bucket(d):
        if d == 0: return 'No Discount'
        if d <= 0.2: return 'Low Discount (0-20%)'
        if d <= 0.5: return 'Medium Discount (20-50%)'
        return 'High Discount (>50%)'
    
    df['Discount Bucket'] = df['Discount'].apply(get_discount_bucket)
    
    # 4. Customer Segmentation (RFM - Simplified for now)
    # Recency: Days since last order
    max_date = df['Order Date'].max()
    rfm = df.groupby('Customer ID').agg({
        'Order Date': lambda x: (max_date - x.max()).days,
        'Order ID': 'count',
        'Sales': 'sum'
    }).rename(columns={
        'Order Date': 'Recency',
        'Order ID': 'Frequency',
        'Sales': 'Monetary'
    })
    
    # Assign scores 1-5
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5])
    
    rfm['RFM_Score'] = rfm['R_Score'].astype(int) + rfm['F_Score'].astype(int) + rfm['M_Score'].astype(int)
    
    def get_segment(score):
        if score >= 13: return 'Champions'
        if score >= 10: return 'Loyal Customers'
        if score >= 7: return 'Potential Loyalists'
        if score >= 4: return 'At Risk'
        return 'Lost'
    
    rfm['Customer Segment'] = rfm['RFM_Score'].apply(get_segment)
    
    # Join back to main df
    df = df.merge(rfm[['Customer Segment']], on='Customer ID', how='left')
    
    return df

def process_and_save():
    raw_csv = "/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/data/raw/Global_Superstore2.csv"
    raw_json = "/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/data/raw/US_STATE_recipes.json"
    processed_csv = "/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/data/processed/cleaned_retail_data.csv"
    processed_parquet = "/Users/ayushyadav/Retail-Analytics-Data-Pipeline-Project/data/processed/cleaned_retail_data.parquet"
    
    df_retail, df_json = load_data(raw_csv, raw_json)
    
    if df_retail is not None:
        df_retail = clean_data(df_retail)
        df_retail = feature_engineering(df_retail)
        
        # Optionally join with JSON data if needed
        # For now, let's just save the cleaned retail data
        
        logging.info(f"Saving cleaned data to {processed_csv}...")
        df_retail.to_csv(processed_csv, index=False)
        
        logging.info(f"Saving cleaned data to {processed_parquet}...")
        df_retail.to_parquet(processed_parquet, index=False)
        
        logging.info("Data Engineering completed successfully.")

if __name__ == "__main__":
    process_and_save()
