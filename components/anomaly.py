import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self, contamination=0.1):
        """
        Initialize the anomaly detector.
        
        Args:
            contamination: The proportion of outliers in the data set
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
    
    def _prepare_features(self, data):
        """Prepare features for anomaly detection"""
        # Ensure date column is datetime
        if 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])
        elif 'Date' in data.columns:
            data['date'] = pd.to_datetime(data['Date'])
        else:
            raise ValueError("Data must contain a 'date' or 'Date' column")
        
        # Create features
        features = pd.DataFrame()
        
        # Amount-based features
        if 'amount' in data.columns:
            features['amount'] = data['amount']
            features['amount_abs'] = data['amount'].abs()
        elif 'Amount' in data.columns:
            features['amount'] = data['Amount']
            features['amount_abs'] = data['Amount'].abs()
        else:
            raise ValueError("Data must contain an 'amount' or 'Amount' column")
        
        # Time-based features
        features['day_of_week'] = data['date'].dt.dayofweek
        features['day_of_month'] = data['date'].dt.day
        features['month'] = data['date'].dt.month
        
        # Category encoding
        if 'transaction_type' in data.columns:
            features['is_expense'] = (data['transaction_type'] == 'expense').astype(int)
        else:
            features['is_expense'] = 0
        
        # Calculate rolling statistics
        data_sorted = data.sort_values('date')
        if 'amount' in data_sorted.columns:
            features['rolling_mean'] = data_sorted['amount'].rolling(window=7, min_periods=1).mean()
            features['rolling_std'] = data_sorted['amount'].rolling(window=7, min_periods=1).std()
        elif 'Amount' in data_sorted.columns:
            features['rolling_mean'] = data_sorted['Amount'].rolling(window=7, min_periods=1).mean()
            features['rolling_std'] = data_sorted['Amount'].rolling(window=7, min_periods=1).std()
        
        # Fill NaN values
        features = features.bfill().ffill()
        
        return features
    
    def detect(self, data):
        """Detect anomalies in the financial data"""
        try:
            # Prepare features
            features = self._prepare_features(data)
            
            # Scale features
            scaled_features = self.scaler.fit_transform(features)
            
            # Fit model and predict
            self.model.fit(scaled_features)
            predictions = self.model.predict(scaled_features)
            
            # Get anomaly scores
            scores = self.model.score_samples(scaled_features)
            
            # Create results DataFrame
            results = data.copy()
            results['anomaly_score'] = scores
            results['is_anomaly'] = predictions == -1
            
            # Get anomalies
            anomalies = results[results['is_anomaly']].copy()
            
            return anomalies.sort_values('anomaly_score', ascending=False)
                
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return pd.DataFrame()
    
    def display_anomalies(self, anomalies):
        if anomalies.empty:
            st.info("No anomalies detected.")
            return

        st.subheader("Detected Anomalies")
        
        # Choose the correct column for amount
        amount_col = 'amount' if 'amount' in anomalies.columns else 'Amount' if 'Amount' in anomalies.columns else None
        if amount_col is None:
            st.error("No 'amount' or 'Amount' column found in anomalies data.")
            return

        # Displaying the plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=anomalies['date'],
            y=anomalies[amount_col],
            mode='markers',
            marker=dict(color='red', size=10),
            text=[f"Employee: {name}" for name in anomalies['Employee Name']],
            hoverinfo='text+x+y'
        ))
        fig.update_layout(
            title='Anomalous Transactions',
            xaxis_title='Date',
            yaxis_title='Amount'
        )
        st.plotly_chart(fig)

        st.write(anomalies)

        st.info(f"Detected {len(anomalies)} anomalies. You can notify employees from the 'Email Center'.")
    
    def get_anomaly_statistics(self, anomalies):
        """Get statistics about detected anomalies"""
        if anomalies.empty:
            return None
        
        stats = {
            'total_anomalies': len(anomalies),
            'anomaly_percentage': (len(anomalies) / len(self.data)) * 100,
            'avg_anomaly_score': anomalies['anomaly_score'].mean(),
            'min_anomaly_score': anomalies['anomaly_score'].min(),
            'max_anomaly_score': anomalies['anomaly_score'].max(),
            'total_anomaly_amount': anomalies['amount'].sum(),
            'avg_anomaly_amount': anomalies['amount'].mean()
        }
        
        return stats
