"""
from engine.data_loader import load_csv, clean_trade_data, add_derived_columns
from engine.bias_rules import detect_overtrading, detect_fomo_behavior, detect_loss_aversion

df = load_csv("data/fomo_trigger_sample.csv")
df = clean_trade_data(df)
df = add_derived_columns(df)


loss_aversion_result = detect_loss_aversion(df)
if loss_aversion_result["avg_win_hold_min"] != None:
    print(f"🏆 Avg holding time for winners: {loss_aversion_result['avg_win_hold_min']} min")
    print(f"💔 Avg holding time for losers: {loss_aversion_result['avg_loss_hold_min']} min")
    print(f"📊 Loss aversion score: {loss_aversion_result['score']}")
    if loss_aversion_result['flag']:
        print("⚠️  You may be showing signs of loss aversion behavior.")
    else:
        print("✅  Your trading behavior does not indicate loss aversion.")
else:
    print("No completed positions found or no winners in the data.")

overtrading_result = detect_overtrading(df)

print(f"📈 Overtrading Score: {overtrading_result['score']}")
if overtrading_result['flag']:
    print("⚠️ You may be overtrading. Consider reviewing your trading strategy.")
else: 
    print("✅ Your trading frequency is within a healthy range.")

fomo_result = detect_fomo_behavior(df)
print(fomo_result)
"""

from ml.build_dataset import process_trader_logs
from ml.cluster import run_kmeans
from ml.pca import apply_pca
from ml.preprocess import scale_features

feature_df = process_trader_logs()
X_scaled, scaler = scale_features(feature_df)
X_pca, pca = apply_pca(X_scaled)
labels, model, silhouette = run_kmeans(X_pca, n_clusters=4)
feature_df["cluster"] = labels

print(f"✅ Clustering complete! Silhouette score: {silhouette:.2f}")
print(feature_df[["trader_id", "cluster"]])

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(X_pca.iloc[:, 0], X_pca.iloc[:, 1], c=labels, cmap="viridis", s=100)


for i, trader in enumerate(feature_df["trader_id"]):
    plt.text(X_pca.iloc[i, 0]+0.02, X_pca.iloc[i, 1], trader, fontsize=9)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title(f"K-Means Clusters (k=4), Silhouette = {silhouette:.2f}")
plt.grid(True)
plt.show()
