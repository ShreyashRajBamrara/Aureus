import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging

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
        if 'date' not in data.columns:
            raise ValueError("Data must contain a 'date' column")
        
        data['date'] = pd.to_datetime(data['date'])
        
        # Create features
        features = pd.DataFrame()
        
        # Amount-based features
        features['amount'] = data['amount']
        features['amount_abs'] = data['amount'].abs()
        
        # Time-based features
        features['day_of_week'] = data['date'].dt.dayofweek
        features['day_of_month'] = data['date'].dt.day
        features['month'] = data['date'].dt.month
        
        # Category encoding
        features['is_expense'] = (data['transaction_type'] == 'expense').astype(int)
        
        # Calculate rolling statistics
        data_sorted = data.sort_values('date')
        features['rolling_mean'] = data_sorted['amount'].rolling(window=7, min_periods=1).mean()
        features['rolling_std'] = data_sorted['amount'].rolling(window=7, min_periods=1).std()
        
        # Fill NaN values
        features = features.fillna(method='bfill').fillna(method='ffill')
        
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
            
            if not anomalies.empty:
                # Create visualization
                fig = go.Figure()
                
                # Add normal points
                normal = results[~results['is_anomaly']]
                fig.add_trace(go.Scatter(
                    x=normal['date'],
                    y=normal['amount'],
                    mode='markers',
                    name='Normal',
                    marker=dict(color='blue', size=8)
                ))
                
                # Add anomalies
                fig.add_trace(go.Scatter(
                    x=anomalies['date'],
                    y=anomalies['amount'],
                    mode='markers',
                    name='Anomaly',
                    marker=dict(color='red', size=12, symbol='star')
                ))
                
                # Update layout
                fig.update_layout(
                    title='Transaction Anomalies',
                    xaxis_title='Date',
                    yaxis_title='Amount ($)',
                    template='plotly_white',
                    hovermode='x unified'
                )
                
                # Add anomaly details
                anomalies['date'] = anomalies['date'].dt.strftime('%Y-%m-%d')
                anomalies = anomalies.sort_values('anomaly_score')
                
                return anomalies
            else:
                return pd.DataFrame()  # Return empty DataFrame if no anomalies found
                
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return pd.DataFrame()  # Return empty DataFrame on error
    
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
