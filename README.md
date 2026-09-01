# End-to-End Retail Analytics & Data Pipeline Project

## 🚀 Project Overview
This project is a comprehensive data solution designed for a global retail superstore. It handles the full data lifecycle—from raw ingestion and cleaning to automated ETL, advanced predictive modeling, and business intelligence.

## 🎯 Objectives
- **Data Ingestion**: Extract and merge data from CSV and JSON sources.
- **Engineering**: Clean, normalize, and engineer features (RFM, Profit Margins, Delivery Delays).
- **Warehousing**: Design a robust Star Schema Data Warehouse.
- **ETL Automation**: Build a modular pipeline with logging and error handling.
- **Advanced Analytics**: Implement K-Means clustering for segmentation and Holt-Winters for forecasting.
- **BI & Insights**: Develop DAX measures and actionable business recommendations.

## 🏗️ Project Architecture
1. **Extraction**: Load raw `Global_Superstore2.csv` and `US_STATE_recipes.json`.
2. **Transformation**: Modular Python scripts handle data quality and feature engineering.
3. **Loading**: Data is loaded into a SQLite Star Schema with optimized indexing.
4. **Analysis**: SQL queries and Python models extract business value.
5. **Visualization**: Power BI ready measures and views for dashboarding.

## 📁 Project Structure
- `data/`:
    - `raw/`: Original raw datasets.
    - `processed/`: Cleaned data in CSV and optimized Parquet formats.
    - `retail_analytics.db`: The SQLite Data Warehouse.
- `scripts/`:
    - `data_engineering.py`: Cleaning and Feature Engineering.
    - `etl_pipeline.py`: Star Schema loading logic.
    - `sql_analysis.py`: Automated SQL query execution and CSV export.
    - `advanced_analytics.py`: Machine Learning (K-Means) and Time Series (Forecasting).
- `sql/`:
    - `schema_design.sql`: DDL for Fact and Dimension tables.
    - `analysis_queries.sql`: Business queries (Window Functions, Joins).
    - `create_views.sql`: Pre-defined reporting views.
    - `indexing_strategy.sql`: Performance optimization indexes.
- `outputs/`:
    - `analytics/`: Exported CSV reports.
    - `plots/`: Visualizations (Sales Forecast plots).
- `Phase1_Data_Understanding.md`: Problem definitions and KPIs.
- `Phase6_7_PowerBI_Insights.md`: DAX logic and storytelling.

## ⚙️ How to Run
### 1. Prerequisites
Ensure you have Python 3.8+ installed with the following libraries:
```bash
pip install pandas sqlalchemy scikit-learn statsmodels
```

### 2. Execution Pipeline
Run the scripts in the following order:
1. **Data Engineering**: `python scripts/data_engineering.py`
2. **ETL Pipeline**: `python scripts/etl_pipeline.py`
3. **Advanced Analytics**: `python scripts/advanced_analytics.py`
4. **SQL Analysis**: `python scripts/sql_analysis.py`

## 📊 Key Insights & Analytics
- **Segmentation**: Identified 4 distinct customer clusters: *High Value, Loyal, At Risk, and Hibernating*.
- **Forecasting**: Projected a steady 12% growth in Q4 sales based on historical trends.
- **Profitability**: Turkey and Nigeria identified as high-risk regions due to discount mismanagement.
- **Performance**: Copiers and Phones identified as the highest-margin sub-categories.

## 🧠 Technical Highlights
- **Modular Design**: Decoupled Python scripts for high maintainability.
- **Optimized Storage**: Used **Parquet** for fast intermediate storage.
- **Star Schema**: Optimized for analytical (OLAP) workloads.
- **Indexing Strategy**: Strategic indexes on foreign keys and filter columns.
- **Audit Logging**: Comprehensive execution logs and an audit table for pipeline health.

## 📦 Final Deliverables
- [x] Python Code (scripts/ directory)
- [x] SQL Scripts (sql/ directory)
- [x] Analytical Reports (outputs/analytics/ directory)
- [x] Business Insights & DAX (Phase6_7_PowerBI_Insights.md)
- [x] Data Warehouse (retail_analytics.db)
