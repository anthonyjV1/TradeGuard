import pandas as pd
from sklearn.preprocessing import StandardScaler

def scale_features(df: pd.DataFrame, drop_cols = ["trader_id"]):
    X = df.drop(columns=drop_cols)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return pd.DataFrame(X_scaled, columns=X.columns), scaler