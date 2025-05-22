import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    if df is None or df.empty:
        return pd.DataFrame()
    
    anomalies = []
    
    # Check for unusually high expenses (using Isolation Forest for robustness)
    # Ensure 'Amount' column exists before accessing it
    if 'Amount' in df.columns:
        X = df[['Amount']].values
        # Adjust contamination based on expected anomaly percentage, or use 'auto'
        clf = IsolationForest(contamination='auto', random_state=42)
        preds = clf.fit_predict(X)
        amount_anomalies = df[preds == -1].copy()
        if not amount_anomalies.empty:
            amount_anomalies['Anomaly_Type'] = 'Unusually High Amount'
            anomalies.append(amount_anomalies)
    else:
        print("Warning: 'Amount' column not found for anomaly detection.")
    
    # Check for future dates
    if 'Date' in df.columns:
        try:
            today = pd.Timestamp.now()
            future_date_anomalies = df[df['Date'] > today].copy()
            if not future_date_anomalies.empty:
                future_date_anomalies['Anomaly_Type'] = 'Future Date'
                anomalies.append(future_date_anomalies)
        except Exception as e:
             print(f"Error processing Date column for anomalies: {e}")
    else:
        print("Warning: 'Date' column not found for anomaly detection.")
    
    # Check for missing vendor info
    if 'Vendor' in df.columns:
        missing_vendor_anomalies = df[df['Vendor'] == 'Unknown Vendor'].copy()
        if not missing_vendor_anomalies.empty:
            missing_vendor_anomalies['Anomaly_Type'] = 'Missing Vendor Information'
            anomalies.append(missing_vendor_anomalies)
    else:
         print("Warning: 'Vendor' column not found for anomaly detection.")

    # Check for specific notes indicating anomalies
    if 'Notes' in df.columns:
        notes_anomalies = df[df['Notes'].str.contains('suspicious|anomaly|fraud|error', case=False, na=False)].copy()
        if not notes_anomalies.empty:
            notes_anomalies['Anomaly_Type'] = 'Flagged in Notes'
            anomalies.append(notes_anomalies)
    else:
        print("Warning: 'Notes' column not found for anomaly detection.")
    
    # Combine all anomalies
    if anomalies:
        # Use ignore_index=True to handle potential missing columns in individual anomaly dataframes
        combined_anomalies = pd.concat(anomalies, ignore_index=True).drop_duplicates(subset=df.columns.tolist())
        return combined_anomalies
    else:
        # Ensure the returned DataFrame has the Anomaly_Type column even if empty
        return pd.DataFrame(columns=df.columns.tolist() + ['Anomaly_Type']) 