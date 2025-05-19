import streamlit as st
from models import forecast_model, anomaly_detector
from utils import charts
import pandas as pd

# Minimal dashboard page

def show():
    st.header("📊 Startup Financial Dashboard")
    # Load data
    df = pd.read_csv("data/startup_sample.csv")

    # Forecast cash flow and runway
    forecast, runway, burn_rate = forecast_model.get_forecast_and_metrics(df)

    # Detect anomalies
    anomalies = anomaly_detector.detect_anomalies(df)

    # Show metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Burn Rate", f"${burn_rate:,.0f}")
    col2.metric("Runway (months)", f"{runway:.1f}")
    col3.metric("Anomalies", len(anomalies))

    # Show charts
    st.plotly_chart(charts.cashflow_chart(forecast), use_container_width=True)
    st.plotly_chart(charts.anomaly_chart(df, anomalies), use_container_width=True)

    # Show anomaly table
    if len(anomalies) > 0:
        st.subheader("Suspicious Transactions")
        st.dataframe(anomalies)
