import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processing import load_and_process_data, get_time_series_data
from models.forecasting import forecast_expenditure, calculate_burn_rate, calculate_runway
from utils.anomaly_detection import detect_anomalies
import os

def dashboard_page():
    st.title("Financial Dashboard")
    
    df = load_and_process_data()
    
    if df is not None:
        st.success("Data loaded successfully!")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Company Overview", "Department View", "Employee View"])
        
        with tab1:
            st.subheader("Company Overview")
            
            # Summary metrics
            total_spent = df['Amount'].sum()
            avg_transaction = df['Amount'].mean()
            num_transactions = len(df)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Expenditure", f"₹{total_spent:,.2f}")
            col2.metric("Average Transaction", f"₹{avg_transaction:,.2f}")
            col3.metric("Number of Transactions", num_transactions)
            
            # Time series analysis
            st.subheader("Monthly Expenditure Trend")
            monthly_data = get_time_series_data(df)
            
            # Create interactive plot with Plotly
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=monthly_data['MonthYearDate'],
                y=monthly_data['Total_Amount'],
                mode='lines+markers',
                name='Actual'
            ))
            
            # Add forecasting
            forecast_data = forecast_expenditure(monthly_data)
            if not forecast_data.empty:
                fig.add_trace(go.Scatter(
                    x=forecast_data[forecast_data['Is_Prediction']]['Date'],
                    y=forecast_data[forecast_data['Is_Prediction']]['Predicted_Amount'],
                    mode='lines',
                    name='Forecast',
                    line=dict(dash='dash')
                ))
                fig.add_trace(go.Scatter(
                    x=forecast_data[forecast_data['Is_Prediction']]['Date'],
                    y=forecast_data[forecast_data['Is_Prediction']]['Upper_Bound'],
                    mode='lines',
                    name='Upper Bound',
                    line=dict(width=0),
                    showlegend=False
                ))
                fig.add_trace(go.Scatter(
                    x=forecast_data[forecast_data['Is_Prediction']]['Date'],
                    y=forecast_data[forecast_data['Is_Prediction']]['Lower_Bound'],
                    mode='lines',
                    name='Lower Bound',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(0,100,80,0.2)',
                    showlegend=False
                ))
            
            fig.update_layout(
                title="Monthly Expenditure Trend with Forecast",
                xaxis_title="Date",
                yaxis_title="Amount (₹)",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Category breakdown
            st.subheader("Expenditure by Category")
            category_data = df.groupby('Category')['Amount'].sum().reset_index()
            fig = px.pie(category_data, values='Amount', names='Category', title='Expenditure Distribution by Category')
            st.plotly_chart(fig, use_container_width=True)
            
            # Department breakdown - Overview
            st.subheader("Expenditure by Department (Overview)")
            dept_data_overview = df.groupby('Department')['Amount'].sum().reset_index()
            fig = px.bar(dept_data_overview, x='Department', y='Amount', title='Department-wise Expenditure Overview')
            st.plotly_chart(fig, use_container_width=True)
            
            # Anomaly detection - Overview
            st.subheader("Detected Anomalies (Overview)")
            anomalies_overview = detect_anomalies(df)
            if not anomalies_overview.empty:
                st.dataframe(anomalies_overview)
            else:
                st.info("No anomalies detected in the current dataset.")
            
            # Raw data
            with st.expander("View Raw Data"):
                st.dataframe(df)
                
        with tab2:
            st.subheader("Department-wise Analysis")
            
            # Department selector
            departments = ['All'] + sorted(df['Department'].unique().tolist())
            selected_dept = st.selectbox("Select Department", departments)
            
            # Filter data based on selection
            if selected_dept != 'All':
                dept_df = df[df['Department'] == selected_dept]
            else:
                dept_df = df
            
            # Department metrics
            total_dept_spent = dept_df['Amount'].sum()
            avg_dept_transaction = dept_df['Amount'].mean()
            num_dept_transactions = len(dept_df)
            
            col1, col2, col3 = st.columns(3)
            col1.metric(f"Total {selected_dept} Expenditure", f"₹{total_dept_spent:,.2f}")
            col2.metric("Average Transaction", f"₹{avg_dept_transaction:,.2f}")
            col3.metric("Number of Transactions", num_dept_transactions)
            
            # Department trend
            st.subheader("Expenditure Trend")
            dept_monthly = dept_df.groupby('MonthYear')['Amount'].sum().reset_index()
            st.line_chart(dept_monthly.set_index('MonthYear'))
            
            # Category breakdown for department
            st.subheader("Category Distribution")
            dept_category = dept_df.groupby('Category')['Amount'].sum().reset_index()
            if not dept_category.empty:
                fig = px.pie(dept_category, values='Amount', names='Category')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No category data for this department.")
            
            # Top vendors
            st.subheader("Top Vendors")
            top_vendors = dept_df.groupby('Vendor')['Amount'].sum().sort_values(ascending=False).head(10)
            if not top_vendors.empty:
                st.bar_chart(top_vendors)
            else:
                st.info("No vendor data for this department.")

        with tab3:
            st.subheader("Employee-wise Analysis")
            
            # Employee selector
            employees = ['All'] + sorted(df['Employee Name'].unique().tolist())
            selected_employee = st.selectbox("Select Employee", employees)
            
            # Filter data based on selection
            if selected_employee != 'All':
                emp_df = df[df['Employee Name'] == selected_employee]
            else:
                emp_df = df
            
            # Employee metrics
            total_emp_spent = emp_df['Amount'].sum()
            avg_emp_transaction = emp_df['Amount'].mean()
            num_emp_transactions = len(emp_df)
            
            col1, col2, col3 = st.columns(3)
            col1.metric(f"Total Expenses ({selected_employee})", f"₹{total_emp_spent:,.2f}")
            col2.metric("Average Transaction", f"₹{avg_emp_transaction:,.2f}")
            col3.metric("Number of Transactions", num_emp_transactions)
            
            # Employee trend
            st.subheader("Expense Trend")
            emp_monthly = emp_df.groupby('MonthYear')['Amount'].sum().reset_index()
            st.line_chart(emp_monthly.set_index('MonthYear'))
            
            # Category breakdown for employee
            st.subheader("Category Distribution")
            emp_category = emp_df.groupby('Category')['Amount'].sum().reset_index()
            if not emp_category.empty:
                fig = px.pie(emp_category, values='Amount', names='Category')
                st.plotly_chart(fig, use_container_width=True)
            else:
                 st.info("No category data for this employee.")
            
            # Recent transactions
            st.subheader("Recent Transactions")
            if not emp_df.empty:
                st.dataframe(emp_df.sort_values('Date', ascending=False).head(10))
            else:
                st.info("No recent transactions for this employee.") 