# 📊 Analysis: Wallet Risk Scoring – Zeru Round 2

## 🔍 Data Collection Method

We collected on-chain transaction data for 100 wallet addresses using the **Covalent API**, which provides detailed decoded transactions across various protocols including **Compound V2**. The following steps were followed:

- Queried the `/v1/{chain_id}/address/{wallet_address}/transactions_v3/` endpoint.
- Filtered and retained only Compound-related transactions.
- Stored responses in the `data/raw/` directory in JSON format.
- Added retry handling and sleep intervals to avoid rate limits and ensure reliability.

## 🧹 Data Preprocessing & Flattening

Each raw transaction JSON file was parsed and flattened into a structured tabular format with the following attributes:

- `wallet_address`
- `txn_type` (e.g., supply, borrow, repay, liquidate, redeem)
- `token_symbol`
- `token_amount`
- `usd_value`
- `timestamp`

We aggregated this transactional data per wallet to compute behavioral and financial activity summaries.

## 🛠 Feature Engineering

For each wallet, we engineered the following features:

| Feature               | Description                                       |
|-----------------------|---------------------------------------------------|
| `num_transactions`    | Total number of Compound protocol interactions    |
| `total_supply_usd`    | Total USD value of all supplied assets            |
| `total_borrow_usd`    | Total USD value borrowed                          |
| `borrow_to_supply_ratio` | Risk metric: borrow/supply ratio               |
| `num_liquidations`    | Count of times wallet was liquidated              |
| `avg_txn_value`       | Average USD value per transaction                 |
| `unique_tokens`       | Number of distinct tokens used                    |
| `activity_days`       | Days active with transactions                     |
| `last_active_days_ago`| Days since last activity                          |
| `has_borrowed`        | Binary indicator (1 if borrowed, else 0)          |
| `has_supplied`        | Binary indicator (1 if supplied, else 0)          |

All features were scaled using **MinMaxScaler** to bring them to a uniform [0, 1] range before scoring.


## 🧮 Scoring Approach

Weights were heuristically chosen to emphasize:

- **Negative risk indicators** (e.g., high borrow-to-supply ratio, liquidations)
- **Positive indicators** (e.g., consistent activity, low default behavior)

Wallets with more supply than borrow and no liquidations ranked higher.  
Riskier wallets with frequent borrowing and liquidations received lower scores.

Finally, the weighted risk score was scaled to the range **0 to 1000** using `MinMaxScaler`.

---

## ✅ Justification of Risk Indicators

- **Borrow/Supply ratio > 1** indicates over-leveraged behavior.
- **Liquidations** are clear markers of poor financial management or risk.
- **Low activity** or **abandonment** may indicate dormant or hacked wallets.
- **Frequent, diversified interactions** and **supplying assets** are signs of healthier behavior.

---

## 📁 Output

The final file `output/scores.csv` contains:

| wallet_address | score |
|----------------|-------|
| 0xabc...123    | 732   |
| 0xdef...456    | 198   |

All 100 wallets are included, even if they had no transaction data (they received a score of 0).

---

**Note:** Raw transaction `.json` files were used temporarily during development and have been excluded from GitHub due to file size limits. However, processed `.csv` outputs and core logic are available.