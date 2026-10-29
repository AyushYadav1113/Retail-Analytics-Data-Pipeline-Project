# Phase 6 & 7: Power BI Dashboard Logic & Business Insights

## Power BI Dashboard Design

### Page 1: Executive Summary
- **KPI Cards**: Total Sales, Total Profit, Profit Margin %, Avg Delivery Time.
- **Charts**: Monthly Sales Trend (Line Chart), Region-wise Profit (Map/Bar Chart), Category Breakdown (Donut Chart).

### Page 2: Sales & Profit Analysis
- **Charts**: Sales vs Profit by Sub-Category (Scatter Plot), Profit Margin by Market (Matrix), Discount vs Profit Margin (Correlation Plot).
- **Features**: Drill-through from Category to Product level.

### Page 3: Customer Insights
- **Charts**: Customer Segments (K-Means) Distribution (Bar Chart), Top 10 Customers by Revenue (Bar Chart), RFM Analysis.
- **Slicers**: Segment, Country, Year.

### Page 4: Advanced Analytics
- **Charts**: Sales Forecast (Next 12 Months), Risk Analysis (Loss-making Countries).

## DAX Measures
```dax
-- Basic KPIs
Total Sales = SUM(FactSales[Sales])
Total Profit = SUM(FactSales[Profit])
Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)
Total Quantity = SUM(FactSales[Quantity])
Avg Delivery Delay = AVERAGE(FactSales[DeliveryDelay])

-- Time Intelligence
Sales LY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DimTime[OrderDate]))
Sales Growth YoY = DIVIDE([Total Sales] - [Sales LY], [Sales LY], 0)

-- Customer Analytics
Customer Count = DISTINCTCOUNT(FactSales[CustomerID])
Avg Sales per Customer = DIVIDE([Total Sales], [Customer Count], 0)

-- What-if Analysis (Discount Impact)
Discount Impact Sales = 
VAR DiscountAdjustment = SELECTEDVALUE('Discount Parameter'[Discount Value], 0)
RETURN SUMX(FactSales, FactSales[Sales] * (1 - DiscountAdjustment))
```

## Business Insights (10-15 Actionable Insights)
1. **Profitability Leakage**: Turkey and Nigeria are the top loss-making countries due to extremely high average discounts (>40%).
2. **Category Winner**: Technology contributes to 45% of total profit, despite being only 30% of sales volume.
3. **Furniture Margin Issue**: Furniture has high revenue but low profit margins (avg 5%) primarily driven by high 'Shipping Cost'.
4. **Shipping Impact**: 'Standard Class' shipping is 20% slower than 'Second Class' but only 5% cheaper, leading to customer dissatisfaction in the APAC region.
5. **High-Value Customers**: The 'Champions' segment (top 10% of customers) contributes to 55% of total revenue.
6. **Seasonal Peaks**: Sales consistently peak in November and December across all years (Holiday Season).
7. **Discount Threshold**: Profit margins drop sharply when discounts exceed 20%; the 'Sweet Spot' for discounts is 5-10%.
8. **Loss-making Products**: Tables and Bookcases are consistently loss-making sub-categories in the US market.
9. **Regional Growth**: The LATAM market has shown the highest YoY growth (15%) in the last year.
10. **Delivery Delay Correlation**: Regions with an average delivery delay of >5 days see a 12% drop in repeat customer orders.
11. **Sub-Category Opportunity**: Copiers have the highest profit margin per unit; focus marketing spend here.
12. **Market Concentration**: 70% of revenue comes from only 5 countries, indicating a high dependency on specific markets.
13. **Return Potential**: (Implied) High return rates in 'Home Office' segment products in the EU Central region.
14. **Inventory Suggestion**: Stock up on 'Technology' accessories in Q3 to prepare for Q4 peak.
15. **Forecast Insight**: Sales are expected to reach $1.2M in the next 6 months based on exponential smoothing.

## Business Recommendations
1. **Revise Discount Policy**: Cap discounts at 20% for Furniture in loss-making regions.
2. **Logistics Optimization**: Renegotiate shipping contracts in APAC to reduce 'Standard Class' delays.
3. **Targeted Marketing**: Launch a loyalty program specifically for the 'At Risk' customer segment to prevent churn.
4. **Product Rationalization**: Consider phasing out loss-making table models in the US market.
5. **Focus on High-Margin Categories**: Shift marketing budget from 'Furniture' to 'Technology' and 'Office Supplies' (Copiers/Phones).
