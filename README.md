# Aureus - Company Expenditure Analysis Dashboard

A comprehensive Streamlit application for analyzing and visualizing company expenditure data with AI-powered insights and anomaly detection.

## Features

### 1. Dashboard
- **Company View**: Overall expenditure analysis and trends
- **Department View**: Department-wise expenditure breakdown
- **Employee View**: Individual employee expenditure patterns

### 2. AI Advisor
- Smart insights and recommendations
- Predictive analytics
- Cost optimization suggestions

### 3. Analysis and Report
- Detailed expenditure analysis
- Anomaly detection
- Custom report generation

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
- Copy `.env.example` to `.env`
- Update the variables in `.env` with your configuration

5. Run the application:
```bash
streamlit run Home.py
```

## Project Structure

```
aureus/
├── Home.py                 # Main application entry point
├── pages/                  # Streamlit pages
│   ├── company_view.py     # Company-level dashboard
│   ├── department_view.py  # Department-level dashboard
│   ├── employee_view.py    # Employee-level dashboard
│   ├── advisor_page.py     # AI advisor interface
│   └── reporter_page.py    # Analysis and reporting
├── utils/                  # Utility functions
├── config/                 # Configuration files
├── requirements.txt        # Project dependencies
└── .env                    # Environment variables
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/aureus](https://github.com/yourusername/aureus)
