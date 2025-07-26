# Zeru DeFi Risk Score – Compound V2 Wallet Scoring

This project evaluates the DeFi risk of 100 wallet addresses interacting with the Compound V2 protocol using transaction data from the Covalent API. The final output assigns each wallet a risk score between **0–1000**, where a higher score indicates lower risk.

---

## 📁 Project Structure

```
zeru-defi-risk-score/
│
├── data/
│   └── raw/                  # Raw JSONs from Covalent API (excluded from Git – must be regenerated)
│
├── output/
│   └── scores.csv                   # Final output: wallet_id, score
│
├── scripts/
│   ├── fetch_transactions.py        # Download Compound V2 txns via Covalent
│   ├── flatten_transactions.py      # Convert JSON to flat CSV
│   ├── feature_engineering.py       # Create features from flattened data
│   └── scoring.py                   # Compute risk score
│
└── wallet.csv                       # Input list of 103 wallet addresses

 
```

---

## ⚙️ Setup Instructions

1. **Clone this repository**

   ```bash
   git clone <repo-url>
   cd zeru-defi-risk-score
   ```

2. **Install required packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Covalent API key**

   In `scripts/fetch_transactions.py`, replace:

   ```python
   API_KEY = "your_covalent_api_key"
   ```

4. **Note on Raw Data Folder**

   > 🔹 The `data/raw/` folder (containing raw JSONs) is excluded from GitHub due to large file sizes.
   > To populate it, run the transaction fetch script after adding your API key:

   ```bash
   python scripts/fetch_transactions.py
   ```

---


## 🚀 Run Pipeline

You can run each stage step-by-step:

### 1. Fetch Transactions

```bash
python scripts/fetch_transactions.py
```

Fetches Compound V2 transactions from Covalent API for all wallets.

### 2. Flatten JSON to CSV

```bash
python scripts/flatten_transactions.py
```

Parses the raw JSONs into a single `flattened_transactions.csv` file.

### 3. Generate Features

```bash
python scripts/feature_engineering.py
```

Creates a `features.csv` containing relevant metrics for scoring.

### 4. Score Wallets

```bash
python scripts/scoring.py
```

Generates `scores.csv` with risk score between 0–1000 for each wallet.

---

## 🧠 Risk Score Logic

Each wallet is scored using engineered features such as:

* Number of Compound V2 interactions
* Type of actions (deposit, borrow, repay, etc.)
* Total value transferred
* Activity spread across time
* Number of unique tokens used

The score is normalized on a scale from **0 (highest risk)** to **1000 (lowest risk)**.

---

## 📝 Output

Final file:
`wallet_scores.csv`

Format:

```
wallet_address,score
0x1234abcd..., 782
0xabcd1234..., 455
...
```

---

## 📦 Dependencies

```txt
pandas
requests
tqdm
scikit-learn
```

Install via:

```bash
pip install -r requirements.txt
```

---

## 📩 Notes

* The scoring model is linear and rule-based for transparency.
* You can easily extend this to other protocols by modifying `fetch_transactions.py` and adjusting feature logic.
