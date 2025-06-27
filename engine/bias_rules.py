import pandas as pd
from datetime import timedelta

def detect_loss_aversion(df: pd.DataFrame) -> dict:
    df = df.sort_values(by="timestamp")
    positions = []

    for symbol in df["symbol"].unique():
        symbol_df = df[df["symbol"] == symbol]
        buys = []

        for _, row in symbol_df.iterrows():
            if row["side"] == "buy":
                buys.append(row.to_dict())
            elif row["side"] == "sell":
                qty_to_match = row["quantity"]

                while qty_to_match > 0 and buys:
                    buy_row = buys[0]
                    match_qty = min(buy_row["quantity"], qty_to_match)

                    entry_time = buy_row["timestamp"]
                    exit_time  = row["timestamp"]
                    holding_min = (exit_time - entry_time).total_seconds() / 60.0
                    pnl = (row["price"] - buy_row["price"]) * match_qty

                    positions.append(
                        {
                            "symbol": symbol,
                            "entry_time": entry_time,
                            "exit_time": exit_time,
                            "holding_time_min": holding_min,
                            "pnl": pnl,
                            "qty": match_qty,
                        }
                    )

                    buy_row["quantity"] -= match_qty
                    qty_to_match       -= match_qty

                    if buy_row["quantity"] <= 0:
                        buys.pop(0)

    if not positions:
        return {
            "message": "No completed positions found",
            "avg_win_hold_min": None,
            "avg_loss_hold_min": None,
            "score": None,
            "flag": False,
        }

    pos_df  = pd.DataFrame(positions)
    winners = pos_df[pos_df["pnl"] > 0]
    losers  = pos_df[pos_df["pnl"] <= 0]

    avg_win_hold  = winners["holding_time_min"].mean() if not winners.empty else 0
    avg_loss_hold = losers["holding_time_min"].mean()  if not losers.empty  else 0

    score = (avg_loss_hold / avg_win_hold) if avg_win_hold > 0 else None
    flag  = (score is not None) and (score > 1.5)

    return {
        "avg_win_hold_min": round(avg_win_hold, 2)  if avg_win_hold  else 0,
        "avg_loss_hold_min": round(avg_loss_hold, 2) if avg_loss_hold else 0,
        "score": round(score, 2) if score is not None else None,
        "flag": flag,
    }


def detect_overtrading(df: pd.DataFrame) -> dict:
    pass

def detect_fomo_behavior(df: pd.DataFrame) -> dict:
    pass
