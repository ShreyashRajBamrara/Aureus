import pandas as pd
from prophet import Prophet

# Forecast cash flow and calculate runway and burn rate
def get_forecast_and_metrics(df):
    # Assume df has columns: date, amount
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    # Aggregate by month
    monthly = df.groupby(pd.Grouper(key='date', freq='M')).sum().reset_index()
    monthly.rename(columns={'date': 'ds', 'amount': 'y'}, inplace=True)

    # Prophet forecast
    m = Prophet()
    m.fit(monthly)
    future = m.make_future_dataframe(periods=3, freq='M')
    forecast = m.predict(future)

    # Burn rate: average negative monthly cash flow (last 3 months)
    last3 = monthly.tail(3)['y']
    burn_rate = -last3[last3 < 0].mean() if (last3 < 0).any() else 0

    # Runway: current cash / burn rate
    current_cash = df['amount'].sum()
    runway = current_cash / burn_rate if burn_rate > 0 else 99

    return forecast, runway, burn_rate
