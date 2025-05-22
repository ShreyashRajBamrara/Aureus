import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Dashboard:
    def __init__(self):
        self.data: Optional[pd.DataFrame] = None
    
    def load_data(self, df: pd.DataFrame):
        """Load data into the dashboard."""
        self.data = df
        if 'date' in df.columns:
            self.data['date'] = pd.to_datetime(df['date'])
    
    def _aggregate_data(self, frequency='D'):
        """Aggregate data based on frequency (D=daily, W=weekly, M=monthly)"""
        if frequency == 'D':
            return self.data.groupby('date')['amount'].sum().reset_index()
        elif frequency == 'W':
            return self.data.groupby(pd.Grouper(key='date', freq='W-MON'))['amount'].sum().reset_index()
        elif frequency == 'M':
            return self.data.groupby(pd.Grouper(key='date', freq='M'))['amount'].sum().reset_index()
    
    def show_summary(self):
        """Display summary statistics."""
        if self.data is None:
            st.warning("No data loaded")
            return
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_income = self.data[self.data['transaction_type'] == 'income']['amount'].sum()
            st.metric("Total Income", f"${total_income:,.2f}")
        
        with col2:
            total_expenses = self.data[self.data['transaction_type'] == 'expense']['amount'].sum()
            st.metric("Total Expenses", f"${total_expenses:,.2f}")
        
        with col3:
            net_income = total_income - total_expenses
            st.metric("Net Income", f"${net_income:,.2f}")
    
    def show_cash_flow(self):
        """Display cash flow chart."""
        if self.data is None:
            st.warning("No data loaded")
            return
        
        # Prepare data
        daily_data = self.data.groupby(['date', 'transaction_type'])['amount'].sum().reset_index()
        
        # Create figure
        fig = px.line(
            daily_data,
            x='date',
            y='amount',
            color='transaction_type',
            title='Daily Cash Flow',
            labels={'amount': 'Amount ($)', 'date': 'Date'},
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def show_category_breakdown(self):
        """Display expense category breakdown."""
        if self.data is None:
            st.warning("No data loaded")
            return
        
        # Filter expenses and group by category
        expenses = self.data[self.data['transaction_type'] == 'expense']
        category_data = expenses.groupby('category')['amount'].sum().reset_index()
        
        # Create pie chart
        fig = px.pie(
            category_data,
            values='amount',
            names='category',
            title='Expense Categories',
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def show_transaction_table(self):
        """Display transaction table with filtering options."""
        if self.data is None:
            st.warning("No data loaded")
            return
        
        # Add filters
        col1, col2 = st.columns(2)
        
        with col1:
            transaction_type = st.multiselect(
                "Transaction Type",
                options=self.data['transaction_type'].unique(),
                default=self.data['transaction_type'].unique()
            )
        
        with col2:
            category = st.multiselect(
                "Category",
                options=self.data['category'].unique(),
                default=self.data['category'].unique()
            )
        
        # Filter data
        filtered_data = self.data[
            (self.data['transaction_type'].isin(transaction_type)) &
            (self.data['category'].isin(category))
        ]
        
        # Display table
        st.dataframe(
            filtered_data.sort_values('date', ascending=False),
            use_container_width=True
        )
    
    def render(self):
        """Render the complete dashboard."""
        # st.title("Financial Dashboard")
        
        if self.data is None:
            st.warning("Please load data to view the dashboard")
            return
        
        # Time period selection
        frequency = st.radio(
            "Select Time Period",
            ["Daily", "Weekly", "Monthly"],
            horizontal=True,
            help="Choose how you want to view the spending data"
        )
        
        # Map frequency selection
        freq_map = {
            "Daily": "D",
            "Weekly": "W",
            "Monthly": "M"
        }
        
        # Get aggregated data
        agg_data = self._aggregate_data(freq_map[frequency])
        
        # Create two columns for metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_spent = self.data['amount'].sum()
            st.metric("Total Spent", f"₹{total_spent:,.2f}")
        
        with col2:
            avg_transaction = self.data['amount'].mean()
            st.metric("Average Transaction", f"₹{avg_transaction:,.2f}")
        
        with col3:
            most_frequent_vendor = self.data['vendor'].mode().iloc[0]
            st.metric("Most Frequent Vendor", most_frequent_vendor)
        
        with col4:
            highest_dept = self.data.groupby('department')['amount'].sum().idxmax()
            st.metric("Highest Spending Department", highest_dept)
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Spending over time
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=agg_data['date'],
                y=agg_data['amount'],
                mode='lines+markers',
                name='Spending',
                line=dict(color='#1f77b4', width=2)
            ))
            
            fig.update_layout(
                title='Spending Over Time',
                xaxis_title='Date',
                yaxis_title='Amount (₹)',
                hovermode='x unified',
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Department-wise spending
            dept_data = self.data.groupby('department')['amount'].sum().reset_index()
            dept_data = dept_data.sort_values('amount', ascending=False)
            
            fig = px.bar(
                dept_data,
                x='department',
                y='amount',
                title='Department-wise Spending',
                labels={'amount': 'Amount (₹)', 'department': 'Department'},
                color='amount',
                color_continuous_scale='Viridis'
            )
            
            fig.update_layout(
                template='plotly_white',
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Create two more columns for additional charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Payment method distribution
            payment_data = self.data.groupby('payment_method')['amount'].sum().reset_index()
            
            fig = px.pie(
                payment_data,
                values='amount',
                names='payment_method',
                title='Payment Method Distribution',
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(template='plotly_white')
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Category-wise spending
            category_data = self.data.groupby('category')['amount'].sum().reset_index()
            category_data = category_data.sort_values('amount', ascending=False).head(10)
            
            fig = px.bar(
                category_data,
                x='category',
                y='amount',
                title='Top 10 Spending Categories',
                labels={'amount': 'Amount (₹)', 'category': 'Category'},
                color='amount',
                color_continuous_scale='Viridis'
            )
            
            fig.update_layout(
                template='plotly_white',
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed data
        st.subheader("Detailed Spending Data")
        st.write("""
        Below is a detailed breakdown of all transactions. You can sort and filter this data to analyze specific aspects of your spending.
        """)
        
        # Format the dataframe with Indian Rupee symbol
        display_data = self.data.copy()
        display_data['amount'] = display_data['amount'].apply(lambda x: f"₹{x:,.2f}")
        display_data['date'] = display_data['date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(display_data)

def show_forecast(self):
    """Show forecasting options"""
    if self.data is None:
        st.warning("No data loaded")
        return
    
    periods = st.slider("Forecast Period (days)", 7, 90, 30)
    
    if st.button("Generate Forecast"):
        with st.spinner("Creating forecast..."):
            from components.forecasting import FinancialForecaster
            forecaster = FinancialForecaster()
            forecast = forecaster.generate_forecast(self.data, periods)
            
            if 'error' in forecast:
                st.error(forecast['error'])
            else:
                st.plotly_chart(forecast['plot'])
                st.dataframe(forecast['data'])