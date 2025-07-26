# 📊 Analysis: DeFi Wallet Risk Scoring (Compound V2)

This document explains the approach used to collect data, engineer features, and compute risk scores for 100 wallets interacting with the Compound V2 protocol.

---

## 1. 📟 Data Collection

* **API Used**: [Covalent API](https://www.covalenthq.com/docs/)
* **Protocol**: Compound V2
* **Wallet Source**: Provided list of 100 wallet addresses
* **Script**: `fetch_transactions.py`

We queried each wallet’s transaction history related to Compound V2 using Covalent's `protocol_v2` endpoints and saved results as JSON in `data/raw_transactions/`.

---

## 2. 🗹 Data Flattening

* **Script**: `flatten_transactions.py`
* Raw JSON responses were parsed to extract:

  * Transaction hash
  * Wallet address
  * Token involved
  * Transaction value
  * Method/event name (e.g., deposit, borrow, repay)
  * Timestamp

Corrupted or null-decoded transactions were skipped safely.

---

## 3. 🧮 Feature Engineering

* **Script**: `feature_engineering.py`
* The following features were engineered per wallet:

| Feature              | Description                             |
| -------------------- | --------------------------------------- |
| `num_transactions`   | Number of Compound V2 transactions      |
| `total_value_usd`    | Sum of all tx amounts in USD            |
| `num_unique_tokens`  | Number of unique tokens interacted with |
| `active_days`        | Days between first and last tx          |
| `num_borrow_events`  | Total borrow actions                    |
| `num_supply_events`  | Total supply/deposit actions            |
| `repay_borrow_ratio` | Ratio of repay to borrow actions        |

The features were normalized for scoring.

---

## 4. 📈 Risk Scoring

* **Script**: `scoring.py`
* Wallets were scored based on:

  * High number of transactions (more active = safer)
  * Higher diversity of tokens (indicates diversification)
  * Balanced borrow and repay behavior (healthy repayment)
  * Lower borrow dominance and high repay ratio
  * Significant value transferred (indicates trust)

Each feature was min-max scaled and aggregated with weights:

```python
score = (
    0.2 * norm(num_transactions) +
    0.2 * norm(total_value_usd) +
    0.15 * norm(num_unique_tokens) +
    0.15 * norm(active_days) +
    0.15 * norm(repay_borrow_ratio) +
    0.15 * norm(num_supply_events)
)
```

Then scaled to 0–1000.

---

## 5. ✅ Final Output

* File: `wallet_scores.csv`
* Format:

  ```csv
  wallet_address,score
  0xfaa07...,732
  ...
  ```
* Wallets with limited or no activity were scored lower (riskier).

---

## 6. 📌 Limitations

* The scoring model is static and doesn’t account for protocol-level risks or market volatility.
* Value calculations assume the token prices fetched by Covalent are accurate.
* On-chain liquidation or health factor data was not directly used.

---

## 7. 🔄 Improvements Possible

* Use real-time token prices for value normalization.
* Incorporate Compound V2-specific risk metrics like collateral ratio or liquidation risk.
* Include historical lending/borrowing rate volatility per token.

---
