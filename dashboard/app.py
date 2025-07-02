import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="TradeGuard", layout="wide")
st.title("📊 TradeGuard — Behavioral Trading Dashboard")

uploaded_file = st.file_uploader("Upload your trade log (.csv)", type=["csv"])

if uploaded_file:
    st.info("🔄 Sending file to backend for analysis...")

    response = requests.post(
        "http://localhost:8000/analyze",
        files={"file": (uploaded_file.name, uploaded_file, "text/csv")},
    )

    if response.status_code == 200:
        result = response.json()
        features = result["features"]
        coords = result["all_coords"]
        clusters = result["all_clusters"]
        user_coords = result["coordinates"]
        user_cluster = result["cluster"]

        st.success("✅ Analysis complete!")
        st.info(features)

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Avg Hold Time (All)", f"{features['avg_holding_time']} min")
        col2.metric("Loss Aversion Score", features['loss_aversion_score'])
        col3.metric("Overtrading Score", features['overtrading_score'])
        col4.metric("FOMO Score", features['fomo_trade_ratio'])
        col5.metric("Bias Flags", features['bias_flag_count'])

        if features["loss_aversion_score"] > 1.5:
            st.warning("⚠️ You may be showing signs of **loss aversion** behavior.")
        else:
            st.success("✅ Your trading behavior does not indicate loss aversion.")
        if features["overtrading_score"] > 5.0:
            st.warning("⚠️ You may be overtrading. Consider reducing trade frequency.")
        else:
            st.success("✅ Your trading frequency is within normal limits.")
        if features["fomo_trade_ratio"] > 30:
            st.warning("⚠️ High FOMO detected. Consider reducing impulsive trades.")
        else:
            st.success("✅ Your FOMO ratio is within acceptable limits.")

        st.subheader("🧠 ML Engine — Trader Clustering")

        fig, ax = plt.subplots()

        if len(clusters) > 1:
            
            for cluster_id in set(clusters):
                xs = [pt[0] for pt, c in zip(coords, clusters) if c == cluster_id]
                ys = [pt[1] for pt, c in zip(coords, clusters) if c == cluster_id]
                ax.scatter(xs, ys, label=f"Cluster {cluster_id}", alpha=0.4)
        else:
            
            ax.scatter(coords[0][0], coords[0][1], label=f"Cluster {clusters[0]}", alpha=0.7)

        
        ax.scatter(user_coords[0], user_coords[1], color='red', s=120, edgecolors='black', label='You')

        ax.set_xlabel("PCA 1")
        ax.set_ylabel("PCA 2")
        ax.set_title("Trader Behavior Clusters")
        ax.legend()
        st.pyplot(fig)

        st.subheader(f"🧬 You are in Cluster {user_cluster}")

        if user_cluster == 0:
            st.info("🧊 Loss aversion")
        elif user_cluster == 1:
            st.warning("🔥 Aggressive: High overtrading.")
        elif user_cluster == 2:
            st.info("📈 Fomo.")
        else:
            st.write("Cluster profile not yet defined.")
    else:
        st.error("❌ Backend error: " + response.text)
