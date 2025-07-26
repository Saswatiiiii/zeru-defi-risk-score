import pandas as pd
from sklearn.preprocessing import MinMaxScaler

INPUT_FILE = "data/wallet_features.csv"
OUTPUT_FILE = "output/wallet_scores.csv"

def score_wallets():
    df = pd.read_csv(INPUT_FILE)

    # Ensure numeric types and handle NaNs
    df["total_value"] = pd.to_numeric(df["total_value"], errors="coerce").fillna(0)
    df["tx_count"] = pd.to_numeric(df["tx_count"], errors="coerce").fillna(0)
    df["total_gas"] = pd.to_numeric(df["total_gas"], errors="coerce").fillna(0)
    df["success_rate"] = pd.to_numeric(df["success_rate"], errors="coerce").fillna(0)
    df["unique_tx_types"] = pd.to_numeric(df["unique_tx_types"], errors="coerce").fillna(0)

    # Features to consider in scoring
    features = ["total_value", "tx_count", "total_gas", "success_rate", "unique_tx_types"]

    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df[features]), columns=features)

    # Define scoring weights (adjustable)
    weights = {
        "total_value": 0.25,
        "tx_count": 0.2,
        "total_gas": 0.15,
        "success_rate": 0.2,
        "unique_tx_types": 0.2
    }

    # Compute weighted sum
    df["score"] = (
        df_scaled["total_value"] * weights["total_value"] +
        df_scaled["tx_count"] * weights["tx_count"] +
        df_scaled["total_gas"] * weights["total_gas"] +
        df_scaled["success_rate"] * weights["success_rate"] +
        df_scaled["unique_tx_types"] * weights["unique_tx_types"]
    ) * 1000

    # Final formatting
    result = df[["wallet_address", "score"]]
    result["score"] = result["score"].round().astype(int)
    result.to_csv(OUTPUT_FILE, index=False)

    print(f"✅ Wallet risk scores saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    score_wallets()
