import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    # Assume df has columns: date, amount
    X = df[['amount']].values
    clf = IsolationForest(contamination=0.1, random_state=42)
    preds = clf.fit_predict(X)
    anomalies = df[preds == -1].copy()
    return anomalies
