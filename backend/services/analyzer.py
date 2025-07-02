
import pandas as pd
import joblib
from tradeguard.data_loader import load_csv, clean_trade_data, add_derived_columns
from tradeguard.bias_rules import detect_loss_aversion, detect_overtrading, detect_fomo_behavior
from ml.feature_builder import extract_features_from_log


def analyze_trades(file_path: str):
    
    df = load_csv(file_path)
    df = clean_trade_data(df)
    df = add_derived_columns(df)

    
    features = extract_features_from_log(df)  

    
    feature_df = pd.DataFrame([features])

    
    scaler = joblib.load("ml/models/scaler.pkl")
    pca = joblib.load("ml/models/pca.pkl")
    kmeans = joblib.load("ml/models/kmeans.pkl")

    X_scaled = scaler.transform(feature_df)
    X_pca = pca.transform(X_scaled)

    clusters = kmeans.predict(X_pca)
    user_cluster = int(clusters[0])
    user_coords = X_pca[0].tolist()

    return {
    "features": features,
    "cluster": user_cluster,
    "coordinates": user_coords,
    "all_coords": X_pca.tolist(),
    "all_clusters": clusters.tolist()
}

