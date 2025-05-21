import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_expenditure_trend(time_series_data, forecast_data=None):
    """
    Create a time series chart of expenditure trends with optional forecast
    
    Parameters:
    -----------
    time_series_data : pandas.DataFrame
        DataFrame with 'MonthYearDate' and 'Total_Amount' columns
    forecast_data : pandas.DataFrame, optional
        DataFrame with forecasted values
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object
    """
    fig = go.Figure()
    
    # Add historical data
    fig.add_trace(go.Scatter(
        x=time_series_data['MonthYearDate'],
        y=time_series_data['Total_Amount'],
        mode='lines+markers',
        name='Historical Expenditure',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    # Add forecast if provided
    if forecast_data is not None:
        # Only include forecast part
        forecast_only = forecast_data[forecast_data['Is_Prediction']]
        
        # Add prediction line
        fig.add_trace(go.Scatter(
            x=forecast_only['Date'],
            y=forecast_only['Predicted_Amount'],
            mode='lines',
            name='Forecasted Expenditure',
            line=dict(color='#ff7f0e', width=3, dash='dash')
        ))
        
        # Add confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_only['Date'].tolist() + forecast_only['Date'].tolist()[::-1],
            y=forecast_only['Upper_Bound'].tolist() + forecast_only['Lower_Bound'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255, 127, 14, 0.2)',
            line=dict(color='rgba(255, 127, 14, 0)'),
            name='Confidence Interval'
        ))
    
    # Update layout
    fig.update_layout(
        title='Monthly Expenditure Trend',
        xaxis_title='Month',
        yaxis_title='Total Expenditure (INR)',
        hovermode='x unified',
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    return fig

def create_category_breakdown(df):
    """
    Create a pie chart showing expenditure breakdown by category
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataframe with expenditure data
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object
    """
    category_data = df.groupby('Category').agg(
        Total_Amount=('Amount', 'sum')
    ).reset_index()
    
    fig = px.pie(
        category_data, 
        values='Total_Amount', 
        names='Category',
        title='Expenditure by Category',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(template='plotly_white')
    
    return fig

def create_payment_method_chart(df):
    """
    Create a bar chart showing expenditure by payment method
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataframe with expenditure data
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object
    """
    payment_data = df.groupby('Payment Method').agg(
        Total_Amount=('Amount', 'sum')
    ).reset_index().sort_values('Total_Amount', ascending=False)
    
    fig = px.bar(
        payment_data,
        x='Payment Method',
        y='Total_Amount',
        title='Expenditure by Payment Method',
        color='Payment Method',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    fig.update_layout(template='plotly_white')
    
    return fig

def create_vendor_distribution(df, top_n=10):
    """
    Create a bar chart showing expenditure by top vendors
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataframe with expenditure data
    top_n : int
        Number of top vendors to include
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object
    """
    vendor_data = df.groupby('Vendor').agg(
        Total_Amount=('Amount', 'sum')
    ).reset_index().sort_values('Total_Amount', ascending=False).head(top_n)
    
    fig = px.bar(
        vendor_data,
        x='Total_Amount',
        y='Vendor',
        title=f'Top {top_n} Vendors by Expenditure',
        color='Total_Amount',
        color_continuous_scale='Viridis',
        orientation='h'
    )
    
    fig.update_layout(template='plotly_white', yaxis={'categoryorder':'total ascending'})
    
    return fig

def create_department_comparison(df):
    """
    Create a bar chart comparing expenditure across departments
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataframe with expenditure data
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object
    """
    dept_data = df.groupby('Department').agg(
        Total_Amount=('Amount', 'sum')
    ).reset_index().sort_values('Total_Amount', ascending=False)
    
    fig = px.bar(
        dept_data,
        x='Department',
        y='Total_Amount',
        title='Expenditure by Department',
        color='Department',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    fig.update_layout(template='plotly_white')
    
    return fig

def create_department_trend(df):
    """
    Create a line chart showing expenditure trend by department over time
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataframe with expenditure data
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object
    """
    dept_time_data = df.groupby(['MonthYearDate', 'Department']).agg(
        Total_Amount=('Amount', 'sum')
    ).reset_index()
    
    fig = px.line(
        dept_time_data,
        x='MonthYearDate',
        y='Total_Amount',
        color='Department',
        title='Department Expenditure Trend',
        markers=True
    )
    
    fig.update_layout(
        template='plotly_white',
        xaxis_title='Month',
        yaxis_title='Total Expenditure (INR)',
        hovermode='x unified'
    )
    
    return fig

def create_employee_spending_chart(df, top_n=10):
    """
    Create a bar chart showing expenditure by top employees
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataframe with expenditure data
    top_n : int
        Number of top employees to include
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object
    """
    employee_data = df.groupby('Employee Name').agg(
        Total_Amount=('Amount', 'sum')
    ).reset_index().sort_values('Total_Amount', ascending=False).head(top_n)
    
    fig = px.bar(
        employee_data,
        x='Total_Amount',
        y='Employee Name',
        title=f'Top {top_n} Employees by Expenditure',
        color='Total_Amount',
        color_continuous_scale='Viridis',
        orientation='h'
    )
    
    fig.update_layout(template='plotly_white', yaxis={'categoryorder':'total ascending'})
    
    return fig

def create_employee_category_chart(df, employee_name):
    """
    Create a pie chart showing category breakdown for a specific employee
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataframe with expenditure data
    employee_name : str
        Name of the employee to analyze
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object
    """
    employee_df = df[df['Employee Name'] == employee_name]
    category_data = employee_df.groupby('Category').agg(
        Total_Amount=('Amount', 'sum')
    ).reset_index()
    
    fig = px.pie(
        category_data, 
        values='Total_Amount', 
        names='Category',
        title=f'Expenditure Categories for {employee_name}',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(template='plotly_white')
    
    return fig

def create_anomaly_chart(df, anomalies):
    """
    Create a scatter plot highlighting anomalous transactions
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Processed dataframe with expenditure data
    anomalies : pandas.DataFrame
        Dataframe containing anomalous entries
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object
    """
    fig = px.scatter(
        df,
        x='Date',
        y='Amount',
        color_discrete_sequence=['#1f77b4'],
        opacity=0.7,
        title='Expenditure with Anomaly Detection'
    )
    
    # Add anomalies if they exist
    if not anomalies.empty:
        fig.add_trace(go.Scatter(
            x=anomalies['Date'],
            y=anomalies['Amount'],
            mode='markers',
            marker=dict(color='red', size=12, symbol='x'),
            name='Anomalies',
            text=anomalies['Anomaly_Type'],
            hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Amount: %{y}<extra></extra>'
        ))
    
    fig.update_layout(
        template='plotly_white',
        xaxis_title='Date',
        yaxis_title='Amount (INR)',
        hovermode='closest'
    )
    
    return fig
