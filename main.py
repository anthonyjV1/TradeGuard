from engine.data_loader import load_csv, clean_trade_data, add_derived_columns
from engine.bias_rules import detect_overtrading, detect_fomo_behavior, detect_loss_aversion

df = load_csv("data/overtrading_sample.csv")
df = clean_trade_data(df)
df = add_derived_columns(df)

"""
result = detect_loss_aversion(df)
if result["avg_win_hold_min"] > 0:
    print(f"🏆 Avg holding time for winners: {result['avg_win_hold_min']} min")
    print(f"💔 Avg holding time for losers: {result['avg_loss_hold_min']} min")
    print(f"📊 Loss aversion score: {result['score']}")
    if result['flag']:
        print("⚠️  You may be showing signs of loss aversion behavior.")
    else:
        print("✅  Your trading behavior does not indicate loss aversion.")
else:
    print("No completed positions found or no winners in the data.")

"""
result = detect_overtrading(df)
print(result)