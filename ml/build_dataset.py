import pandas as pd
import os
from ml.feature_builder import extract_features_from_log
from tradeguard.data_loader import load_csv, clean_trade_data, add_derived_columns

def process_trader_logs(log_folder="data/traders/"):
    rows = []
    for file in os.listdir(log_folder):
        if file.endswith(".csv"):
            path = os.path.join(log_folder, file)
            df = load_csv(path)
            df = clean_trade_data(df)
            df = add_derived_columns(df)
            features = extract_features_from_log(df)
            features["trader_id"] = file.replace(".csv", "")
            rows.append(features)

    return pd.DataFrame(rows)
