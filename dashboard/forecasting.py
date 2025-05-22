import pandas as pd
import numpy as np
from prophet import Prophet
from datetime import datetime, timedelta

def forecast_expenditure(time_series_data, periods=6):
    """
    Forecast future expenditures using Facebook Prophet
    
    Parameters:
    -----------
    time_series_data : pandas.DataFrame
        DataFrame with 'MonthYearDate' and 'Total_Amount' columns
    periods : int
        Number of months to forecast
        
    Returns:
    --------
    pandas.DataFrame
        Dataframe with forecasted values
    """
    # Prepare data for Prophet
    prophet_df = time_series_data[['MonthYearDate', 'Total_Amount']].copy()
    prophet_df.columns = ['ds', 'y']
    
    # Initialize and fit the model
    model = Prophet(yearly_seasonality=True, 
                   monthly_seasonality=True,
                   daily_seasonality=False,
                   seasonality_mode='multiplicative')
    model.fit(prophet_df)
    
    # Create future dataframe for prediction
    future = model.make_future_dataframe(periods=periods, freq='MS')
    
    # Make predictions
    forecast = model.predict(future)
    
    # Format the results
    result = pd.DataFrame({
        'Date': forecast['ds'],
        'Predicted_Amount': forecast['yhat'],
        'Lower_Bound': forecast['yhat_lower'],
        'Upper_Bound': forecast['yhat_upper'],
        'Is_Prediction': forecast['ds'] > prophet_df['ds'].max()
    })
    
    return result

def calculate_runway(current_cash, burn_rate):
    """
    Calculate runway in months based on current cash and burn rate
    
    Parameters:
    -----------
    current_cash : float
        Current cash available
    burn_rate : float
        Monthly burn rate (negative cash flow)
        
    Returns:
    --------
    float
        Runway in months
    """
    if burn_rate <= 0:
        return float('inf')  # Infinite runway if burn rate is zero or positive
    
    return current_cash / burn_rate

def calculate_burn_rate(time_series_data, months=3):
    """
    Calculate average monthly burn rate based on recent months
    
    Parameters:
    -----------
    time_series_data : pandas.DataFrame
        DataFrame with 'MonthYearDate' and 'Total_Amount' columns
    months : int
        Number of recent months to consider
        
    Returns:
    --------
    float
        Average monthly burn rate
    """
    # Sort by date and get the last 'months' entries
    recent_data = time_series_data.sort_values('MonthYearDate', ascending=False).head(months)
    
    # Calculate average monthly expenditure
    avg_monthly_burn = recent_data['Total_Amount'].mean()
    
    return avg_monthly_burn
