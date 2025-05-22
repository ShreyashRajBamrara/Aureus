import pandas as pd
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    def __init__(self):
        self.required_columns = ['date', 'amount', 'category', 'transaction_type']
    
    def preprocess_aureus_data(self, df):
        """
        Preprocess Aureus expenditure data into the required format.
        
        Args:
            df: DataFrame containing Aureus expenditure data
            
        Returns:
            DataFrame in the required format
        """
        try:
            # Create a new DataFrame with required columns
            processed_df = pd.DataFrame()
            
            # Map date column
            processed_df['date'] = pd.to_datetime(df['Date'])
            
            # Map amount column
            processed_df['amount'] = df['Amount']
            
            # Map category column
            processed_df['category'] = df['Category']
            
            # Set transaction_type to 'expense' as all records are expenses
            processed_df['transaction_type'] = 'expense'
            
            # Add additional useful columns
            processed_df['vendor'] = df['Vendor']
            processed_df['payment_method'] = df['Payment Method']
            processed_df['department'] = df['Department']
            processed_df['status'] = df['Status']
            processed_df['employee'] = df['Employee Name']
            
            # Sort by date
            processed_df = processed_df.sort_values('date')
            
            return processed_df
            
        except Exception as e:
            logger.error(f"Error preprocessing data: {str(e)}")
            raise
    
    def validate_processed_data(self, df):
        """
        Validate the processed data has all required columns and correct data types.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check required columns
            missing_columns = [col for col in self.required_columns if col not in df.columns]
            if missing_columns:
                return False, f"Missing required columns: {', '.join(missing_columns)}"
            
            # Validate date column
            if not pd.api.types.is_datetime64_any_dtype(df['date']):
                return False, "Date column must be datetime type"
            
            # Validate amount column
            if not pd.api.types.is_numeric_dtype(df['amount']):
                return False, "Amount column must be numeric type"
            
            # Validate transaction_type column
            valid_types = ['income', 'expense']
            if not df['transaction_type'].isin(valid_types).all():
                return False, f"Transaction type must be one of: {', '.join(valid_types)}"
            
            return True, "Data validation successful"
            
        except Exception as e:
            return False, f"Error validating data: {str(e)}"
    
    def detect_anomalies(self, df):
        """
        Detect potential anomalies in the data.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            DataFrame containing potential anomalies
        """
        try:
            anomalies = pd.DataFrame()
            
            # Check for missing vendors
            missing_vendor = df[df['vendor'].isna()]
            if not missing_vendor.empty:
                missing_vendor['anomaly_type'] = 'Missing Vendor'
                anomalies = pd.concat([anomalies, missing_vendor])
            
            # Check for suspiciously large amounts (more than 3 standard deviations)
            amount_mean = df['amount'].mean()
            amount_std = df['amount'].std()
            large_amounts = df[df['amount'] > (amount_mean + 3 * amount_std)]
            if not large_amounts.empty:
                large_amounts['anomaly_type'] = 'Suspiciously Large Amount'
                anomalies = pd.concat([anomalies, large_amounts])
            
            # Check for future dates
            future_dates = df[df['date'] > datetime.now()]
            if not future_dates.empty:
                future_dates['anomaly_type'] = 'Future Date'
                anomalies = pd.concat([anomalies, future_dates])
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return pd.DataFrame() 