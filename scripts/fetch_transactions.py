# fetch_transactions.py
import os
import requests
import time
import json
import pandas as pd
from utils import COVALENT_API_KEY, CHAIN_ID

def fetch_transactions():
    os.makedirs("data/raw", exist_ok=True)
    df = pd.read_csv("wallets.csv")  # Your file with 100 wallet addresses
    wallets = df["wallet_address"].tolist()

    for i, wallet in enumerate(wallets):
        print(f"🔁 Fetching {i+1}/{len(wallets)}: {wallet}")
        url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet}/transactions_v2/?key={COVALENT_API_KEY}"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                with open(f"data/raw/{wallet}.json", "w") as f:
                    json.dump(resp.json(), f)
            else:
                print(f"❌ Failed for {wallet} — {resp.status_code}")
        except Exception as e:
            print(f"⚠️ Error for {wallet}: {str(e)}")
        time.sleep(0.5)  # Avoid rate limit

if __name__ == "__main__":
    fetch_transactions()
