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

# Initialize session state for popup
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = True  # Changed to True by default

# Initialize session state for terms popup
if 'show_terms_popup' not in st.session_state:
    st.session_state.show_terms_popup = True  # Show by default

# Custom CSS with animations
st.markdown("""
<style>
    /* Background image */
    .stApp {
        background: url('https://raw.githubusercontent.com/Arun2310Rajaputhra/INVESTORS-DASHBOARD/main/background_website.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Make content readable */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.05);
        padding-top: 1rem;
    }
    
    /* Transparent plotly charts container (from Code 2) */
    .js-plotly-plot .plotly {
        background-color: transparent !important;
    }
    
    .plotly-container {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(1px);
    }
    
    .main-header {
        font-size: 1.6rem;
        color: #1E88E5;
        margin-bottom: 1rem;
        animation: fadeIn 1s;
    }
    
    /* GLASS EFFECT for Investment Overview metric cards ONLY */
    .metric-card {
        background-color: rgba(0, 31, 63, 0.55); /* Changed to semi-transparent */
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
        animation: slideUp 0.5s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.1); /* Added glass border */
        backdrop-filter: blur(1px); /* Added glass blur effect */
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        background-color: rgba(0, 31, 63, 0.65); /* Slightly more opaque on hover */
    }
    
    /* Light Red Color for Subheadings */
    .light-red-heading {
        color: #FF6B6B; /* Light Red Color */
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(255, 107, 107, 0.3);
        animation: fadeIn 0.8s;
    }
    
    /* BRIGHT SHINING RED for Platform Charges Status */
    .bright-red-heading {
        color: #FF0000 !important; /* Bright Shining Red */
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(255, 0, 0, 0.5);
        animation: fadeIn 0.8s, pulseBright 2s infinite;
        text-shadow: 0 0 8px rgba(255, 0, 0, 0.5);
    }
    
    @keyframes pulseBright {
        0% { text-shadow: 0 0 5px rgba(255, 0, 0, 0.5); }
        50% { text-shadow: 0 0 15px rgba(255, 0, 0, 0.8); }
        100% { text-shadow: 0 0 5px rgba(255, 0, 0, 0.5); }
    }
    
    /* WhatsApp Icon - FIXED POSITION */
    .whatsapp-float {
        position: fixed;
        bottom: 80px;
        right: 20px;
        z-index: 9999;
    }
    
    .whatsapp-icon-circle {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        animation: floatUp 0.5s ease-out;
        position: relative;
        background: linear-gradient(135deg, #25D366, #128C7E);
    }
    
    .whatsapp-icon-circle:hover {
        transform: scale(1.1) translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }
    
    .whatsapp-icon-circle:active {
        transform: scale(0.95);
    }
    
    .whatsapp-icon-circle i {
        font-size: 30px;
        color: white;
    }
    
    .whatsapp-tooltip {
        position: absolute;
        right: 70px;
        top: 50%;
        transform: translateY(-50%);
        background-color: rgba(0, 0, 0, 0.85);
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 500;
        white-space: nowrap;
        opacity: 0;
        transition: opacity 0.3s;
        pointer-events: none;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }
    
    .whatsapp-icon-circle:hover .whatsapp-tooltip {
        opacity: 1;
    }
    
    .profit-positive {
        color: #00C853;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    .profit-negative {
        color: #FF5252;
        font-weight: bold;
    }
    .pending-alert {
        background-color: #FFF3CD;
        border: 1px solid #FFEEBA;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        animation: fadeIn 0.5s;
    }
    .success-message {
        animation: slideIn 0.5s, fadeOut 2s 3s forwards;
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    
    /* Footer for copyright (from Code 2) */
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
        z-index: 9998;
        backdrop-filter: blur(1px);
    }
    
    /* Page Links Footer */
    .page-links-footer {
        width: 100%;
        text-align: center;
        padding: 20px 0;
        margin-top: 40px;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        background-color: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(1px);
        animation: fadeIn 1s;
    }
    
    .page-links-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
        flex-wrap: wrap;
    }
    
    .page-link-item {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #a0d2ff;
        text-decoration: none;
        font-size: 14px;
        transition: all 0.3s ease;
        padding: 8px 15px;
        border-radius: 5px;
        background-color: rgba(0, 31, 63, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .page-link-item:hover {
        background-color: rgba(0, 31, 63, 0.5);
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        text-decoration: none;
    }
    
    .page-link-item i {
        font-size: 16px;
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
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    @keyframes floatUp {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Pending Alert Banner */
    .pending-banner {
        background: linear-gradient(90deg, #FF6B6B, #FF8E53);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        border-left: 5px solid #FF0000;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        animation: slideInRight 0.5s ease-out;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .pending-banner-content {
        flex: 1;
    }
    
    .pending-banner-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .pending-banner-message {
        font-size: 14px;
        opacity: 0.9;
    }
    
    .pending-banner-amount {
        background: rgba(255, 255, 255, 0.2);
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        margin-left: 15px;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .pending-banner-close {
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        padding: 8px 15px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        margin-left: 15px;
        transition: all 0.3s ease;
    }
    
    .pending-banner-close:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.05);
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Highlight text */
    .highlight-text {
        color: #FFD700;
        font-weight: bold;
        background: rgba(255, 215, 0, 0.1);
        padding: 2px 8px;
        border-radius: 4px;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    /* Terms & Conditions Banner */
    .terms-banner {
        background: linear-gradient(90deg, #4A6FA5, #6B8DC3);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        border-left: 5px solid #1E3A5F;
        box-shadow: 0 4px 15px rgba(74, 111, 165, 0.3);
        animation: slideInRight 0.5s ease-out;
    }
    
    .terms-banner-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .terms-banner-content {
        font-size: 14px;
        margin-bottom: 15px;
        opacity: 0.9;
    }
    
    .terms-link {
        color: #FFD700;
        font-weight: bold;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 5px 10px;
        background: rgba(255, 215, 0, 0.1);
        border-radius: 4px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .terms-link:hover {
        background: rgba(255, 215, 0, 0.2);
        text-decoration: none;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(255, 215, 0, 0.2);
    }
    
    .terms-buttons {
        display: flex;
        gap: 10px;
        margin-top: 15px;
    }
    
    /* Remarks Column Text Wrapping */
    .stDataFrame [data-testid="stDataFrame"] td {
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
</style>
""", unsafe_allow_html=True)

# Add copyright footer
st.markdown("""
<div class="copyright-footer">
    © Copyright 2025. All rights reserved with Rajaputra Arun Kumar, Hyderabad
</div>
""", unsafe_allow_html=True)

# Add WhatsApp Icon - SINGLE ICON
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

<div class="whatsapp-float">
    <!-- WhatsApp Icon Only -->
    <a href="https://wa.me/919398854605?text=Hello%20from%20Quantum%20Predictions%20Dashboard" 
       target="_blank" style="text-decoration: none;" rel="noopener noreferrer">
        <div class="whatsapp-icon-circle">
            <i class="fab fa-whatsapp"></i>
            <span class="whatsapp-tooltip">Chat on WhatsApp</span>
        </div>
    </a>
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
    
    return metrics

def get_user_reinvestment_data(user_id, data):
    """Get re-investment details for specific user"""
    re_invest_df = data.get('Re_Investment_Details', pd.DataFrame())
    if re_invest_df.empty:
        return pd.DataFrame()
    
    # Try different possible column names for UserID
    user_id_column = None
    possible_column_names = ['UserID', 'Userid', 'USERID', 'userid', 'User ID', 'User_Id']
    
    for col in possible_column_names:
        if col in re_invest_df.columns:
            user_id_column = col
            break
    
    if user_id_column:
        # Filter for user
        user_reinvest = re_invest_df[re_invest_df[user_id_column] == user_id].copy()
        
        # Select only required columns
        required_columns = ['Re-Invest_ID', 'Requested_Amount', 'Total_Added_Amount', 
                          'Pending_Amount_To_Be_Add', 'Applied_To_Main_Investment_Status']
        
        # Filter only existing columns
        available_columns = [col for col in required_columns if col in user_reinvest.columns]
        
        if not user_reinvest.empty and available_columns:
            return user_reinvest[available_columns]
    
    return pd.DataFrame()

def get_user_platform_charges_data(user_id, data):
    """Get platform charges details for specific user - SIMPLE VERSION like Re-Investment section"""
    # Try to get the sheet with the correct name
    charges_df = data.get('Platofrm_Maintaince_Charges', pd.DataFrame())
    
    # If not found, try alternative names
    if charges_df.empty:
        charges_df = data.get('Platform_Maintaince_Charges', pd.DataFrame())
    
    if charges_df.empty:
        charges_df = data.get('Platform_Maintenance_Charges', pd.DataFrame())
    
    if charges_df.empty:
        charges_df = data.get('Charges', pd.DataFrame())
    
    if charges_df.empty:
        return pd.DataFrame()
    
    # Try different possible column names for UserID
    user_id_column = None
    possible_column_names = ['UserID', 'Userid', 'USERID', 'userid', 'User ID', 'User_Id']
    
    for col in possible_column_names:
        if col in charges_df.columns:
            user_id_column = col
            break
    
    if user_id_column:
        # Filter for user
        user_charges = charges_df[charges_df[user_id_column] == user_id].copy()
        
        # Select only required columns as specified
        required_columns = ['Charge_ID', 'Reason_For_Charge', 'Charge_Per_Head', 'Paid_Amt', 'Pending_Amt']
        
        # Filter only existing columns
        available_columns = [col for col in required_columns if col in user_charges.columns]
        
        if not user_charges.empty and available_columns:
            return user_charges[available_columns]
    
    return pd.DataFrame()

def create_company_profit_graph(data):
    """Create company profit graph (excluding negatives) with transparent style from Code 2"""
    daily_report_df = data.get('Daily_Report', pd.DataFrame())
    
    if daily_report_df.empty:
        return None
    
    # Group by date and sum profits (exclude negatives)
    daily_report_df['Date'] = pd.to_datetime(daily_report_df['Date'])
    company_daily = daily_report_df[daily_report_df['Profit'] > 0].groupby('Date')['Profit'].sum().reset_index()
    
    if company_daily.empty:
        return None
    
    # Using style from Code 2
    fig = px.line(
        company_daily,
        x='Date',
        y='Profit',
        title='📈 Company Daily Profit Trend (Positive Profits Only)',
        markers=True,
        line_shape='spline',
        color_discrete_sequence=['#00ff88']  # From Code 2
    )
    
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Total Profit (₹)',
        hovermode='x unified',
        template='plotly_dark',  # Changed from Code 1's 'plotly_white' to Code 2's 'plotly_dark'
        plot_bgcolor='rgba(0,0,0,0)',  # From Code 2
        paper_bgcolor='rgba(0,0,0,0)',  # From Code 2
        font_color='white',  # From Code 2
        transition={'duration': 500}
    )
    
    return fig

def create_investment_vs_profit_chart(data, selected_user=None):
    """Create candle-type vertical bar chart for investment vs profit"""
    investor_df = data.get('Investor_Details', pd.DataFrame())
    
    if investor_df.empty:
        return None
    
    # Prepare data for all users or specific user
    if selected_user:
        investor_df = investor_df[investor_df['UserID'] == selected_user]
        if investor_df.empty:
            return None
    
    # Sort by total investment (descending) for better visualization
    investor_df = investor_df.sort_values('Total_Invested_Amount', ascending=False)
    
    # Get top 10 users if too many
    if len(investor_df) > 10 and not selected_user:
        investor_df = investor_df.head(10)
    
    # Create figure
    fig = go.Figure()
    
    # Add Investment bars (base)
    fig.add_trace(go.Bar(
        x=investor_df['Name'] if 'Name' in investor_df.columns else investor_df['Contact_Name'],
        y=investor_df['Total_Invested_Amount'],
        name='Total Investment',
        marker_color='#1E88E5',  # Blue
        opacity=0.8,
        width=0.4,
        offset=-0.2,  # Position to left
        text=[f'₹{x:,.0f}' for x in investor_df['Total_Invested_Amount']],
        textposition='auto',
        hovertext=[
            f"<b>{name}</b><br>" +
            f"Investment: ₹{inv:,.2f}<br>" +
            f"Profit: ₹{profit:,.2f}<br>" +
            f"ROI: {roi:.1f}%"
            for name, inv, profit, roi in zip(
                investor_df['Name'] if 'Name' in investor_df.columns else investor_df['Contact_Name'],
                investor_df['Total_Invested_Amount'],
                investor_df['Total Profit Earned'] if 'Total Profit Earned' in investor_df.columns else [0]*len(investor_df),
                (investor_df['Total Profit Earned'] / investor_df['Total_Invested_Amount'] * 100) if 'Total Profit Earned' in investor_df.columns else [0]*len(investor_df)
            )
        ],
        hoverinfo='text'
    ))
    
    # Add Profit bars (on top)
    profit_column = 'Total Profit Earned' if 'Total Profit Earned' in investor_df.columns else 'Total Profit'
    
    # Determine profit colors (green for positive, red for negative)
    profit_colors = []
    for profit in investor_df[profit_column]:
        if profit >= 0:
            profit_colors.append('#00C853')  # Green
        else:
            profit_colors.append('#FF5252')  # Red
    
    fig.add_trace(go.Bar(
        x=investor_df['Name'] if 'Name' in investor_df.columns else investor_df['Contact_Name'],
        y=investor_df[profit_column],
        name='Total Profit',
        marker_color=profit_colors,
        opacity=0.8,
        width=0.4,
        offset=0.2,  # Position to right
        text=[f'₹{x:,.0f}' for x in investor_df[profit_column]],
        textposition='auto',
        hovertext=[
            f"<b>{name}</b><br>" +
            f"Investment: ₹{inv:,.2f}<br>" +
            f"Profit: ₹{profit:,.2f}<br>" +
            f"Status: {'Profit' if profit >= 0 else 'Loss'}<br>" +
            f"ROI: {roi:.1f}%"
            for name, inv, profit, roi in zip(
                investor_df['Name'] if 'Name' in investor_df.columns else investor_df['Contact_Name'],
                investor_df['Total_Invested_Amount'],
                investor_df[profit_column],
                (investor_df[profit_column] / investor_df['Total_Invested_Amount'] * 100)
            )
        ],
        hoverinfo='text'
    ))
    
    # Add connecting lines between bars (optional, creates candle effect)
    for i, (inv, profit) in enumerate(zip(investor_df['Total_Invested_Amount'], investor_df[profit_column])):
        # Add line from investment bar to profit bar
        fig.add_shape(
            type="line",
            x0=i-0.1, x1=i+0.1,
            y0=inv, y1=inv,
            line=dict(color="rgba(255,255,255,0.3)", width=1),
        )
    
    # Update layout
    fig.update_layout(
        title='📊 Investment vs Profit Analysis (Candle-Type Bars)',
        xaxis_title='Investors',
        yaxis_title='Amount (₹)',
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1,
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=500 if selected_user else 600,
        margin=dict(l=50, r=50, t=80, b=100)
    )
    
    # Format y-axis with ₹ symbol
    fig.update_yaxes(tickprefix='₹ ')
    
    # Rotate x-axis labels for better readability
    fig.update_xaxes(tickangle=45)
    
    return fig

def create_company_investment_vs_profit_chart(data):
    """Create candle-type vertical bar chart for COMPANY investment vs profit"""
    investor_df = data.get('Investor_Details', pd.DataFrame())
    
    if investor_df.empty:
        return None
    
    # Get company totals
    company_total_investment = investor_df['Total_Invested_Amount'].sum() if 'Total_Invested_Amount' in investor_df.columns else 0
    
    # Get total company profit from Daily_Report
    daily_report_df = data.get('Daily_Report', pd.DataFrame())
    total_company_profit = 0
    if not daily_report_df.empty:
        # Get unique daily Total_Profit values
        daily_report_df['Date'] = pd.to_datetime(daily_report_df['Date'])
        unique_daily = daily_report_df.drop_duplicates(subset=['Date'], keep='first')
        
        # Try to find Total_Profit column
        profit_column = None
        possible_column_names = ['Total_Profit', 'Total Profit', 'TotalProfit', 'total_profit']
        
        for col in possible_column_names:
            if col in unique_daily.columns:
                profit_column = col
                break
        
        if profit_column:
            total_company_profit = unique_daily[profit_column].sum()
        elif 'Profit' in unique_daily.columns:
            total_company_profit = unique_daily['Profit'].sum()
    
    # Create data for the chart
    categories = ['Company']
    investments = [company_total_investment]
    profits = [total_company_profit]
    
    # Create figure
    fig = go.Figure()
    
    # Add Investment bars (base)
    fig.add_trace(go.Bar(
        x=categories,
        y=investments,
        name='Total Company Investment',
        marker_color='#1E88E5',  # Blue
        opacity=0.8,
        width=0.4,
        offset=-0.2,  # Position to left
        text=[f'₹{x:,.0f}' for x in investments],
        textposition='auto',
        hovertext=[
            f"<b>Company</b><br>" +
            f"Total Investment: ₹{inv:,.2f}<br>" +
            f"Total Profit: ₹{profit:,.2f}<br>" +
            f"ROI: {roi:.1f}%"
            for inv, profit, roi in zip(
                investments,
                profits,
                [(profit/inv*100) if inv > 0 else 0 for inv, profit in zip(investments, profits)]
            )
        ],
        hoverinfo='text'
    ))
    
    # Add Profit bars (on top)
    profit_colors = ['#00C853' if profit >= 0 else '#FF5252' for profit in profits]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=profits,
        name='Total Company Profit',
        marker_color=profit_colors,
        opacity=0.8,
        width=0.4,
        offset=0.2,  # Position to right
        text=[f'₹{x:,.0f}' for x in profits],
        textposition='auto',
        hovertext=[
            f"<b>Company</b><br>" +
            f"Total Investment: ₹{inv:,.2f}<br>" +
            f"Total Profit: ₹{profit:,.2f}<br>" +
            f"Status: {'Profit' if profit >= 0 else 'Loss'}<br>" +
            f"ROI: {roi:.1f}%"
            for inv, profit, roi in zip(
                investments,
                profits,
                [(profit/inv*100) if inv > 0 else 0 for inv, profit in zip(investments, profits)]
            )
        ],
        hoverinfo='text'
    ))
    
    # Add connecting lines between bars
    for i, (inv, profit) in enumerate(zip(investments, profits)):
        # Add line from investment bar to profit bar
        fig.add_shape(
            type="line",
            x0=i-0.1, x1=i+0.1,
            y0=inv, y1=inv,
            line=dict(color="rgba(255,255,255,0.3)", width=1),
        )
    
    # Update layout
    fig.update_layout(
        title='🏢 Company Total Investment vs Total Profit',
        xaxis_title='',
        yaxis_title='Amount (₹)',
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1,
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Format y-axis with ₹ symbol
    fig.update_yaxes(tickprefix='₹ ')
    
    return fig

def create_user_profit_table(user_id, data, selected_date=None, payment_status=None):
    """Create filtered profit table for user"""
    daily_report_df = data.get('Daily_Report', pd.DataFrame())
    
    if daily_report_df.empty:
        return pd.DataFrame()
    
    # Filter for user
    user_data = daily_report_df[daily_report_df['UserID'] == user_id].copy()
    
    # Try to find Total_Profit column with different variations
    profit_column = None
    possible_column_names = ['Total_Profit', 'Total Profit', 'TotalProfit', 'total_profit']
    
    for col in possible_column_names:
        if col in user_data.columns:
            profit_column = col
            break
    
    # Make sure Total_Profit column exists (rename if found)
    if profit_column and profit_column != 'Total_Profit':
        user_data['Total_Profit'] = user_data[profit_column]
    elif 'Profit' in user_data.columns and 'Total_Profit' not in user_data.columns:
        # If only Profit column exists, use it as Total_Profit
        user_data['Total_Profit'] = user_data['Profit']
    
    # Check if Remarks column exists - if not, create empty column
    # This ensures the column appears even when empty
    if 'Remarks' not in user_data.columns:
        user_data['Remarks'] = ''
    
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
    # SOLUTION 1: Using rem units
    st.markdown("""
    <div style="text-align: center;">
        <h6 style="margin-bottom: 0; font-size: 1.8rem; color: yellow;">QUANTUM PREDICTIONS</h6>
        <p style="margin-top: -1.1rem; font-size: 0.66rem; color: #a0d2ff; letter-spacing: 1px;">
            AI-ENHANCED FORECASTING & SIMULATION
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add welcome animation
    welcome_text = "Welcome to QUANTUM PREDICTION"
    display = st.empty()
    for i in range(len(welcome_text) + 1):
        display.markdown(f"<h3 style='text-align: center;'>{welcome_text[:i]}|</h3>", unsafe_allow_html=True)
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
        st.header("🔐 User Login")
        
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
                    time.sleep(0.5)
                    
                    # Date range filter
                    st.header("📅 Filters")
                    
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
                        ["All", "Completed", "Pending", "Recovered", "Re-Invest"]
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
        # ==============================================
        # TERMS & CONDITIONS BANNER (NEW ADDITION)
        # ==============================================
        if st.session_state.show_terms_popup:
            st.markdown("""
            <div class="terms-banner">
                <div class="terms-banner-title">
                    <i class="fas fa-file-contract"></i>
                    📜 IMPORTANT: Terms & Conditions
                </div>
                <div class="terms-banner-content">
                    Our trading system operates with specific strategies that include risk management protocols. 
                    Please review our complete Terms & Conditions for detailed information about system stability, 
                    risk factors, and investment policies.
                </div>
                <div style="margin-bottom: 10px;">
                    <a href="https://sites.google.com/view/quantum-pred-terms-conditions/home" 
                       target="_blank" 
                       class="terms-link"
                       rel="noopener noreferrer">
                        <i class="fas fa-external-link-alt"></i>
                        Click here to read complete Terms & Conditions
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a close button that works with Streamlit
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button("✅ I Understand - Close Terms Message", key="close_terms_btn", use_container_width=True):
                    st.session_state.show_terms_popup = False
                    st.rerun()
            
            st.markdown("---")  # Add a separator
        
        # Welcome header with animation
        st.markdown(f"<h6 class='main-header'>Hello, {metrics['name']}!</h6>", unsafe_allow_html=True)
        
        # Profit celebration animation
        if metrics['total_profit'] > 0:
            st.balloons()
            st.markdown("""<div class='success-message'>
                <div class='stAlert' style='background-color: #d4edda; color: #155724; padding: 1rem; border-radius: 5px;'>
                    🎉 Great! You're making positive profits!
                </div>
            </div>""", unsafe_allow_html=True)
        
        # Get platform charges data early to check for pending amounts
        charges_data = get_user_platform_charges_data(metrics['user_id'], data)
        total_pending = 0
        if not charges_data.empty and 'Pending_Amt' in charges_data.columns:
            total_pending = charges_data['Pending_Amt'].sum()
        
        # SIMPLE BANNER APPROACH - Show a prominent banner at the top
        if total_pending > 0 and st.session_state.show_popup:
            st.markdown(f"""
            <div class="pending-banner">
                <div class="pending-banner-content">
                    <div class="pending-banner-title">
                        <i class="fas fa-exclamation-triangle"></i>
                        ⚠️ PLATFORM CHARGES PENDING!
                    </div>
                    <div class="pending-banner-message">
                        You have <span class="highlight-text">₹{total_pending:,.2f}</span> in Platform Charges Pending Amount. 
                        Please pay it at your earliest convenience. If you don't wish to pay? No problem. 
                        Just ignore this message. Charges can be adjusted into your daily profit.
                    </div>
                </div>
                <div class="pending-banner-amount">₹{total_pending:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a close button that works with Streamlit
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button("✅ I Understand - Close This Message", key="close_banner_btn", use_container_width=True):
                    st.session_state.show_popup = False
                    st.rerun()
            
            st.markdown("---")  # Add a separator
        
        # Key Metrics in columns - With Light Red Heading
        st.markdown('<div class="light-red-heading">📈 Investment Overview</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <h4>Your Total Investment</h4>
                <h2>₹{int(metrics['total_investment']):,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            profit_class = "profit-positive" if metrics['total_profit'] >= 0 else "profit-negative"
            st.markdown(f"""
            <div class='metric-card'>
                <h4>Your Total Profit</h4>
                <h2 class='{profit_class}'>₹{metrics['total_profit']:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            roi_class = "profit-positive" if metrics['roi'] >= 0 else "profit-negative"
            st.markdown(f"""
            <div class='metric-card'>
                <h4>ROI</h4>
                <h2 class='{roi_class}'>{metrics['roi']:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='metric-card'>
                <h4>Expected Profit For Next 30 Days</h4>
                <h2>₹{metrics['expected_monthly']:,.2f}</h2>
                <small>Based on daily avg: ₹{metrics['avg_daily_profit']:.2f}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Investment vs Profit Chart - Candle Type Bars (NEW ADDITION)
        st.markdown('<div class="light-red-heading">💹 Investment vs Profit Analysis</div>', unsafe_allow_html=True)
        
        # Add toggle for viewing all users vs current user only
        col1, col2 = st.columns([3, 1])
        with col1:
            view_option = st.radio(
                "View:",
                ["Your Data Only", "Compare with Other Investors"],
                horizontal=True,
                label_visibility="collapsed"
            )
        
        # Create chart based on selection
        chart_type = "current" if view_option == "Your Data Only" else "all"
        profit_chart = create_investment_vs_profit_chart(
            data, 
            selected_user if view_option == "Your Data Only" else None
        )
        
        if profit_chart:
            # Wrap in transparent container
            st.markdown("<div class='plotly-container'>", unsafe_allow_html=True)
            st.plotly_chart(profit_chart, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # REMOVED: ROI insights section below the chart (as requested)
            # Just show tip for comparison view
            if view_option == "Compare with Other Investors":
                st.info("💡 **Tip:** Compare your investment performance with other investors. Hover over bars to see detailed metrics.")
        else:
            st.info("No data available for the investment vs profit chart.")
        
        # Company Profit Trend and Company Investment vs Profit
        st.markdown('<div class="light-red-heading">📊 Company Performance</div>', unsafe_allow_html=True)
        
        # Company Profit Graph
        profit_fig = create_company_profit_graph(data)
        if profit_fig:
            # Wrap plotly chart in a transparent container
            st.markdown("<div class='plotly-container'>", unsafe_allow_html=True)
            st.plotly_chart(profit_fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No profit data available for graph.")
        
        # NEW: Company Investment vs Profit Candle Chart
        company_chart = create_company_investment_vs_profit_chart(data)
        if company_chart:
            st.markdown("<div class='plotly-container'>", unsafe_allow_html=True)
            st.plotly_chart(company_chart, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No data available for company investment vs profit chart.")
        
        # Filtered Data Table
        st.markdown('<div class="light-red-heading">📋 Your Profit Details (Filtered Data)</div>', unsafe_allow_html=True)
        
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
                # Animated counter for total profit
                placeholder = st.empty()
                for i in range(0, int(total_profit_filtered) + 1, max(1, int(total_profit_filtered/20))):
                    placeholder.metric(f"Total Profit ({date_range[0]} to {date_range[1]})", 
                                     f"₹{i:,.2f}")
                    time.sleep(0.02)
                placeholder.metric(f"Total Profit ({date_range[0]} to {date_range[1]})", 
                                 f"₹{total_profit_filtered:,.2f}")
            
            with col2:
                st.metric(f"Average Daily Profit", 
                         f"₹{avg_daily_filtered:,.2f}")
            
            # Display the table with fade-in animation
            st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
            
            # Update display columns to include Total_Profit AND Remarks
            display_cols = ['Date', 'Invest_Amount', 'Company_Total_Invest', 'Profit', 'Total_Profit', 'Payment', 'Remarks']
            # Filter to only include columns that exist in the dataframe
            display_cols = [col for col in display_cols if col in filtered_data.columns]
            
            # Simple dataframe display with Remarks column
            st.dataframe(
                filtered_data[display_cols].rename(columns={
                    'Date': 'Date',
                    'Invest_Amount': 'Your Investment (₹)',
                    'Company_Total_Invest': 'Company Total Investment (₹)',
                    'Profit': 'Your Profit With Tax(₹)',
                    'Total_Profit': 'Company Profit (₹)',
                    'Payment': 'Payment Status',
                    'Remarks': 'Remarks'
                }),
                use_container_width=True,
                hide_index=True
            )
            st.markdown("</div>", unsafe_allow_html=True)
            
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
        
        # UPDATED: Changed section title from "Your Investment History" to "Your Main Investment History"
        st.markdown('<div class="light-red-heading">💰 Your Main Investment History</div>', unsafe_allow_html=True)
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
        
        # NEW SECTION: Re-Investment Details
        st.markdown('<div class="light-red-heading">🔄 Your Re-Investment Details</div>', unsafe_allow_html=True)
        
        # Get re-investment data
        reinvest_data = get_user_reinvestment_data(metrics['user_id'], data)
        
        if not reinvest_data.empty:
            # Display the re-investment table
            # Define column renaming for better display
            column_rename = {
                'Re-Invest_ID': 'Request ID',
                'Requested_Amount': 'Requested Amount',
                'Total_Added_Amount': 'Till Now Added Amount',
                'Pending_Amount_To_Be_Add': 'Still Pending Amount To Add',
                'Applied_To_Main_Investment_Status': 'Updated To Main Investment'
            }
            
            # Only rename columns that exist in the data
            rename_dict = {col: column_rename[col] for col in reinvest_data.columns if col in column_rename}
            
            # Format the display dataframe
            display_df = reinvest_data.rename(columns=rename_dict)
            
            # Format currency columns with ₹ symbol
            currency_columns = ['Requested Amount', 'Till Now Added Amount', 'Still Pending Amount To Add']
            for col in currency_columns:
                if col in display_df.columns:
                    display_df[col] = display_df[col].apply(lambda x: f'₹{x:,.2f}' if pd.notna(x) else '₹0.00')
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Download button for re-investment data (keep original format for download)
            csv_reinvest = reinvest_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Re-Investment Data",
                data=csv_reinvest,
                file_name=f"{metrics['user_id']}_reinvestment_data.csv",
                mime="text/csv",
            )
        else:
            st.info("No re-investment records found.")
        
        # UPDATED: Platform Charges Status - SIMPLE VERSION like Re-Investment
        st.markdown('<div class="bright-red-heading">⚠️ Platform Charges Status</div>', unsafe_allow_html=True)
        
        # Check if popup should be shown for the first time (for users with pending)
        if total_pending > 0 and 'popup_shown' not in st.session_state:
            st.session_state.show_popup = True
            st.session_state.popup_shown = True
        
        if not charges_data.empty:
            # Display the platform charges table
            # Define column renaming as specified
            column_rename = {
                'Charge_ID': 'Charge ID',
                'Reason_For_Charge': 'Reason',
                'Charge_Per_Head': 'Charge Per Person',
                'Paid_Amt': 'Paid',
                'Pending_Amt': 'Pending'
            }
            
            # Only rename columns that exist in the data
            rename_dict = {col: column_rename[col] for col in charges_data.columns if col in column_rename}
            
            # Format the display dataframe
            display_df = charges_data.rename(columns=rename_dict)
            
            # Format currency columns with ₹ symbol
            currency_columns = ['Charge Per Person', 'Paid', 'Pending']
            for col in currency_columns:
                if col in display_df.columns:
                    display_df[col] = display_df[col].apply(lambda x: f'₹{x:,.2f}' if pd.notna(x) else '₹0.00')
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Show total pending amount
            st.warning(f"**Total Pending Amount: ₹{total_pending:,.2f}**")
            
            # Download button for platform charges data
            csv_charges = charges_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Platform Charges Data",
                data=csv_charges,
                file_name=f"{metrics['user_id']}_platform_charges.csv",
                mime="text/csv",
            )
        else:
            st.success("✅ No platform charges found for your account!")
        
        # Additional Insights - With Light Red Heading
        st.markdown('<div class="light-red-heading">📊 Additional Insights</div>', unsafe_allow_html=True)
        
        # Get the Daily_Report data
        daily_report_df = data.get('Daily_Report', pd.DataFrame())
        
        # Calculate total company profit CORRECTLY (UNIQUE DAILY TOTALS)
        total_company_profit = 0
        if not daily_report_df.empty:
            # Ensure Date column is datetime
            daily_report_df['Date'] = pd.to_datetime(daily_report_df['Date'])
            
            # Try to find Total_Profit column
            profit_column = None
            possible_column_names = ['Total_Profit', 'Total Profit', 'TotalProfit', 'total_profit']
            
            for col in possible_column_names:
                if col in daily_report_df.columns:
                    profit_column = col
                    break
            
            if profit_column:
                # Get unique daily Total_Profit values (take first entry per date)
                unique_daily = daily_report_df.drop_duplicates(subset=['Date'], keep='first')
                total_company_profit = unique_daily[profit_column].sum()
            elif 'Profit' in daily_report_df.columns:
                # Fallback: Group by Date and sum Profit column
                daily_totals = daily_report_df.groupby('Date')['Profit'].sum().reset_index()
                total_company_profit = daily_totals['Profit'].sum()
            else:
                total_company_profit = 0
        else:
            total_company_profit = 0
        
        # Company total investment
        company_total = investor_df['Total_Invested_Amount'].sum() if not investor_df.empty else 0
        
        # Display in 3 columns EXACTLY like the others
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Company Investment", f"₹{company_total:,.2f}")
        
        with col2:
            total_investors = len(investor_df)
            st.metric("Total Investors", total_investors)
        
        with col3:
            st.metric("Total Company Profit", f"₹{total_company_profit:,.2f}")
            # REMOVED: The calculation text as requested
    
    else:
        st.error("Could not load user metrics. Please try again.")
    
    # Add Page Links Footer at the very bottom
    st.markdown("""
    <div class="page-links-footer">
        <div class="page-links-container">
            <!-- Our Live Server Link -->
            <a href="https://t.me/RajputhQuantumPredictions" 
               target="_blank" 
               class="page-link-item"
               rel="noopener noreferrer">
                <i class="fab fa-telegram"></i>
                Our Live Server
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()