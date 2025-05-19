import streamlit as st
import pandas as pd
from models import anomaly_detector
from utils import report_generator

def show():
    st.header("🚨 Fraud & Anomaly Watch")
    df = pd.read_csv("data/startup_sample.csv")
    anomalies = anomaly_detector.detect_anomalies(df)

    if anomalies.empty:
        st.success("No suspicious transactions detected.")
    else:
        st.warning(f"{len(anomalies)} suspicious transactions found!")
        st.dataframe(anomalies)
        if st.button("Generate Recovery/Investor Email"):
            email = report_generator.generate_email(anomalies)
            st.code(email, language="text")
