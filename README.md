# 🤖 XAU/USD AI Trading Bot — London & New York Session

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![MetaTrader5](https://img.shields.io/badge/MetaTrader-5-orange?style=for-the-badge)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Live%20Trading-brightgreen?style=for-the-badge)

**Algorithmic trading bot for XAU/USD (Gold) powered by Machine Learning (XGBoost) with Smart Money Concept (SMC) strategy, targeting London and New York sessions.**

[📊 View Live Dashboard](#-performance-dashboard) · [📈 Backtest Results](#-backtest-results) · [🚀 Getting Started](#-getting-started)

</div>

---

## 📊 Performance Dashboard

> Backtest Period: **August 2025 – September 2026** | 1,978 Trades

| Metric | Value |
|--------|-------|
| 💰 Total Return | **+80.41%** |
| 📉 Max Drawdown | **2.37%** |
| 📊 Profit Factor | **1.54** |
| 🎯 Win Rate | **34.28%** |
| ⚖️ Risk:Reward Ratio | **1 : 3** |
| 💵 Avg Win Trade | **$34** |
| 🔻 Avg Loss Trade | **$11** |
| 🏦 Final Equity | **$27,226** (from $10,000) |

### Equity Curve

```
$27,226 ──────────────────────────────────────────────────────── ↗
                                                          ↗
                                                    ↗
                                         ↗
                              ↗
                   ↗
$10,000 ──────────────────────────────────────────────────────────
Aug 25   Sep 25   Nov 25   Jan 26   Mar 26   May 26   Jul 26   Sep 26
```

> ✅ Konsisten profit setiap bulan, tidak ada bulan merah selama 13 bulan backtest!

---

## 🧠 Strategy Overview

Bot ini menggabungkan **Smart Money Concept (SMC)** dengan **Machine Learning (XGBoost)** untuk mengidentifikasi high-probability entry points pada sesi London dan New York.

### Signal Types

| Signal | Description |
|--------|-------------|
| 🧱 **RBS (Rally-Base-Sell)** | Sell dari Order Block bearish |
| 🧱 **SBR (Support-Become-Resistance)** | Level support yang menjadi resistance |
| 🎯 **REVERSAL_SNIPER** | Reversal high-confidence (100% strength) |
| 🤖 **AI_XGBOOST** | Sinyal dari model ML (confidence > 60%) |

### Feature Engineering

Top 10 features berdasarkan XGBoost importance:

1. `ob` — Order Block signal (**dominan, score: 1.0**)
2. `m15_ob` — Order Block M15 timeframe (0.21)
3. `ob_bottom / ob_top` — Level OB boundaries (0.21 / 0.20)
4. `consecutive_direction` — Momentum directional (0.16)
5. `ob_mitigated` — OB already mitigated (0.08)
6. `atr_ratio` — Volatility ratio (0.07)
7. `body_ratio` — Candle body strength (0.05)
8. `returns_1` — Short-term returns (0.05)
9. `bb_percent_b` — Bollinger Band position (0.05)

---

## 📈 Backtest Results

### Monthly P&L Heatmap (All Green ✅)

| Year | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 2025 | — | — | — | — | — | — | — | +1.22% | +3.07% | +6.22% | +1.77% | +2.64% |
| 2026 | +12.98% | +12.38% | +10.02% | +4.38% | +7.91% | +7.60% | +5.04% | +5.18% | — | — | — | — |

### Session Performance

| Session | Trades | Win Rate |
|---------|--------|----------|
| 🌍 Asian Session | 1,451 | 32.87% |
| 🗽 London Session | 527 | 38.14% |

> London session has a **higher win rate** due to higher volatility & clearer SMC setups.

---

## 🏗️ Architecture

```
london_ny_bot.py          ← Main bot engine (MT5 connection, order management)
├── config_london_ny.py   ← Configuration (sessions, risk params, symbols)
├── regime_detector.py    ← Market regime detection (trending/ranging)
└── ln-ny up/
    ├── feature_eng.py    ← Feature engineering pipeline
    └── train_ml_v5.py    ← XGBoost model training script

backtests/
└── ml_v5/
    ├── xgboost_model_v5_scalper.pkl          ← Trained model
    └── xgboost_model_v5_scalper_metadata.json

backtest_trades.csv       ← Full backtest trade log (1,978 trades)
feature_importance.csv    ← Feature importance scores
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install MetaTrader5 xgboost pandas numpy scikit-learn python-dotenv
```

### Configuration

1. Copy `.env.example` to `.env` and fill your MT5 credentials:
```env
MT5_LOGIN=your_account_number
MT5_PASSWORD=your_password
MT5_SERVER=your_broker_server
```

2. Adjust parameters in `config_london_ny.py`:
```python
LOT_SIZE = 0.01          # Trading lot size
MAX_SPREAD = 30          # Max spread in points
RISK_PER_TRADE = 0.01   # 1% risk per trade
```

### Run the Bot

```bash
python london_ny_bot.py
```

### Train the Model

```bash
python "ln-ny up/train_ml_v5.py"
```

---

## 📊 Visualizations

Built with **Tableau** — Dashboard includes:
- 📈 Equity Curve & Drawdown chart
- 🗓️ Monthly P&L Heatmap
- 🏆 Feature Importance analysis
- 📊 Win Rate by session
- 📉 Trade P&L Distribution

---

## ⚠️ Disclaimer

> This bot is for **educational and research purposes only**. Past backtest performance does not guarantee future results. Trading involves significant financial risk. Always use proper risk management and never trade with money you cannot afford to lose.

---

## 👤 Author

**Muhamad Gani**
- 💼 Data Analyst & Algorithmic Trading Enthusiast
- 🌐 GitHub: [@Gannn10](https://github.com/Gannn10)

---

<div align="center">
⭐ Star this repo if you find it useful!
</div>
