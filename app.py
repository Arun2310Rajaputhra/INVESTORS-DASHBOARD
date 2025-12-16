import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
import time

# Page configuration
st.set_page_config(
    page_title="Investment Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations and transparent effects
st.markdown("""
<style>
    /* Background image with dark overlay for better readability */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                    url('https://raw.githubusercontent.com/Arun2310Rajaputhra/INVESTORS-DASHBOARD/main/background_website.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        min-height: 100vh;
    }
    
    /* Make content containers transparent */
    .main .block-container {
        background-color: transparent;
        padding-top: 1rem;
        padding-bottom: 3rem;
    }
    
    /* Transparent sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 20, 40, 0.85) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar .sidebar-content {
        background-color: transparent;
    }
    
    /* Glass-morphism effect for main header */
    .main-header {
        font-size: 1.6rem;
        color: #FFFFFF;
        margin-bottom: 1rem;
        animation: fadeIn 1s;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Glass-morphism metric cards */
    .metric-card {
        background-color: rgba(0, 31, 63, 0.85);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s, box-shadow 0.3s;
        animation: slideUp 0.5s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        background-color: rgba(0, 31, 63, 0.95);
        border-color: rgba(30, 136, 229, 0.3);
    }
    
    /* Profit colors with glow effect */
    .profit-positive {
        color: #00ff88;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
        animation: pulse 2s infinite;
    }
    
    .profit-negative {
        color: #ff5252;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 82, 82, 0.3);
    }
    
    /* Transparent pending alerts */
    .pending-alert {
        background-color: rgba(255, 243, 205, 0.9);
        border: 1px solid rgba(255, 238, 186, 0.8);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        animation: fadeIn 0.5s;
        backdrop-filter: blur(5px);
    }
    
    /* Success message with transparency */
    .success-message {
        animation: slideIn 0.5s, fadeOut 2s 3s forwards;
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background-color: rgba(212, 237, 218, 0.9);
        border-radius: 8px;
        backdrop-filter: blur(5px);
    }
    
    /* Transparent plotly charts container */
    .js-plotly-plot .plotly {
        background-color: transparent !important;
    }
    
    .plotly-container {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
    }
    
    /* Transparent dataframes */
    .dataframe {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Transparent headers and titles */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    .stSubheader {
        color: white !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
    }
    
    /* Transparent buttons */
    .stButton > button {
        background-color: rgba(30, 136, 229, 0.9);
        color: white;
        border: none;
        transition: all 0.3s;
        backdrop-filter: blur(5px);
    }
    
    .stButton > button:hover {
        background-color: rgba(13, 71, 161, 0.9);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
    }
    
    /* Transparent select boxes and inputs */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(5px);
    }
    
    .stDateInput > div > div {
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(5px);
    }
    
    /* Footer for copyright */
    .copyright-footer {
        position: fixed;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 12px;
        color: rgba(255, 255, 255, 0.6);
        padding: 5px;
        background-color: rgba(0, 0, 0, 0.3);
        z-index: 1000;
        backdrop-filter: blur(5px);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); text-shadow: 0 0 10px rgba(0, 255, 136, 0.3); }
        50% { transform: scale(1.05); text-shadow: 0 0 15px rgba(0, 255, 136, 0.5); }
        100% { transform: scale(1); text-shadow: 0 0 10px rgba(0, 255, 136, 0.3); }
    }
    
    /* Title styling */
    .dashboard-title {
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 1s;
    }
    
    .dashboard-title h6 {
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-weight: 800;
        letter-spacing: 1px;
    }
    
    .dashboard-title p {
        font-size: 1rem !important;
        color: #a0d2ff !important;
        letter-spacing: 2px;
        font-weight: 300;
        margin-top: -0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Add copyright footer
st.markdown("""
<div class="copyright-footer">
    © Copyright 2025. All rights reserved with Rajaputra Arun Kumar, Hyderabad
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_excel_data():
    """Load all sheets from the Excel file"""
    # Show loading animation
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        with st.spinner('📊 Loading latest investment data...'):
            try:
                # Updated Excel file name
                github_url = "https://raw.githubusercontent.com/Arun2310Rajaputhra/INVESTORS-DASHBOARD/main/INVESTMENT_APP_DETAILS_UPDATE.xlsx"
                excel_data = pd.ExcelFile(github_url)
                
                # Load all sheets
                sheets = {}
                for sheet_name in excel_data.sheet_names:
                    if sheet_name in ['Platform_Maintaince_Charges', 'Platform_Maintenance_Charges', 'Charges']:
                        df = excel_data.parse(sheet_name)
                        df.columns = df.columns.str.strip()
                        sheets[sheet_name] = df
                    else:
                        sheets[sheet_name] = excel_data.parse(sheet_name)
                
                # Success animation
                st.success("✅ Data loaded successfully!")
                time.sleep(0.5)
                
                return sheets
            except Exception as e:
                st.error(f"❌ Error loading data: {str(e)}")
                return {}
            finally:
                time.sleep(0.5)
                loading_placeholder.empty()

def calculate_user_metrics(user_id, data):
    """Calculate all metrics for a specific user"""
    # Get investor details
    investor_df = data.get('Investor_Details', pd.DataFrame())
    daily_profits_df = data.get('Daily_Profits_Calculations', pd.DataFrame())
    daily_report_df = data.get('Daily_Report', pd.DataFrame())
    charges_df = data.get('Platform_Maintaince_Charges', pd.DataFrame())
    
    # Filter for current user
    user_info = investor_df[investor_df['UserID'] == user_id]
    
    if user_info.empty:
        return None
    
    metrics = {
        'user_id': user_id,
        'name': user_info.iloc[0]['Name'] if 'Name' in user_info.columns else user_info.iloc[0]['Contact_Name'],
        'total_investment': float(user_info.iloc[0]['Total_Invested_Amount']),
        'total_profit': float(user_info.iloc[0]['Total Profit Earned']) if 'Total Profit Earned' in user_info.columns else 0,
    }
    
    # Calculate ROI
    if metrics['total_investment'] > 0:
        metrics['roi'] = (metrics['total_profit'] / metrics['total_investment']) * 100
    else:
        metrics['roi'] = 0
    
    # Calculate expected monthly returns (average daily profit × 30)
    user_daily_profits = daily_report_df[daily_report_df['UserID'] == user_id]
    user_daily_profits = user_daily_profits[user_daily_profits['Profit'] > 0]  # Exclude negatives
    
    if not user_daily_profits.empty:
        avg_daily_profit = user_daily_profits['Profit'].mean()
        metrics['expected_monthly'] = avg_daily_profit * 30
        metrics['avg_daily_profit'] = avg_daily_profit
    else:
        metrics['expected_monthly'] = 0
        metrics['avg_daily_profit'] = 0
    
    # Get investment history
    user_investments = daily_profits_df[daily_profits_df['UserID'] == user_id]
    user_investments = user_investments[user_investments['User_Invested_Amount'].notna()]
    
    investment_history = []
    for _, row in user_investments.iterrows():
        investment_history.append({
            'date': row['Date'] if pd.notna(row['Date']) else row['Transaction_Date'],
            'amount': row['User_Invested_Amount'],
            'transaction_id': row.get('Transaction_ID', 'N/A')
        })
    metrics['investment_history'] = investment_history
    
    # Get pending charges - WITH ERROR HANDLING
    pending_charges = []
    if not charges_df.empty:
        # Try to find UserID column with different variations
        user_id_column = None
        possible_column_names = ['UserID', 'Userid', 'USERID', 'userid', 'User ID', 'User_Id']
        
        for col in possible_column_names:
            if col in charges_df.columns:
                user_id_column = col
                break
        
        if user_id_column:
            user_charges = charges_df[charges_df[user_id_column] == user_id]
            if not user_charges.empty:
                for _, row in user_charges.iterrows():
                    # Get pending amount with error handling
                    pending_amt = 0
                    try:
                        pending_amt = float(row.get('Pending_Amt', 0))
                    except (ValueError, TypeError):
                        try:
                            pending_amt = float(row.get('Pending_Amt', 0))
                        except:
                            pending_amt = 0
                    
                    if pd.notna(pending_amt) and pending_amt > 0:
                        pending_charges.append({
                            'reason': row.get('Reason_For_Charge', 'N/A'),
                            'amount': pending_amt,
                            'charge_per_head': float(row.get('Charge_Per_Head', 0))
                        })
    
    metrics['pending_charges'] = pending_charges
    
    return metrics

def create_company_profit_graph(data):
    """Create company profit graph (excluding negatives)"""
    daily_report_df = data.get('Daily_Report', pd.DataFrame())
    
    if daily_report_df.empty:
        return None
    
    # Group by date and sum profits (exclude negatives)
    daily_report_df['Date'] = pd.to_datetime(daily_report_df['Date'])
    company_daily = daily_report_df[daily_report_df['Profit'] > 0].groupby('Date')['Profit'].sum().reset_index()
    
    if company_daily.empty:
        return None
    
    fig = px.line(
        company_daily,
        x='Date',
        y='Profit',
        title='📈 Company Daily Profit Trend (Positive Profits Only)',
        markers=True,
        line_shape='spline',
        color_discrete_sequence=['#00ff88']
    )
    
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Total Profit (₹)',
        hovermode='x unified',
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        transition={'duration': 500}
    )
    
    return fig

def create_user_profit_table(user_id, data, selected_date=None, payment_status=None):
    """Create filtered profit table for user"""
    daily_report_df = data.get('Daily_Report', pd.DataFrame())
    
    if daily_report_df.empty:
        return pd.DataFrame()
    
    # Filter for user
    user_data = daily_report_df[daily_report_df['UserID'] == user_id].copy()
    
    # Make sure Total_Profit column exists (rename if needed)
    if 'Total_Profit' not in user_data.columns and 'Total Profit' in user_data.columns:
        user_data['Total_Profit'] = user_data['Total Profit']
    
    # Apply date filter if selected
    if selected_date:
        if isinstance(selected_date, list) and len(selected_date) == 2:
            start_date, end_date = selected_date
            user_data = user_data[
                (pd.to_datetime(user_data['Date']) >= pd.to_datetime(start_date)) &
                (pd.to_datetime(user_data['Date']) <= pd.to_datetime(end_date))
            ]
        else:
            user_data = user_data[pd.to_datetime(user_data['Date']) == pd.to_datetime(selected_date)]
    
    # Apply payment status filter
    if payment_status and payment_status != 'All':
        user_data = user_data[user_data['Payment'] == payment_status]
    
    # Sort by date
    user_data = user_data.sort_values('Date', ascending=False)
    
    return user_data

def main():
    # Enhanced dashboard title
    st.markdown("""
    <div class="dashboard-title">
        <h6>QUANTUM PREDICTIONS</h6>
        <p>AI-ENHANCED FORECASTING & SIMULATION</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add welcome animation
    welcome_text = "Welcome to QUANTUM PREDICTIONS"
    display = st.empty()
    for i in range(len(welcome_text) + 1):
        display.markdown(f"<h3 style='text-align: center; color: white;'>{welcome_text[:i]}|</h3>", unsafe_allow_html=True)
        time.sleep(0.05)
    time.sleep(0.5)
    display.empty()
    
    # Load data
    data = load_excel_data()
    
    if not data:
        st.error("❌ No data loaded. Please check the data source.")
        return
    
    # Sidebar for login and filters
    with st.sidebar:
        st.markdown("## 🔐 User Login")
        
        # Get all user IDs for dropdown
        investor_df = data.get('Investor_Details', pd.DataFrame())
        if investor_df.empty:
            st.error("No investor data found.")
            st.stop()
            
        user_ids = investor_df['UserID'].unique().tolist() if not investor_df.empty else []
        
        if user_ids:
            selected_user = st.selectbox("Select your User ID:", user_ids)
            
            if selected_user:
                # Calculate user metrics
                metrics = calculate_user_metrics(selected_user, data)
                
                if metrics:
                    # Success animation for login
                    st.success(f"✅ Welcome, {metrics['name']}!")
                    time.sleep(0.3)
                    
                    st.markdown("## 📅 Filters")
                    
                    # Date range selector
                    col1, col2 = st.columns(2)
                    with col1:
                        start_date = st.date_input("Start Date", 
                                                  value=datetime.now() - timedelta(days=30))
                    with col2:
                        end_date = st.date_input("End Date", 
                                                value=datetime.now())
                    
                    date_range = [start_date, end_date]
                    
                    # Payment status filter
                    payment_status = st.selectbox(
                        "Payment Status:",
                        ["All", "Completed", "Pending", "Recovered"]
                    )
                else:
                    st.error("User not found in records.")
                    st.stop()
            else:
                st.info("Please select a User ID to continue.")
                st.stop()
        else:
            st.error("No investor data found.")
            st.stop()
    
    # Main Dashboard
    if metrics:
        # Welcome header with animation
        st.markdown(f"<h4 class='main-header'>Hello, {metrics['name']}!</h4>", unsafe_allow_html=True)
        
        # Profit celebration animation
        if metrics['total_profit'] > 0:
            st.balloons()
            st.markdown("""<div class='success-message'>
                <div style='background-color: rgba(212, 237, 218, 0.9); color: #155724; padding: 1rem; border-radius: 5px; backdrop-filter: blur(5px);'>
                    🎉 Great! You're making positive profits!
                </div>
            </div>""", unsafe_allow_html=True)
        
        # Key Metrics in columns
        st.markdown("<h3 style='color: white;'>📈 Investment Overview</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='color: #a0d2ff;'>Your Total Investment</h4>
                <h2 style='color: white;'>₹{int(metrics['total_investment']):,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            profit_class = "profit-positive" if metrics['total_profit'] >= 0 else "profit-negative"
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='color: #a0d2ff;'>Your Total Profit</h4>
                <h2 class='{profit_class}'>₹{metrics['total_profit']:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            roi_class = "profit-positive" if metrics['roi'] >= 0 else "profit-negative"
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='color: #a0d2ff;'>ROI</h4>
                <h2 class='{roi_class}'>{metrics['roi']:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='color: #a0d2ff;'>Expected Month End</h4>
                <h2 style='color: white;'>₹{metrics['expected_monthly']:,.2f}</h2>
                <small style='color: #a0d2ff;'>Based on daily avg: ₹{metrics['avg_daily_profit']:.2f}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Company Profit Graph
        st.markdown("<h3 style='color: white;'>📊 Company Profit Trend</h3>", unsafe_allow_html=True)
        profit_fig = create_company_profit_graph(data)
        if profit_fig:
            # Wrap plotly chart in a transparent container
            st.markdown("<div class='plotly-container'>", unsafe_allow_html=True)
            st.plotly_chart(profit_fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No profit data available for graph.")
        
        # Filtered Data Table
        st.markdown("<h3 style='color: white;'>📋 Your Profit Details</h3>", unsafe_allow_html=True)
        
        # Get filtered data
        filtered_data = create_user_profit_table(
            metrics['user_id'], 
            data, 
            date_range, 
            payment_status
        )
        
        if not filtered_data.empty:
            # Display summary stats with animation
            total_profit_filtered = filtered_data['Profit'].sum()
            avg_daily_filtered = filtered_data['Profit'].mean()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(f"Total Profit ({date_range[0]} to {date_range[1]})", 
                         f"₹{total_profit_filtered:,.2f}")
            
            with col2:
                st.metric(f"Average Daily Profit", 
                         f"₹{avg_daily_filtered:,.2f}")
            
            # Update display columns to include Total_Profit
            display_cols = ['Date', 'Invest_Amount', 'Company_Total_Invest', 'Profit', 'Total_Profit', 'Payment']
            display_cols = [col for col in display_cols if col in filtered_data.columns]
            
            st.dataframe(
                filtered_data[display_cols].rename(columns={
                    'Date': 'Date',
                    'Invest_Amount': 'Your Investment',
                    'Company_Total_Invest': 'Company Total',
                    'Profit': 'Your Profit',
                    'Total_Profit': 'Company Profit',
                    'Payment': 'Status'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Download button for filtered data
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data",
                data=csv,
                file_name=f"{metrics['user_id']}_profit_data.csv",
                mime="text/csv",
            )
        else:
            st.info("No data found for the selected filters.")
        
        # Investment History
        st.markdown("<h3 style='color: white;'>💰 Your Investment History</h3>", unsafe_allow_html=True)
        if metrics['investment_history']:
            invest_df = pd.DataFrame(metrics['investment_history'])
            st.dataframe(
                invest_df.rename(columns={
                    'date': 'Investment Date',
                    'amount': 'Amount (₹)',
                    'transaction_id': 'Transaction ID'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No investment history found.")
        
        # Pending Charges
        st.markdown("<h3 style='color: white;'>⚠️ Platform Charges Status</h3>", unsafe_allow_html=True)
        if metrics['pending_charges']:
            for charge in metrics['pending_charges']:
                st.markdown(f"""
                <div class='pending-alert'>
                    <strong>Reason:</strong> {charge['reason']}<br>
                    <strong>Pending Amount:</strong> ₹{charge['amount']:,.2f}<br>
                    <strong>Charge Per Head:</strong> ₹{charge['charge_per_head']:,.2f}
                </div>
                """, unsafe_allow_html=True)
            
            total_pending = sum(float(c['amount']) for c in metrics['pending_charges'])
            st.warning(f"**Total Pending Charges: ₹{total_pending:,.2f}**")
        else:
            st.success("✅ All platform charges are cleared!")
        
        # Additional Insights
        st.markdown("<h3 style='color: white;'>📊 Additional Insights</h3>", unsafe_allow_html=True)
        
        # Get the Daily_Report data
        daily_report_df = data.get('Daily_Report', pd.DataFrame())
        
        # Calculate total company profit (sum of all profits)
        total_company_profit = 0
        if not daily_report_df.empty:
            total_company_profit = daily_report_df['Profit'].sum()
        
        # Company total investment
        company_total = investor_df['Total_Invested_Amount'].sum() if not investor_df.empty else 0
        
        # Display in 3 columns EXACTLY like the others
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='color: #a0d2ff;'>Total Company Investment</h4>
                <h2 style='color: white;'>₹{company_total:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_investors = len(investor_df)
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='color: #a0d2ff;'>Total Investors</h4>
                <h2 style='color: white;'>{total_investors}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='color: #a0d2ff;'>Total Company Profit</h4>
                <h2 style='color: white;'>₹{total_company_profit:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.error("Could not load user metrics. Please try again.")

if __name__ == "__main__":
    main()