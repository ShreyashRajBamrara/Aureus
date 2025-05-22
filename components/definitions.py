import streamlit as st

class FinancialDefinitions:
    def __init__(self):
        self.terms = {
            "Forecasting Terms": {
                "Forecast": "A prediction of future financial values based on historical data and trends.",
                "Lower Bound": "The minimum expected value in a forecast range, showing the lowest possible outcome.",
                "Upper Bound": "The maximum expected value in a forecast range, showing the highest possible outcome.",
                "Confidence Interval": "A range of values that likely contains the true value, showing the reliability of the forecast.",
                "Trend": "The general direction in which financial data is moving over time.",
                "Seasonality": "Regular patterns that repeat at specific intervals (daily, weekly, monthly, yearly)."
            },
            "Financial Analysis Terms": {
                "Expenditure": "Money spent on goods and services.",
                "Revenue": "Income generated from business activities.",
                "Profit": "Revenue minus expenses.",
                "Cash Flow": "The movement of money in and out of a business.",
                "Budget": "A financial plan for a defined period.",
                "Expense": "Cost incurred in the process of generating revenue."
            },
            "Graph Terms": {
                "Line Chart": "A graph showing data points connected by lines, useful for showing trends over time.",
                "Bar Chart": "A graph using rectangular bars to show comparisons between categories.",
                "Scatter Plot": "A graph showing the relationship between two variables using dots.",
                "Histogram": "A graph showing the distribution of data using bars.",
                "Pie Chart": "A circular graph divided into slices to show proportions."
            },
            "Statistical Terms": {
                "Mean": "The average value of a set of numbers.",
                "Median": "The middle value in a sorted set of numbers.",
                "Mode": "The most frequently occurring value in a set of numbers.",
                "Standard Deviation": "A measure of how spread out numbers are from their average.",
                "Variance": "A measure of how far a set of numbers are spread out from their average."
            }
        }

    def render(self):
        st.title("Financial Terms and Definitions")
        st.write("""
        This page provides clear explanations of financial terms and concepts used throughout the application.
        Use this as a reference to better understand the financial data and visualizations.
        """)

        # Create tabs for different categories
        tabs = st.tabs(list(self.terms.keys()))
        
        for tab, category in zip(tabs, self.terms.keys()):
            with tab:
                st.subheader(category)
                for term, definition in self.terms[category].items():
                    with st.expander(term):
                        st.write(definition)
                        # Add example if available
                        if term in ["Forecast", "Lower Bound", "Upper Bound"]:
                            st.image("assets/forecast_example.png", caption="Example of forecast visualization", use_column_width=True) 