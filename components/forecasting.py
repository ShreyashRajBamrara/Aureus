import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from prophet import Prophet
import plotly.graph_objects as go
from typing import Dict, Any
import logging
from datetime import datetime, timedelta
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinancialForecaster:
    def __init__(self):
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=True,
            interval_width=0.95
        )
        self.scaler = StandardScaler()
    
    def _aggregate_data(self, data, frequency='D'):
        """Aggregate data based on frequency (D=daily, W=weekly, M=monthly)"""
        df = data.copy()
        df['date'] = pd.to_datetime(df['date'])
        
        if frequency == 'D':
            return df.groupby('date')['amount'].sum().reset_index()
        elif frequency == 'W':
            return df.groupby(pd.Grouper(key='date', freq='W-MON'))['amount'].sum().reset_index()
        elif frequency == 'M':
            return df.groupby(pd.Grouper(key='date', freq='M'))['amount'].sum().reset_index()
    
    def generate_forecast(self, data, periods=30, frequency='D'):
        try:
            # Aggregate data based on frequency
            df = self._aggregate_data(data, frequency)
            df['ds'] = df['date']
            df['y'] = df['amount']
            
            # Fit the model
            self.model.fit(df[['ds', 'y']])
            
            # Make future dataframe
            future = self.model.make_future_dataframe(periods=periods, freq=frequency)
            forecast = self.model.predict(future)
            
            # Create a more user-friendly visualization
            fig = go.Figure()
            
            # Add actual data
            fig.add_trace(go.Scatter(
                x=df['ds'],
                y=df['y'],
                name='Actual Spending',
                line=dict(color='#1f77b4', width=2)
            ))
            
            # Add forecast
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat'],
                name='Forecasted Spending',
                line=dict(color='#2ca02c', width=2, dash='dash')
            ))
            
            # Add confidence interval
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat_upper'],
                fill=None,
                mode='lines',
                line_color='rgba(44, 160, 44, 0.2)',
                name='Upper Bound'
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat_lower'],
                fill='tonexty',
                mode='lines',
                line_color='rgba(44, 160, 44, 0.2)',
                name='Lower Bound'
            ))
            
            # Update layout for better readability
            fig.update_layout(
                title='Spending Forecast',
                xaxis_title='Date',
                yaxis_title='Amount (₹)',
                hovermode='x unified',
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                ),
                template='plotly_white'
            )
            
            # Add annotations for key points
            last_actual = df['y'].iloc[-1]
            last_forecast = forecast['yhat'].iloc[-1]
            
            fig.add_annotation(
                x=df['ds'].iloc[-1],
                y=last_actual,
                text=f"Last Actual: ₹{last_actual:,.2f}",
                showarrow=True,
                arrowhead=1
            )
            
            fig.add_annotation(
                x=forecast['ds'].iloc[-1],
                y=last_forecast,
                text=f"Forecast: ₹{last_forecast:,.2f}",
                showarrow=True,
                arrowhead=1
            )
            
            # Create a summary dataframe
            summary_df = pd.DataFrame({
                'Date': forecast['ds'].tail(periods),
                'Forecasted Amount': forecast['yhat'].tail(periods).round(2),
                'Minimum Expected': forecast['yhat_lower'].tail(periods).round(2),
                'Maximum Expected': forecast['yhat_upper'].tail(periods).round(2)
            })
            
            return {
                'plot': fig,
                'data': summary_df,
                'metrics': {
                    'last_actual': last_actual,
                    'last_forecast': last_forecast,
                    'change_percent': ((last_forecast - last_actual) / last_actual * 100).round(2)
                }
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def render_forecast(self, data, periods=30):
        """Render the forecast with explanations"""
        st.subheader("Spending Forecast")
        
        # Add frequency selection
        frequency = st.radio(
            "Select Time Period",
            ["Daily", "Weekly", "Monthly"],
            horizontal=True,
            help="Choose how you want to view the spending data"
        )
        
        # Map frequency selection to Prophet frequency
        freq_map = {
            "Daily": "D",
            "Weekly": "W",
            "Monthly": "M"
        }
        
        # Add explanation
        st.write("""
        This forecast shows:
        - **Actual Spending**: Your historical spending (blue line)
        - **Forecasted Spending**: Predicted future spending (green dashed line)
        - **Confidence Range**: The shaded area shows the possible range of future spending
        """)
        
        # Generate forecast
        forecast_results = self.generate_forecast(data, periods, freq_map[frequency])
        
        if 'error' in forecast_results:
            st.error(forecast_results['error'])
            return
        
        # Display the plot
        st.plotly_chart(forecast_results['plot'], use_container_width=True)
        
        # Display key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Last Actual Spending",
                f"₹{forecast_results['metrics']['last_actual']:,.2f}"
            )
        with col2:
            st.metric(
                "Forecasted Spending",
                f"₹{forecast_results['metrics']['last_forecast']:,.2f}"
            )
        with col3:
            st.metric(
                "Expected Change",
                f"{forecast_results['metrics']['change_percent']}%",
                delta=f"{forecast_results['metrics']['change_percent']}%"
            )
        
        # Display detailed forecast data
        st.subheader("Detailed Forecast")
        st.write("""
        Below is a detailed breakdown of the forecast. The confidence range shows the minimum and maximum 
        expected spending for each time period in the forecast.
        """)
        
        # Format the dataframe with Indian Rupee symbol
        formatted_df = forecast_results['data'].copy()
        for col in ['Forecasted Amount', 'Minimum Expected', 'Maximum Expected']:
            formatted_df[col] = formatted_df[col].apply(lambda x: f"₹{x:,.2f}")
        
        st.dataframe(formatted_df)
    
    def get_forecast_components(self, model):
        """Get forecast components (trend, seasonality)"""
        if model is None:
            return None
        
        # Get forecast components
        components = model.plot_components()
        return components
    
    def evaluate_forecast(self, actual, predicted):
        """Evaluate forecast accuracy"""
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        
        mae = mean_absolute_error(actual, predicted)
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        r2 = r2_score(actual, predicted)
        
        return {
            'MAE': mae,
            'RMSE': rmse,
            'R2': r2
        }