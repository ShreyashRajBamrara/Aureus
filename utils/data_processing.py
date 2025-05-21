import pandas as pd
import os

def load_and_process_data():
    try:
        data_path = os.path.join('data', 'aureus_expenditure_with_anomalies.csv')
        if not os.path.exists(data_path):
            # In a utils file, we shouldn't use st.error directly
            # Instead, we can return None and handle the error in the calling function (in app.py)
            print(f"Error: Data file not found: {data_path}") # Print to console for debugging
            return None
            
        # Read the CSV file
        df = pd.read_csv(data_path)
        
        # Handle missing values
        df['Vendor'].fillna('Unknown Vendor', inplace=True)
        df['Notes'].fillna('', inplace=True)
        df['Employee Name'].fillna('Unassigned', inplace=True)
        df['Department'].fillna('Unassigned', inplace=True)
        
        # Convert date format
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Ensure Amount is numeric
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df['Amount'].fillna(0, inplace=True)
        
        # Create additional time-based columns for analysis
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        df['MonthYear'] = df['Date'].dt.strftime('%b %Y')
        df['MonthYearDate'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-01'))
        df['Quarter'] = df['Date'].dt.quarter
        df['QuarterYear'] = df['Date'].dt.year.astype(str) + '-Q' + df['Date'].dt.quarter.astype(str)
        
        return df
    except Exception as e:
        print(f"Error loading data: {str(e)}") # Print error to console
        return None

def get_time_series_data(df):
    if df is None:
        return pd.DataFrame()
        
    # Group by month for time series analysis
    monthly_data = df.groupby('MonthYearDate').agg(
        Total_Amount=('Amount', 'sum'),
        Num_Transactions=('Expense ID', 'count')
    ).reset_index()
    
    return monthly_data 