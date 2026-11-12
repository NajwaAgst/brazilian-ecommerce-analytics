
# Brazilian E-Commerce Analytics Dashboard

An interactive data analytics dashboard built using Python and Streamlit to explore business performance, customer purchasing behavior, and delivery performance based on the Brazilian E-Commerce Public Dataset by Olist.

## Project Overview

This project analyzes Brazilian e-commerce transactions from January 2017 to August 2018. The analysis focuses on identifying sales trends, understanding customer purchasing patterns, and evaluating delivery performance.

The results are presented through an interactive dashboard developed with Streamlit and Plotly to make business insights easier to explore and understand.

## Business Questions

This project addresses three main business questions:

1. **Sales Performance Analysis**  
   How do monthly orders, revenue, and Average Order Value (AOV) change over time?

2. **Customer Segmentation Analysis**  
   What are the characteristics of customers based on their purchasing behavior using the RFM model?

3. **Delivery Performance Analysis**  
   How well does the company perform in delivering orders on time, and what is the average delivery duration?

## Dataset

The project uses the Brazilian E-Commerce Public Dataset by Olist.

- Period: January 2017 – August 2018
- Data type: E-commerce transaction and delivery data
- Main analytical datasets:
  - `monthly_sales.csv`
  - `rfm_data.csv`
  - `delivery_data.csv`

## Tools & Technologies

- Python
- Pandas
- Streamlit
- Plotly
- Jupyter Notebook / Google Colab
- Visual Studio Code

## Analysis Methodology

### 1. Sales Performance Analysis

The analysis measures:
- Total Orders
- Total Revenue
- Average Order Value (AOV)
- Monthly sales trends

Revenue is calculated using the sum of product prices, excluding freight value.

### 2. Customer Analysis (RFM)

Customer purchasing behavior is analyzed using the RFM model:

- **Recency:** Number of days since the customer's last purchase.
- **Frequency:** Number of distinct orders made by the customer.
- **Monetary:** Total spending based on product prices.

The analysis uses `customer_unique_id` to identify individual customers.

### 3. Delivery Performance Analysis

Delivery performance is evaluated using:
- Total delivered orders
- On-time delivery rate
- Late delivery rate
- Average delivery duration
- Delivery delay distribution

An order is classified as:
- **On Time:** Actual delivery date is on or before the estimated delivery date.
- **Late:** Actual delivery date is after the estimated delivery date.

## Key Findings

### Sales Performance
- Total orders: 96,211
- Total revenue: R$13,181,027.13
- Average Order Value: R$137.00

### Customer Analysis
- Total customers: 93,104
- Average Recency: 238.24 days
- Average Frequency: 1.03 orders
- Average Monetary: R$141.57

### Delivery Performance
- Total valid deliveries: 96,203
- On-time deliveries: 88,381 (91.87%)
- Late deliveries: 7,822 (8.13%)
- Average delivery duration: 12.54 days

## Dashboard Features

The dashboard consists of three main pages:

1. **Overview**
   - Business performance KPIs
   - Monthly order and revenue trends
   - AOV analysis
   - Delivery status overview

2. **Customer Analysis**
   - Customer purchasing metrics
   - Recency distribution
   - Frequency distribution
   - Monetary distribution

3. **Delivery Analysis**
   - On-time and late delivery metrics
   - Delivery duration distribution
   - Delivery delay analysis

## Project Structure

```text
ecommerce-analytics/
│
├── app.py
├── requirements.txt
├── README.md
│
└── dashboard_data/
    ├── monthly_sales.csv
    ├── rfm_data.csv
    └── delivery_data.csv
```

## How to Run the Dashboard

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd ecommerce-analytics
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

For macOS / Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

## Conclusion

This project demonstrates how e-commerce transaction data can be transformed into meaningful business insights through exploratory data analysis and interactive visualization.

The analysis provides an overview of sales performance, customer purchasing behavior, and delivery efficiency, which can support data-driven business evaluation and decision-making.

---

**Developed as a Data Analytics Portfolio Project.**
