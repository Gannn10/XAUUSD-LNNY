import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Quantitative Strategy Analytics | XAU/USD",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (INSTITUTIONAL VIBE) ---
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .metric-container {
        background-color: #1e2129;
        border-radius: 5px;
        padding: 15px;
        border-left: 4px solid #2e9cca;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-title {
        font-size: 0.9rem;
        color: #a0aab2;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 1.8rem;
        color: #ffffff;
        font-weight: 700;
    }
    .metric-positive {
        color: #00e676 !important;
    }
    .metric-negative {
        color: #ff5252 !important;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    trades_file = os.path.join(base_path, "backtest_trades.csv")
    features_file = os.path.join(base_path, "feature_importance.csv")
    
    trades_df = pd.DataFrame()
    features_df = pd.DataFrame()
    
    if os.path.exists(trades_file):
        trades_df = pd.read_csv(trades_file)
        trades_df['Entry_Time'] = pd.to_datetime(trades_df['Entry_Time'])
        trades_df['Exit_Time'] = pd.to_datetime(trades_df['Exit_Time'])
        trades_df['Trade_Duration'] = (trades_df['Exit_Time'] - trades_df['Entry_Time']).dt.total_seconds() / 3600.0 # in hours
        trades_df['Date'] = trades_df['Exit_Time'].dt.date
        
    if os.path.exists(features_file):
        features_df = pd.read_csv(features_file)
        
    return trades_df, features_df

trades_df, features_df = load_data()

if trades_df.empty:
    st.error("Quantitative Backtest Data Not Found. Please ensure backtest_trades.csv exists.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.markdown("## ⚙️ Strategy Filters")
st.sidebar.markdown("---")

min_date = trades_df['Date'].min()
max_date = trades_df['Date'].max()

date_range = st.sidebar.date_input(
    "Evaluation Period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

trade_types = st.sidebar.multiselect(
    "Trade Direction",
    options=trades_df['Type'].unique(),
    default=trades_df['Type'].unique()
)

# Apply Filters
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = trades_df[(trades_df['Date'] >= start_date) & 
                            (trades_df['Date'] <= end_date) & 
                            (trades_df['Type'].isin(trade_types))].copy()
else:
    filtered_df = trades_df.copy()

if filtered_df.empty:
    st.warning("No trades match the selected filters.")
    st.stop()

# --- CALCULATE QUANTS METRICS ---
initial_equity = 10000.0 # From README
final_equity = filtered_df['Cumulative_Equity'].iloc[-1]
total_return_pct = ((final_equity - initial_equity) / initial_equity) * 100

total_trades = len(filtered_df)
winning_trades = filtered_df[filtered_df['Profit_Loss'] > 0]
losing_trades = filtered_df[filtered_df['Profit_Loss'] <= 0]

win_rate = (len(winning_trades) / total_trades) * 100 if total_trades > 0 else 0
gross_profit = winning_trades['Profit_Loss'].sum()
gross_loss = abs(losing_trades['Profit_Loss'].sum())
profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')

avg_win = winning_trades['Profit_Loss'].mean() if not winning_trades.empty else 0
avg_loss = losing_trades['Profit_Loss'].mean() if not losing_trades.empty else 0
risk_reward = abs(avg_win / avg_loss) if avg_loss != 0 else 0

max_drawdown = filtered_df['Drawdown'].max()
calmar_ratio = (total_return_pct / max_drawdown) if max_drawdown > 0 else float('inf')

# Daily Returns for Sharpe/Sortino
daily_returns = filtered_df.groupby('Date')['Profit_Loss'].sum()
# Approximate daily return percentage relative to initial equity for standard ratios
daily_ret_pct = daily_returns / initial_equity
mean_daily_ret = daily_ret_pct.mean()
std_daily_ret = daily_ret_pct.std()

sharpe_ratio = (mean_daily_ret / std_daily_ret) * np.sqrt(252) if std_daily_ret > 0 else 0

downside_returns = daily_ret_pct[daily_ret_pct < 0]
downside_std = downside_returns.std()
sortino_ratio = (mean_daily_ret / downside_std) * np.sqrt(252) if downside_std > 0 else 0

# --- HELPER UI COMPONENT ---
def metric_card(title, value, suffix="", is_currency=False, is_positive_good=True, polarity_check=False):
    color_class = ""
    if polarity_check:
        try:
            val_float = float(str(value).replace(',', '').replace('$', '').replace('%', ''))
            if val_float > 0:
                color_class = "metric-positive" if is_positive_good else "metric-negative"
            elif val_float < 0:
                color_class = "metric-negative" if is_positive_good else "metric-positive"
        except:
            pass
            
    val_str = f"${value:,.2f}" if is_currency else f"{value:,.2f}"
    
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">{title}</div>
            <div class="metric-value {color_class}">{val_str}{suffix}</div>
        </div>
    """, unsafe_allow_html=True)


# --- MAIN DASHBOARD ---
st.title("🏛️ Quantitative Strategy Analytics")
st.markdown("<p style='color: #888;'>XAU/USD | SMC + XGBoost Alpha Model</p>", unsafe_allow_html=True)

# 1. TOP METRICS
st.markdown("### Executive Summary")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    metric_card("Net Return", total_return_pct, suffix="%", polarity_check=True)
with col2:
    metric_card("Profit Factor", profit_factor, polarity_check=True)
with col3:
    metric_card("Max Drawdown", max_drawdown, suffix="%", is_positive_good=False, polarity_check=True)
with col4:
    metric_card("Sharpe Ratio", sharpe_ratio, polarity_check=True)
with col5:
    metric_card("Win Rate", win_rate, suffix="%")

st.markdown("<br>", unsafe_allow_html=True)

col6, col7, col8, col9, col10 = st.columns(5)
with col6:
    metric_card("Total Trades", total_trades)
with col7:
    metric_card("Sortino Ratio", sortino_ratio, polarity_check=True)
with col8:
    metric_card("Risk / Reward", risk_reward)
with col9:
    metric_card("Avg Win Trade", avg_win, is_currency=True, polarity_check=True)
with col10:
    metric_card("Avg Loss Trade", avg_loss, is_currency=True, is_positive_good=False, polarity_check=True)

st.markdown("---")

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["📈 Portfolio Performance", "📅 Time & Duration Analysis", "⚖️ Distribution & Risk", "🧠 ML Alpha Drivers"])

# --- TAB 1: PORTFOLIO PERFORMANCE ---
with tab1:
    st.subheader("Equity Curve & Drawdown Profile")
    
    # Create figure with secondary y-axis for Drawdown
    from plotly.subplots import make_subplots
    fig_equity = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add Equity trace
    fig_equity.add_trace(
        go.Scatter(x=filtered_df['Exit_Time'], y=filtered_df['Cumulative_Equity'], 
                   name="Cumulative Equity", fill='tozeroy',
                   line=dict(color='#2e9cca', width=2),
                   fillcolor='rgba(46, 156, 202, 0.1)'),
        secondary_y=False,
    )
    
    # Add Drawdown trace
    fig_equity.add_trace(
        go.Scatter(x=filtered_df['Exit_Time'], y=filtered_df['Drawdown'], 
                   name="Drawdown (%)", fill='tozeroy',
                   line=dict(color='#ff5252', width=1),
                   fillcolor='rgba(255, 82, 82, 0.2)'),
        secondary_y=True,
    )
    
    fig_equity.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        height=500,
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_equity.update_yaxes(title_text="Equity ($)", secondary_y=False)
    fig_equity.update_yaxes(title_text="Drawdown (%)", secondary_y=True, autorange="reversed")
    
    st.plotly_chart(fig_equity, use_container_width=True)

# --- TAB 2: TIME & DURATION ANALYSIS ---
with tab2:
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.subheader("Monthly Return Heatmap (%)")
        
        # Calculate monthly returns
        filtered_df['Month'] = pd.to_datetime(filtered_df['Exit_Time']).dt.month
        filtered_df['Year'] = pd.to_datetime(filtered_df['Exit_Time']).dt.year
        
        monthly_profit = filtered_df.groupby(['Year', 'Month'])['Profit_Loss'].sum().reset_index()
        monthly_profit['Return_Pct'] = (monthly_profit['Profit_Loss'] / initial_equity) * 100
        
        heatmap_data = monthly_profit.pivot(index='Year', columns='Month', values='Return_Pct').fillna(0)
        
        # Month names
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        # Map columns to month names if they exist
        existing_months = [month_names[i-1] for i in heatmap_data.columns]
        
        fig_heat = px.imshow(heatmap_data, 
                             labels=dict(x="Month", y="Year", color="Return (%)"),
                             x=existing_months,
                             color_continuous_scale="RdYlGn",
                             text_auto=".2f",
                             aspect="auto")
        fig_heat.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with col_t2:
        st.subheader("Trade Duration vs. Profit")
        
        fig_scatter = px.scatter(filtered_df, x="Trade_Duration", y="Profit_Loss", 
                                 color="Type", size=abs(filtered_df['Profit_Loss']),
                                 hover_data=['Exit_Time'],
                                 color_discrete_map={'BUY': '#00e676', 'SELL': '#ff5252'},
                                 labels={"Trade_Duration": "Duration (Hours)", "Profit_Loss": "Profit/Loss ($)"})
        fig_scatter.update_layout(template="plotly_dark", height=400)
        # Add zero line
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_scatter, use_container_width=True)

# --- TAB 3: DISTRIBUTION & RISK ---
with tab3:
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.subheader("P&L Distribution (Trade Level)")
        fig_dist = px.histogram(filtered_df, x='Profit_Loss', nbins=60, 
                                color="Type", barmode="stack",
                                color_discrete_map={'BUY': '#00e676', 'SELL': '#ff5252'},
                                title="Distribution of Trade Outcomes")
        fig_dist.update_layout(template="plotly_dark", height=450)
        fig_dist.add_vline(x=0, line_dash="dash", line_color="white")
        st.plotly_chart(fig_dist, use_container_width=True)
        
    with col_d2:
        st.subheader("Win Rate by Direction")
        
        buy_trades = filtered_df[filtered_df['Type'] == 'BUY']
        sell_trades = filtered_df[filtered_df['Type'] == 'SELL']
        
        buy_win = len(buy_trades[buy_trades['Profit_Loss'] > 0]) / len(buy_trades) if len(buy_trades) > 0 else 0
        sell_win = len(sell_trades[sell_trades['Profit_Loss'] > 0]) / len(sell_trades) if len(sell_trades) > 0 else 0
        
        win_data = pd.DataFrame({
            "Direction": ["BUY", "SELL"],
            "Win Rate (%)": [buy_win * 100, sell_win * 100],
            "Count": [len(buy_trades), len(sell_trades)]
        })
        
        fig_bar = px.bar(win_data, x="Direction", y="Win Rate (%)", text="Win Rate (%)",
                         color="Direction", color_discrete_map={'BUY': '#00e676', 'SELL': '#ff5252'},
                         title="Strategy Edge Analysis")
        fig_bar.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig_bar.update_layout(template="plotly_dark", height=450)
        fig_bar.update_yaxes(range=[0, max(win_data['Win Rate (%)']) * 1.2 if not win_data.empty else 100])
        st.plotly_chart(fig_bar, use_container_width=True)

# --- TAB 4: FEATURE IMPORTANCE ---
with tab4:
    st.subheader("Alpha Drivers (XGBoost Feature Importance)")
    if not features_df.empty:
        features_df_sorted = features_df.sort_values(by="Importance_Score", ascending=True).tail(20)
        fig_feat = px.bar(features_df_sorted, x='Importance_Score', y='Feature_Name', orientation='h',
                          color='Importance_Score', color_continuous_scale='Viridis',
                          labels={'Importance_Score': 'Information Gain / Score', 'Feature_Name': 'Alpha Feature'})
        fig_feat.update_layout(template="plotly_dark", height=600)
        st.plotly_chart(fig_feat, use_container_width=True)
    else:
        st.info("Feature importance data is not available.")

# --- RAW DATA EXPANDER ---
with st.expander("🔍 View Raw Trade Logs"):
    st.dataframe(filtered_df[['Entry_Time', 'Exit_Time', 'Type', 'Entry_Price', 'Exit_Price', 'Profit_Loss', 'Cumulative_Equity', 'Drawdown']].sort_values(by="Exit_Time", ascending=False), use_container_width=True)
