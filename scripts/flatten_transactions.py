import os
import json
import pandas as pd
from tqdm import tqdm

INPUT_DIR = "data/raw"
OUTPUT_FILE = "data/flattened_transactions.csv"

def flatten_transactions():
    rows = []
    files = os.listdir(INPUT_DIR)

    print("🔄 Flattening JSON files...")
    for filename in tqdm(files):
        if not filename.endswith(".json"):
            continue

        try:
            with open(os.path.join(INPUT_DIR, filename), "r") as f:
                data = json.load(f)
        except Exception:
            print(f"⚠️ Skipped corrupted JSON: {filename}")
            continue

        wallet_address = filename.replace(".json", "")
        for tx in data.get("data", {}).get("items", []):
            log_events = tx.get("log_events") or []
            tx_type = "unknown"
            if isinstance(log_events, list) and log_events:
                decoded = log_events[0].get("decoded", {})
                tx_type = decoded.get("name", "unknown") if decoded else "unknown"

            row = {
                "wallet_address": wallet_address,
                "tx_hash": tx.get("tx_hash"),
                "value": tx.get("value", 0),
                "gas_offered": tx.get("gas_offered", 0),
                "gas_spent": tx.get("gas_spent", 0),
                "successful": tx.get("successful", True),
                "tx_type": tx_type
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Flattened data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    flatten_transactions()
