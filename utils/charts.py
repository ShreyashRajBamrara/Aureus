import plotly.graph_objs as go
import pandas as pd

def cashflow_chart(forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
    fig.update_layout(title='Cash Flow Forecast', xaxis_title='Date', yaxis_title='Cash Flow')
    return fig

def anomaly_chart(df, anomalies):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['amount'], mode='lines+markers', name='Transactions'))
    if not anomalies.empty:
        fig.add_trace(go.Scatter(x=anomalies['date'], y=anomalies['amount'], mode='markers', name='Anomalies', marker=dict(color='red', size=10)))
    fig.update_layout(title='Anomaly Detection', xaxis_title='Date', yaxis_title='Amount')
    return fig
