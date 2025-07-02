import pandas as pd
from tradeguard.bias_rules import detect_fomo_behavior, detect_loss_aversion, detect_overtrading


def extract_features_from_log(df: pd.DataFrame) -> dict:
    features = {}

    loss_result = detect_loss_aversion(df)
    features["loss_aversion_score"] = loss_result["score"] or 0

    overtrade_result = detect_overtrading(df)
    features["overtrading_score"] = overtrade_result["score"] or 0

    fomo_result = detect_fomo_behavior(df)
    features["fomo_trade_ratio"] = fomo_result["fomo_trade_ratio"] or 0

    features["num_trades"] = len(df)
    features["avg_trade_size"] = df["quantity"].mean()
    features["symbol_count"] = df["symbol"].nunique()

    holding_times = loss_result.get("holding_times", [])
    features["avg_holding_time"] = sum(holding_times) / len(holding_times) if holding_times else 0


    flag_count = int(loss_result["flag"]) + int(overtrade_result["flag"]) + int(fomo_result["flag"])
    features["bias_flag_count"] = flag_count

    print("📦 Extracted features:", features)
    return features
