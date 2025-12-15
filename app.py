import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
import time
import base64

# Page configuration
st.set_page_config(
    page_title="QUANTUM PREDICTIONS",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to encode image to base64
def get_image_base64(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Try to get base64 for background image (for local testing)
background_base64 = None
title_header_base64 = None

# Custom CSS with animations and background
st.markdown(f"""
<style>
    /* Main background with uploaded image */
    .stApp {{
        background: linear-gradient(rgba(0, 15, 40, 0.85), rgba(0, 15, 40, 0.9)),
                    url('https://raw.githubusercontent.com/Arun2310Rajaputhra/INVESTORS-DASHBOARD/main/background_website.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        min-height: 100vh;
    }}
    
    /* Header styling */
    .main-header {{
        text-align: center;
        margin-bottom: 2rem;
        padding: 0.5rem;
        animation: fadeIn 1s;
    }}
    
    /* Title header image styling */
    .title-header-img {{
        max-width: 100%;
        height: auto;
        margin: 0 auto;
        display: block;
        animation: fadeIn 1s ease-out;
    }}
    
    /* On mobile, make title header responsive */
    @media (max-width: 768px) {{
        .title-header-img {{
            max-width: 95%;
            margin-top: 0.5rem;
        }}
    }}
    
    /* Quantum Predictions zoom animation */
    .quantum-title {{
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-align: center;
        margin: 1rem 0 0.5rem 0;
        animation: zoomIn 1s ease-out;
    }}
    
    .quantum-subtitle {{
        font-size: 1.2rem;
        color: #a0d2ff;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
        letter-spacing: 2px;
        animation: fadeInUp 1s ease-out 0.5s both;
    }}
    
    /* Content containers with transparency */
    .main .block-container {{
        padding-top: 1rem;
        padding-bottom: 3rem;
    }}
    
    .metric-card {{
        background-color: rgba(0, 31, 63, 0.85);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s, box-shadow 0.3s;
        animation: slideUp 0.5s ease-out;
        border: 1px solid rgba(30, 136, 229, 0.3);
        backdrop-filter: blur(10px);
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
        border-color: rgba(30, 136, 229, 0.6);
    }}
    
    .profit-positive {{
        color: #00ff88;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
    }}
    
    .profit-negative {{
        color: #ff5252;
        font-weight: bold;
    }}
    
    .pending-alert {{
        background-color: rgba(255, 243, 205, 0.9);
        border: 1px solid #FFEEBA;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        animation: fadeIn 0.5s;
    }}
    
    /* Dataframes with transparency */
    .dataframe {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 8px;
        overflow: hidden;
    }}
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background-color: rgba(0, 20, 40, 0.9) !important;
        border-right: 1px solid rgba(30, 136, 229, 0.3);
    }}
    
    .sidebar .sidebar-content {{
        background-color: transparent;
    }}
    
    /* Money animation */
    .money-celebration {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
    }}
    
    .money-symbol {{
        position: absolute;
        font-size: 2rem;
        opacity: 0;
        animation: moneyZoom 2s forwards;
    }}
    
    /* Copyright footer */
    .copyright-footer {{
        position: fixed;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 12px;
        color: #aaa;
        padding: 5px;
        background-color: rgba(0, 0, 0, 0.3);
        z-index: 1000;
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes slideUp {{
        from {{ transform: translateY(20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    @keyframes zoomIn {{
        0% {{ transform: scale(0.3); opacity: 0; }}
        70% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    
    @keyframes fadeInUp {{
        from {{ transform: translateY(20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    @keyframes moneyZoom {{
        0% {{ transform: scale(0.1) rotate(0deg); opacity: 0; }}
        20% {{ opacity: 1; }}
        80% {{ opacity: 1; }}
        100% {{ transform: scale(2) rotate(20deg); opacity: 0; }}
    }}
    
    /* Smooth transitions for plotly charts */
    .js-plotly-plot .plotly {{
        transition: opacity 0.5s ease-in-out;
    }}
    
    /* Button styling */
    .stButton > button {{
        background-color: #1E88E5;
        color: white;
        border: none;
        transition: all 0.3s;
    }}
    
    .stButton > button:hover {{
        background-color: #0d47a1;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
    }}
</style>
""", unsafe_allow_html=True)

# Add copyright footer
st.markdown("""
<div class="copyright-footer">
    © Copyright 2011. All rights reserved with Rajaputra Arun Kumar, Hyderabad
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_excel_data():
    """Load all sheets from the Excel file"""
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        with st.spinner('📊 Loading latest investment data...'):
            try:
                github_url = "https://raw.githubusercontent.com/Arun2310Rajaputhra/INVESTORS-DASHBOARD/main/INVESTMENT_APP_DETAILS_UPDATE.xlsx"
                excel_data = pd.ExcelFile(github_url)
                
                sheets = {}
                for sheet_name in excel_data.sheet_names:
                    if sheet_name in ['Platform_Maintaince_Charges', 'Platform_Maintenance_Charges', 'Charges']:
                        df = excel_data.parse(sheet_name)
                        df.columns = df.columns.str.strip()
                        sheets[sheet_name] = df
                    else:
                        sheets[sheet_name] = excel_data.parse(sheet_name)
                
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
    investor_df = data.get('Investor_Details', pd.DataFrame())
    daily_profits_df = data.get('Daily_Profits_Calculations', pd.DataFrame())
    daily_report_df = data.get('Daily_Report', pd.DataFrame())
    charges_df = data.get('Platform_Maintaince_Charges', pd.DataFrame())
    
    user_info = investor_df[investor_df['UserID'] == user_id]
    
    if user_info.empty:
        return None
    
    metrics = {
        'user_id': user_id,
        'name': user_info.iloc[0]['Name'] if 'Name' in user_info.columns else user_info.iloc[0]['Contact_Name'],
        'total_investment': float(user_info.iloc[0]['Total_Invested_Amount']),
        'total_profit': float(user_info.iloc[0]['Total Profit Earned']) if 'Total Profit Earned' in user_info.columns else 0,
    }
    
    if metrics['total_investment'] > 0:
        metrics['roi'] = (metrics['total_profit'] / metrics['total_investment']) * 100
    else:
        metrics['roi'] = 0
    
    user_daily_profits = daily_report_df[daily_report_df['UserID'] == user_id]
    user_daily_profits = user_daily_profits[user_daily_profits['Profit'] > 0]
    
    if not user_daily_profits.empty:
        avg_daily_profit = user_daily_profits['Profit'].mean()
        metrics['expected_monthly'] = avg_daily_profit * 30
        metrics['avg_daily_profit'] = avg_daily_profit
    else:
        metrics['expected_monthly'] = 0
        metrics['avg_daily_profit'] = 0
    
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
    
    pending_charges = []
    if not charges_df.empty:
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
    
    user_data = daily_report_df[daily_report_df['UserID'] == user_id].copy()
    
    if 'Total_Profit' not in user_data.columns and 'Total Profit' in user_data.columns:
        user_data['Total_Profit'] = user_data['Total Profit']
    
    if selected_date:
        if isinstance(selected_date, list) and len(selected_date) == 2:
            start_date, end_date = selected_date
            user_data = user_data[
                (pd.to_datetime(user_data['Date']) >= pd.to_datetime(start_date)) &
                (pd.to_datetime(user_data['Date']) <= pd.to_datetime(end_date))
            ]
        else:
            user_data = user_data[pd.to_datetime(user_data['Date']) == pd.to_datetime(selected_date)]
    
    if payment_status and payment_status != 'All':
        user_data = user_data[user_data['Payment'] == payment_status]
    
    user_data = user_data.sort_values('Date', ascending=False)
    
    return user_data

def show_money_animation():
    """Simple money animation without complex formatting"""
    import random
    
    symbols = ['💰', '💵', '₹', '$', '💎']
    html = '<div class="money-celebration">'
    
    for _ in range(12):
        sym = random.choice(symbols)
        left = random.randint(5, 95)
        top = random.randint(5, 95)
        delay = random.uniform(0, 1.5)
        size = random.uniform(1.2, 2.0)
        
        html += f'''
        <div class="money-symbol" style="
            left:{left}%;
            top:{top}%;
            font-size:{size}rem;
            animation-delay:{delay}s;
        ">{sym}</div>
        '''
    
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)
    time.sleep(2)
    st.rerun()

def main():
    # Display title header image
    st.markdown("""
    <div class="main-header">
        <img src="https://raw.githubusercontent.com/Arun2310Rajaputhra/INVESTORS-DASHBOARD/main/title_header.jpg" 
             alt="QUANTUM PREDICTIONS" 
             class="title-header-img">
    </div>
    """, unsafe_allow_html=True)
    
    # Add zoom animation title (as fallback if image doesn't load)
    st.markdown("""
    <div style="display: none;">
        <h1 class="quantum-title">QUANTUM PREDICTIONS</h1>
        <p class="quantum-subtitle">AI-ENHANCED FORECASTING & SIMULATION</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    data = load_excel_data()
    
    if not data:
        st.error("❌ No data loaded. Please check the data source.")
        return
    
    # Sidebar for login and filters
    with st.sidebar:
        st.markdown("## 🔐 User Login")
        
        investor_df = data.get('Investor_Details', pd.DataFrame())
        if investor_df.empty:
            st.error("No investor data found.")
            st.stop()
            
        user_ids = investor_df['UserID'].unique().tolist() if not investor_df.empty else []
        
        if user_ids:
            selected_user = st.selectbox("Select your User ID:", user_ids)
            
            if selected_user:
                metrics = calculate_user_metrics(selected_user, data)
                
                if metrics:
                    st.success(f"✅ Welcome, {metrics['name']}!")
                    time.sleep(0.3)
                    
                    st.markdown("## 📅 Filters")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        start_date = st.date_input("Start Date", 
                                                  value=datetime.now() - timedelta(days=30))
                    with col2:
                        end_date = st.date_input("End Date", 
                                                value=datetime.now())
                    
                    date_range = [start_date, end_date]
                    
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
        # Show money animation if profit is positive
        if metrics['total_profit'] > 0:
            show_money_animation()
        
        st.markdown(f"<h3 style='color: white; margin-bottom: 1.5rem;'>Hello, {metrics['name']}!</h3>", unsafe_allow_html=True)
        
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
            st.plotly_chart(profit_fig, use_container_width=True)
        else:
            st.info("No profit data available for graph.")
        
        # Filtered Data Table
        st.markdown("<h3 style='color: white;'>📋 Your Profit Details</h3>", unsafe_allow_html=True)
        
        filtered_data = create_user_profit_table(
            metrics['user_id'], 
            data, 
            date_range, 
            payment_status
        )
        
        if not filtered_data.empty:
            total_profit_filtered = filtered_data['Profit'].sum()
            avg_daily_filtered = filtered_data['Profit'].mean()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(f"Total Profit ({date_range[0]} to {date_range[1]})", 
                         f"₹{total_profit_filtered:,.2f}")
            
            with col2:
                st.metric(f"Average Daily Profit", 
                         f"₹{avg_daily_filtered:,.2f}")
            
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
        
        daily_report_df = data.get('Daily_Report', pd.DataFrame())
        
        total_company_profit = 0
        if not daily_report_df.empty:
            total_company_profit = daily_report_df['Profit'].sum()
        
        company_total = investor_df['Total_Invested_Amount'].sum() if not investor_df.empty else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Company Investment", f"₹{company_total:,.2f}")
        
        with col2:
            total_investors = len(investor_df)
            st.metric("Total Investors", total_investors)
        
        with col3:
            st.metric("Total Company Profit", f"₹{total_company_profit:,.2f}")
    
    else:
        st.error("Could not load user metrics. Please try again.")

if __name__ == "__main__":
    main()