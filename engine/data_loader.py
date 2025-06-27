import pandas as pd

def load_csv(source) -> pd.DataFrame:
    return pd.read_csv(source, parse_dates=['timestamp'])

def clean_trade_data(df : pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip()
    df['side'] = df['side'].str.lower()
    df['symbol'] = df['symbol'].str.upper()
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df.dropna(subset=['timestamp', 'side', 'symbol', 'price', 'quantity'], inplace=True)
    df = df[(df['price'] > 0) & (df['quantity'] > 0)]
    df = df[df['side'].isin(['buy', 'sell'])]
    df = df.reset_index(drop=True)
    df = df.sort_values(by="timestamp")
    return df

def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    df['total_value'] = df['price'] * df['quantity']
    df['side_numeric'] = df['side'].map({'buy': 1, 'sell': -1})
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['hour'] = df['timestamp'].dt.hour
    df['trade_id'] = df.index
    return df
