# Getting Started with Aureus Financial Analysis System

## Prerequisites

Before installing Aureus, ensure you have:

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **pip (Python package manager)**
   ```bash
   pip --version
   ```

3. **Git** (for cloning the repository)
   ```bash
   git --version
   ```

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/ShreyashRajBamrara/AureusTwo.git
cd AureusTwo
```

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv finance_app_env
finance_app_env\Scripts\activate

# Linux/Mac
python -m venv finance_app_env
source finance_app_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
# Email Configuration (Optional)
ALERT_RECIPIENT=your.email@example.com
REPORT_RECIPIENT=your.email@example.com

# Application Settings
DEBUG=False
```

## Running the Application

### 1. Start the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### 2. First-Time Setup

1. **Data Upload**
   - Navigate to the "Data Upload" page
   - Choose between sample data or upload your own CSV
   - Ensure your CSV follows the required format:

   ```csv
   date,amount,vendor,category,department,payment_method,status
   2024-01-01,1000.00,Vendor A,Office Supplies,IT,Credit Card,Completed
   ```

2. **Required CSV Columns**:
   - `date`: Transaction date (YYYY-MM-DD)
   - `amount`: Transaction amount
   - `vendor`: Vendor name
   - `category`: Transaction category
   - `department`: Department name
   - `payment_method`: Payment method used
   - `status`: Transaction status

## Using the Application

### 1. Dashboard
- View overall financial metrics
- Switch between daily/weekly/monthly views
- Explore interactive visualizations

### 2. Forecasting
- Select forecast period (7-90 days)
- View predicted trends
- Analyze confidence intervals

### 3. Anomaly Detection
- Adjust sensitivity using the slider
- Review detected anomalies
- Export anomaly reports

### 4. AI Advisor
- Ask financial questions
- Get spending insights
- Learn financial terms

### 5. Reports
- Generate periodic reports
- Export data
- Email reports

## Common Issues and Solutions

### 1. Installation Issues
```bash
# If you get SSL errors
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# If you get permission errors
pip install --user -r requirements.txt
```

### 2. Running Issues
```bash
# If port 8501 is in use
streamlit run app.py --server.port 8502

# If you get memory errors
streamlit run app.py --server.maxUploadSize 200
```

### 3. Data Issues
- Ensure CSV is UTF-8 encoded
- Check date format (YYYY-MM-DD)
- Verify all required columns are present

## Development Setup

### 1. Install Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### 2. Run Tests
```bash
pytest tests/
```

### 3. Code Style
```bash
# Install pre-commit hooks
pre-commit install

# Run linting
flake8 .
```

## Updating the Application

### 1. Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### 2. Pull Latest Changes
```bash
git pull origin main
```

## Backup and Data Management

### 1. Backup Data
```bash
# Backup processed data
cp -r data/processed backup/processed_$(date +%Y%m%d)

# Backup reports
cp -r data/reports backup/reports_$(date +%Y%m%d)
```

### 2. Restore Data
```bash
# Restore from backup
cp -r backup/processed_20240101/* data/processed/
```

## Security Considerations

1. **Data Protection**
   - Keep your `.env` file secure
   - Don't commit sensitive data
   - Regular backups

2. **Access Control**
   - Use strong passwords
   - Regular updates
   - Monitor access logs

## Getting Help

1. **Documentation**
   - Read `NOTES.md` for technical details
   - Check inline code comments
   - Review function docstrings

2. **Support**
   - Open an issue on GitHub
   - Check existing issues
   - Join the community forum

## Next Steps

1. **Explore Features**
   - Try different visualizations
   - Test forecasting
   - Experiment with anomaly detection

2. **Customize**
   - Modify dashboard layout
   - Add custom reports
   - Integrate with other tools

3. **Contribute**
   - Report bugs
   - Suggest features
   - Submit pull requests 