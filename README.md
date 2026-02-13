## Overview

**Interlist-Arbitrage** detects pricing discrepancies for companies listed on multiple stock exchanges (e.g., a stock traded on both NYSE and LSE). 

## Project Structure

```
Interlist-Arbitrage/
├── main.py                      # Entry point; orchestrates entire pipeline
├── sql.py                       # Database utilities (MySQL/pymysql integration)
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── API/                         # Core analysis modules
│   ├── api.py                   # High-level API wrapper
│   │
│   ├── Connections/             # External API integrations
│   │   ├── prices.py            # Yahoo Finance price fetching via yfinance
│   │   ├── forex.py             # Frankfurter API for daily FX rates
│   │   └── data.py              # Configuration: companies, exchanges, currencies
│   │
│   └── Wrangling/               # Data transformation & analysis
│       ├── conversion.py        # Currency conversion & arbitrage calculations
│       ├── preprocessing.py     # Data cleaning & validation
│       └── dates.py             # Timestamp handling & historical data
```

---

## Quick Start

### Installation

1. **Clone/setup the project**:
   ```bash
   cd Interlist-Arbitrage
   pip install -r requirements.txt
   ```

2. **Key dependencies**:
   - `yfinance` — Yahoo Finance price data
   - `requests` — HTTP client for Frankfurter API
   - `pandas` — DataFrames for data manipulation
   - `pymysql` — MySQL database connectivity (optional)

### Run the Analysis

```bash
python main.py
```

## Configuration

Edit **`API/Connections/data.py`** to customize the analysis:

### Companies of Interest
Add or remove company names from the `companies` list:
```python
companies = ["HSBC Holdings plc", "Rio Tinto", "Unilever", ...]
```
Experiment with the full legal name or the stock ticker to find best results.

### Exchanges
Supported exchanges (tickers in Yahoo Finance):
```python
exchanges = ["NYQ", "NMS", "LSE", "HKG", "JPX", "GER", "PAR", "AMS", "NSE"]
```
- **NYQ** = NYSE (New York)
- **NMS** = NASDAQ (New York)
- **LSE** = London Stock Exchange
- **HKG** = Hong Kong Stock Exchange
- **JPX** = Japan Exchange Group (Tokyo)
- **GER** = Frankfurt Stock Exchange
- **PAR** = Euronext Paris
- **AMS** = Euronext Amsterdam
- **NSE** = National Stock Exchange (India)

### ADR Conversion Ratios
For companies with American Depositary Receipts (ADRs), specify the conversion factor:
```python
adr = {"HSBC Holdings plc": 5, ...}  # 1 ADR = 5 underlying shares
```
Prices are divided by this ratio to normalize.

### Currency Mapping
Define which currency each exchange uses:
```python
forex = {
    "NYSE": "USD",
    "LSE": "GBP",
    "HKG": "HKD",
    "JPX": "JPY",
    ...
}
```

## Core Modules

### 1. **Connections/prices.py**
Fetches live stock prices from Yahoo Finance.

**Key Functions**:
- `get_info(company)` → Dictionary of `{exchange: price}` for a given company
- `pull_prices(exchanges, info, company)` → List of prices for all exchanges
- `build_df(exchanges, companies)` → DataFrame with shape (companies, exchanges)

---

### 2. **Connections/forex.py**
Retrieves daily forex conversion rates.

**Key Functions**:
- `define_currencies(forex)` → Constructs API URL for Frankfurter
- `pull(forex)` → Returns dict of `{currency_code: exchange_rate}` vs. USD

**API**: [Frankfurter](https://www.frankfurter.dev) — free, daily-updated rates

---

### 3. **Connections/data.py**
Centralized configuration (companies, exchanges, currencies, ADR ratios).

---

### 4. **Wrangling/conversion.py**
Normalizes prices to USD and calculates arbitrage metrics.

**Key Functions**:
- `match_rates(forex, rates)` → Maps exchanges to their currency rates
- `apply(df, applications)` → Divides prices by currency rate for normalization
- `calculate(df, exch)` → Computes:
  - **int_mean**: Mean price across intl. exchanges (excludes NYSE)
  - **difference**: NYC price minus international average
  - **perc_diff**: Percentage spread (shows arbitrage opportunity magnitude)

---

### 5. **Wrangling/preprocessing.py**
Data validation and cleaning (NaN handling, outlier detection).

---

### 6. **Wrangling/dates.py**
Adds timestamps.

---