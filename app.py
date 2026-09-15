import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="XAU/USD Bot Dashboard", page_icon="🤖", layout="wide")

st.title("🤖 XAU/USD AI Trading Bot Dashboard")
st.markdown("**London & New York Session | SMC + XGBoost**")

# Set up paths
base_path = os.path.dirname(__file__)
trades_file = os.path.join(base_path, "backtest_trades.csv")
features_file = os.path.join(base_path, "feature_importance.csv")

# Load Data
@st.cache_data
def load_data():
    trades_df = pd.DataFrame()
    features_df = pd.DataFrame()
    
    if os.path.exists(trades_file):
        trades_df = pd.read_csv(trades_file)
        trades_df['Entry_Time'] = pd.to_datetime(trades_df['Entry_Time'])
        trades_df['Exit_Time'] = pd.to_datetime(trades_df['Exit_Time'])
        
    if os.path.exists(features_file):
        features_df = pd.read_csv(features_file)
        
    return trades_df, features_df

trades_df, features_df = load_data()

if trades_df.empty:
    st.warning("No backtest data found. Please run a backtest first to generate backtest_trades.csv.")
else:
    # --- KPI METRICS ---
    total_trades = len(trades_df)
    winning_trades = len(trades_df[trades_df['Profit_Loss'] > 0])
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    total_profit = trades_df['Profit_Loss'].sum()
    max_drawdown = trades_df['Drawdown'].max()
    final_equity = trades_df['Cumulative_Equity'].iloc[-1]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Trades", f"{total_trades}")
    col2.metric("Win Rate", f"{win_rate:.2f}%")
    col3.metric("Total Profit", f"${total_profit:.2f}")
    col4.metric("Max Drawdown", f"{max_drawdown:.2f}%")
    col5.metric("Final Equity", f"${final_equity:.2f}")
    
    st.markdown("---")
    
    # --- EQUITY CURVE ---
    st.subheader("📈 Equity Curve")
    fig_equity = px.line(trades_df, x='Exit_Time', y='Cumulative_Equity', 
                         title='Cumulative Equity Over Time',
                         labels={'Exit_Time': 'Date', 'Cumulative_Equity': 'Equity ($)'})
    fig_equity.update_layout(template="plotly_dark", hovermode="x unified")
    st.plotly_chart(fig_equity, use_container_width=True)
    
    # --- TRADE DISTRIBUTION ---
    st.subheader("⚖️ Profit & Loss Distribution")
    fig_dist = px.histogram(trades_df, x='Profit_Loss', nbins=50, 
                            title='P&L Distribution',
                            color_discrete_sequence=['indianred'])
    fig_dist.update_layout(template="plotly_dark")
    st.plotly_chart(fig_dist, use_container_width=True)
    
    # --- FEATURE IMPORTANCE ---
    if not features_df.empty:
        st.markdown("---")
        st.subheader("🧠 XGBoost Feature Importance")
        features_df_sorted = features_df.sort_values(by="Importance_Score", ascending=True).tail(15)
        fig_features = px.bar(features_df_sorted, x='Importance_Score', y='Feature_Name', orientation='h',
                              title='Top 15 ML Features', color='Importance_Score', color_continuous_scale='viridis')
        fig_features.update_layout(template="plotly_dark")
        st.plotly_chart(fig_features, use_container_width=True)

    # --- RAW DATA TABLE ---
    st.markdown("---")
    st.subheader("📋 Recent Trades Log")
    st.dataframe(trades_df.tail(20).sort_values(by="Exit_Time", ascending=False), use_container_width=True)
