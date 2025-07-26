import pandas as pd
import os

INPUT_FILE = "data/flattened_transactions.csv"
OUTPUT_FILE = "data/wallet_features.csv"

def extract_features():
    df = pd.read_csv(INPUT_FILE)

    # Ensure proper types
    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
    df["gas_spent"] = pd.to_numeric(df["gas_spent"], errors="coerce").fillna(0)
    df["successful"] = df["successful"].astype(bool)

    features = df.groupby("wallet_address").agg(
        total_value=("value", "sum"),
        tx_count=("tx_hash", "count"),
        total_gas=("gas_spent", "sum"),
        success_rate=("successful", "mean"),
        unique_tx_types=("tx_type", pd.Series.nunique)
    ).reset_index()

    features.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Features saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_features()

