# Aureus Expenditure Dashboard

A comprehensive Streamlit dashboard for analyzing startup expenditure data with company-level, department-level, and employee-level views.

## Features

### 1. Company-Level View (Macro)
- Total expenditure over time with forecasting
- Category-wise breakdown (pie chart)
- Payment method and vendor distribution
- Anomaly detection and visualization

### 2. Department-Level View (Meso)
- Filterable view to inspect expenditures by department
- Key metrics per department (total spent, average per transaction)
- Department-wise trend over time
- Compare departments side by side

### 3. Employee-Level View (Micro)
- Filterable table/chart showing expenses per employee
- Highlight top spenders
- Anomaly detection for suspicious transactions
- Employee spending pattern across time/categories

## Installation

1. Make sure you have all required dependencies installed:

```
pip install streamlit pandas prophet plotly matplotlib scikit-learn
```

2. Navigate to the dashboard directory:

```
cd dashboard
```

3. Run the Streamlit app:

```
streamlit run app.py
```

## Data Processing

The dashboard automatically:
- Loads CSV data from the `/data` directory
- Handles missing values
- Converts date formats
- Ensures numerical fields are properly typed
- Detects anomalies in the data
- Forecasts future expenditures using Prophet
