import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_and_process_data(file_path='../data/aureus_expenditure_with_anomalies.csv'):
    """
    Load and process the expenditure data from CSV file
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file containing expenditure data
        
    Returns:
    --------
    pandas.DataFrame
        Processed dataframe with proper data types and handled missing values
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Handle missing values
    df['Vendor'].fillna('Unknown Vendor', inplace=True)
    df['Notes'].fillna('', inplace=True)
    
    # Convert date format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Ensure Amount is numeric
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    
    # Fill any NaN values in Amount with 0
    df['Amount'].fillna(0, inplace=True)
    
    # Create Month and Year columns for easier aggregation
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['MonthYear'] = df['Date'].dt.strftime('%b %Y')
    
    # Create a Month-Year datetime for proper time series ordering
    df['MonthYearDate'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-01'))
    
    return df

def detect_anomalies(df):
    """
    Detect anomalies in the expenditure data
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataframe with expenditure data
        
    Returns:
    --------
    pandas.DataFrame
        Dataframe containing only anomalous entries
    """
    anomalies = []
    
    # Check for unusually high expenses (above 3 standard deviations)
    mean_amount = df['Amount'].mean()
    std_amount = df['Amount'].std()
    high_amount_threshold = mean_amount + 3 * std_amount
    high_amount_anomalies = df[df['Amount'] > high_amount_threshold].copy()
    if not high_amount_anomalies.empty:
        high_amount_anomalies['Anomaly_Type'] = 'Unusually High Amount'
        anomalies.append(high_amount_anomalies)
    
    # Check for future dates
    today = pd.Timestamp.now()
    future_date_anomalies = df[df['Date'] > today].copy()
    if not future_date_anomalies.empty:
        future_date_anomalies['Anomaly_Type'] = 'Future Date'
        anomalies.append(future_date_anomalies)
    
    # Check for missing vendor info (should be 'Unknown Vendor' after processing)
    missing_vendor_anomalies = df[df['Vendor'] == 'Unknown Vendor'].copy()
    if not missing_vendor_anomalies.empty:
        missing_vendor_anomalies['Anomaly_Type'] = 'Missing Vendor Information'
        anomalies.append(missing_vendor_anomalies)
    
    # Check for specific notes indicating anomalies
    notes_anomalies = df[df['Notes'].str.contains('suspicious|anomaly|fraud|error', case=False, na=False)].copy()
    if not notes_anomalies.empty:
        notes_anomalies['Anomaly_Type'] = 'Flagged in Notes'
        anomalies.append(notes_anomalies)
    
    # Combine all anomalies
    if anomalies:
        return pd.concat(anomalies).drop_duplicates()
    else:
        return pd.DataFrame(columns=df.columns.tolist() + ['Anomaly_Type'])

def get_department_metrics(df):
    """
    Calculate key metrics for each department
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataframe with expenditure data
        
    Returns:
    --------
    pandas.DataFrame
        Dataframe containing department metrics
    """
    dept_metrics = df.groupby('Department').agg(
        Total_Spent=('Amount', 'sum'),
        Avg_Per_Transaction=('Amount', 'mean'),
        Num_Transactions=('Expense ID', 'count')
    ).reset_index()
    
    return dept_metrics

def get_employee_metrics(df):
    """
    Calculate key metrics for each employee
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataframe with expenditure data
        
    Returns:
    --------
    pandas.DataFrame
        Dataframe containing employee metrics
    """
    employee_metrics = df.groupby('Employee Name').agg(
        Total_Spent=('Amount', 'sum'),
        Avg_Per_Transaction=('Amount', 'mean'),
        Num_Transactions=('Expense ID', 'count')
    ).reset_index()
    
    # Sort by total spent in descending order
    employee_metrics = employee_metrics.sort_values('Total_Spent', ascending=False)
    
    return employee_metrics

def get_time_series_data(df):
    """
    Aggregate data by month for time series analysis
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataframe with expenditure data
        
    Returns:
    --------
    pandas.DataFrame
        Dataframe aggregated by month
    """
    monthly_data = df.groupby('MonthYearDate').agg(
        Total_Amount=('Amount', 'sum'),
        Num_Transactions=('Expense ID', 'count')
    ).reset_index()
    
    return monthly_data
