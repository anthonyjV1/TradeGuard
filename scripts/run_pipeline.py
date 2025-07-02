import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pandas as pd
import joblib
from ml.build_dataset import process_trader_logs
from ml.preprocess import scale_features
from ml.pca import apply_pca
from ml.cluster import run_kmeans

# Step 1: Build dataset from all trader logs
print("🔧 Processing trader logs...")
df = process_trader_logs()

# Step 2: Preprocess (scale)
print("🔧 Scaling features...")
X_scaled, scaler = scale_features(df)

# Step 3: PCA
print("🔧 Applying PCA...")
X_pca, pca = apply_pca(X_scaled)

# Step 4: K-means clustering
print("🔧 Running K-means...")
labels, kmeans, silhouette = run_kmeans(X_pca, n_clusters=4)

# Step 5: Save fitted models
joblib.dump(scaler, "ml/models/scaler.pkl")
joblib.dump(pca, "ml/models/pca.pkl")
joblib.dump(kmeans, "ml/models/kmeans.pkl")

# Optional: Save labeled DataFrame
df["cluster"] = labels
df.to_csv("ml/models/clustered_traders.csv", index=False)

print(f"✅ Training complete. Silhouette Score: {silhouette:.2f}")
