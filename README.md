# End-to-End Retail Analytics & Data Pipeline Project

## 🚀 Project Overview
This project builds a complete data solution for a global retail superstore. It covers the entire lifecycle from raw data ingestion to advanced analytics and business storytelling.

## 🎯 Objectives
- Ingest raw retail data (CSV) and supplementary data (JSON).
- Clean and transform data using Python/Pandas.
- Design and implement a Star Schema SQL Data Warehouse.
- Build an automated ETL pipeline with logging and error handling.
- Perform advanced analytics (Customer Segmentation, Sales Forecasting).
- Generate business insights and design Power BI dashboards.

## 📁 Project Structure
- `data/`:
    - `raw/`: Original Global Superstore CSV and US State Recipes JSON.
    - `processed/`: Cleaned data in CSV and Parquet formats.
    - `retail_analytics.db`: SQLite database acting as the Data Warehouse.
- `scripts/`:
    - `data_engineering.py`: Data cleaning, feature engineering, and processing.
    - `etl_pipeline.py`: ETL logic to load data into the Star Schema.
    - `advanced_analytics.py`: K-Means clustering and Time Series forecasting.
- `sql/`:
    - `schema_design.sql`: DDL for Fact and Dimension tables.
    - `analysis_queries.sql`: Business queries using Window Functions and Joins.
- `logs/`: Execution logs for each pipeline stage.
- `outputs/`: Plots and analytical results.
- `Phase1_Data_Understanding.md`: Problem definitions and KPIs.
- `Phase6_7_PowerBI_Insights.md`: DAX measures and business insights.

## ⚙️ How to Run
1. **Setup**: Ensure you have `pandas`, `sqlalchemy`, `scikit-learn`, and `statsmodels` installed.
2. **Phase 2 (Data Engineering)**:
   ```bash
   python scripts/data_engineering.py
   ```
3. **Phase 4 (ETL Pipeline)**:
   ```bash
   python scripts/etl_pipeline.py
   ```
4. **Phase 5 (Advanced Analytics)**:
   ```bash
   python scripts/advanced_analytics.py
   ```
5. **Phase 3 (SQL Analysis)**: Use a SQLite browser or CLI to run queries in `sql/analysis_queries.sql`.

## 📊 Key Insights
- **Top Markets**: APAC and EU are the most profitable.
- **Risk Areas**: Turkey and Nigeria show negative profits due to excessive discounting.
- **Customer Segmentation**: Identified 4 segments: High Value, Loyal, At Risk, and Hibernating.
- **Forecasting**: Predicts steady growth in Q4 based on historical trends.

## 🧠 Technical Highlights
- **Modular Python**: Decoupled scripts for engineering, ETL, and analytics.
- **Star Schema**: Optimized for analytical queries (OLAP).
- **Parquet Storage**: Used for efficient data storage and retrieval.
- **Audit Logging**: Tracks ETL success and record counts.
