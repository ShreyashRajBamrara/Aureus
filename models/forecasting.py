import pandas as pd
from prophet import Prophet
import os

def forecast_expenditure(time_series_data, periods=6):
    if time_series_data.empty:
        return pd.DataFrame()
        
    # Prepare data for Prophet
    prophet_df = time_series_data[['MonthYearDate', 'Total_Amount']].copy()
    prophet_df.columns = ['ds', 'y']
    
    # Initialize and fit the model
    model = Prophet(yearly_seasonality=True,
                   weekly_seasonality=True,
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

def calculate_burn_rate(time_series_data, months=3):
    if time_series_data.empty:
        return 0
        
    # Sort by date and get the last 'months' entries
    recent_data = time_series_data.sort_values('MonthYearDate', ascending=False).head(months)
    
    # Calculate average monthly expenditure
    avg_monthly_burn = recent_data['Total_Amount'].mean()
    
    return avg_monthly_burn

def calculate_runway(current_cash, burn_rate):
    if burn_rate <= 0:
        return float('inf')  # Infinite runway if burn rate is zero or positive
    
    return current_cash / burn_rate 