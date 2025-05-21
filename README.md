# Aureus - Financial Intelligence Platform

Aureus is a comprehensive financial intelligence platform designed for startups to track, analyze, and optimize their expenditures. The platform provides AI-powered insights, anomaly detection, and automated reporting capabilities.

## Features

- **Interactive Dashboard**: Visualize expenditure trends, category distributions, and key metrics
- **Department-wise Analysis**: Track and analyze spending patterns by department
- **Employee-level Insights**: Monitor individual employee expenses and patterns
- **AI Financial Advisor**: Get intelligent insights and recommendations
- **Anomaly Detection**: Automatically identify suspicious transactions and patterns
- **Automated Reporting**: Generate and send reports for flagged anomalies

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aureus.git
cd aureus
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
# Email Configuration
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-specific-password

# Current Cash Balance (in INR)
CURRENT_CASH=10000000

# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

Note: For Gmail, you'll need to use an App Password. Follow these steps:
1. Enable 2-Step Verification in your Google Account
2. Go to Security → App Passwords
3. Generate a new app password for "Mail"
4. Use this password in the EMAIL_PASSWORD variable

5. Run the application:
```bash
streamlit run app.py
```

## Data Structure

The application expects a CSV file named `aureus_expenditure_with_anomalies.csv` in the `data` directory with the following columns:
- Date
- Expense ID
- Amount
- Category
- Vendor
- Department
- Employee Name
- Notes

## Usage

1. **Dashboard**: View overall expenditure trends, forecasts, and key metrics
2. **Department View**: Analyze spending patterns by department
3. **Employee View**: Monitor individual employee expenses
4. **Advisor**: Interact with the AI financial advisor for insights
5. **Reporter**: Review and report detected anomalies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
