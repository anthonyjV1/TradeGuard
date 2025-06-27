import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from engine.data_loader import load_csv, clean_trade_data, add_derived_columns
from engine.bias_rules import detect_loss_aversion

st.set_page_config(page_title="TradeGuard", layout="wide")
st.title("📊 TradeGuard — Behavioral Trading Dashboard")

uploaded_file = st.file_uploader("Upload your trade log (.csv)", type=["csv"])

if uploaded_file:
    df = load_csv(uploaded_file)
    df = clean_trade_data(df)
    df = add_derived_columns(df)

    st.subheader("📄 Cleaned Trade Data")
    st.dataframe(df.head())

    st.subheader("🧠 Behavioral Insights")
    result = detect_loss_aversion(df)
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Hold Time (Winners)", f"{result['avg_win_hold_min']} min")
    col2.metric("Avg Hold Time (Losers)", f"{result['avg_loss_hold_min']} min")
    col3.metric("Loss Aversion Score", result['score'] if result['score'] else "N/A")
    if result['score'] and result['score'] > 2.0:
        st.warning("⚠️ You may be showing signs of **loss aversion** behavior.")
    else:
        st.success("✅ Your trading behavior does not indicate loss aversion.")
        