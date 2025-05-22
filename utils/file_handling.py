import pandas as pd
import os
from pathlib import Path
import json
from datetime import datetime
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self):
        # Create necessary directories
        self.data_dir = Path("data")
        self.processed_dir = self.data_dir / "processed"
        self.exports_dir = self.data_dir / "exports"
        self.reports_dir = self.data_dir / "reports"
        
        for directory in [self.data_dir, self.processed_dir, self.exports_dir, self.reports_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def validate_csv_structure(self, df, required_columns):
        """Validate CSV structure and data types"""
        try:
            # Check required columns
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return False, f"Missing required columns: {', '.join(missing_columns)}"
            
            # Validate date column
            if 'date' in df.columns:
                try:
                    pd.to_datetime(df['date'])
                except:
                    return False, "Invalid date format in 'date' column"
            
            # Validate amount column
            if 'amount' in df.columns:
                try:
                    df['amount'] = pd.to_numeric(df['amount'])
                except:
                    return False, "Invalid numeric format in 'amount' column"
            
            # Validate transaction_type column
            if 'transaction_type' in df.columns:
                valid_types = ['income', 'expense']
                invalid_types = df[~df['transaction_type'].isin(valid_types)]['transaction_type'].unique()
                if len(invalid_types) > 0:
                    return False, f"Invalid transaction types found: {', '.join(invalid_types)}"
            
            return True, "CSV structure is valid"
            
        except Exception as e:
            return False, f"Error validating CSV: {str(e)}"
    
    def save_processed_data(self, df, filename):
        """Save processed data to file"""
        try:
            filepath = self.processed_dir / filename
            df.to_csv(filepath, index=False)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def load_processed_data(self, filename):
        """Load processed data from file"""
        try:
            filepath = self.processed_dir / filename
            if not filepath.exists():
                return None, "File not found"
            
            df = pd.read_csv(filepath)
            return df, None
        except Exception as e:
            return None, str(e)
    
    def export_to_excel(self, df, filename, sheet_name="Financial Data"):
        """Export data to Excel file"""
        try:
            filepath = self.exports_dir / filename
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def export_to_json(self, data, filename):
        """Export data to JSON file"""
        try:
            filepath = self.exports_dir / filename
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def save_report(self, report_data, report_type, format="txt"):
        """Save financial report"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{report_type}_{timestamp}.{format}"
            filepath = self.reports_dir / filename
            
            if format == "txt":
                with open(filepath, 'w') as f:
                    f.write(report_data)
            elif format == "json":
                with open(filepath, 'w') as f:
                    json.dump(report_data, f, indent=4)
            else:
                return False, f"Unsupported format: {format}"
            
            return True, None
        except Exception as e:
            return False, str(e)
    
    def get_latest_report(self, report_type):
        """Get the latest report of a specific type"""
        try:
            reports = list(self.reports_dir.glob(f"{report_type}_*.txt"))
            if not reports:
                return None, "No reports found"
            
            latest_report = max(reports, key=os.path.getctime)
            with open(latest_report, 'r') as f:
                content = f.read()
            return content, None
        except Exception as e:
            return None, str(e)
    
    def cleanup_old_files(self, days=30):
        """Clean up files older than specified days"""
        try:
            cutoff_date = datetime.now() - pd.Timedelta(days=days)
            
            for directory in [self.processed_dir, self.exports_dir, self.reports_dir]:
                for file in directory.glob("*"):
                    if datetime.fromtimestamp(file.stat().st_mtime) < cutoff_date:
                        file.unlink()
            
            return True, None
        except Exception as e:
            return False, str(e)
    
    def read_csv(self, file_path: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Read a CSV file and return the DataFrame and any error message.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Tuple of (DataFrame, error_message)
        """
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Successfully read CSV file: {file_path}")
            return df, None
        except Exception as e:
            error_msg = f"Error reading CSV file: {str(e)}"
            logger.error(error_msg)
            return None, error_msg
    
    def get_processed_files(self) -> list:
        """Get list of processed files."""
        return [f.name for f in self.processed_dir.glob("*.csv")]
    
    def delete_processed_file(self, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Delete a processed file.
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            file_path = self.processed_dir / filename
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Successfully deleted file: {filename}")
                return True, None
            return False, f"File not found: {filename}"
        except Exception as e:
            error_msg = f"Error deleting file: {str(e)}"
            logger.error(error_msg)
            return False, error_msg 