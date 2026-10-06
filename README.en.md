# Compound Returns of an Index Fund vs. a Leveraged ETF

[中文](README.md) | **English**

Compares monthly dollar-cost averaging (DCA) into **SSO (ProShares Ultra S&P500, 2× long the S&P 500)** and **SPY (S&P 500 ETF)** from SSO's launch (June 2006) to today. The dashboard is a single offline HTML page with the data embedded — just double-click to open it.

## Features

- **Monthly DCA**: buys **whole shares** at the monthly bar's **open**; buys 1 share when the price is above the monthly amount
- **Split restoration**: Yahoo's split-adjusted prices are restored to the actual traded prices, and share counts double in split months
- **Expense ratio** (SSO 0.89%, SPY 0.0945%, editable) and **dividend reinvestment**
- **Buy the dip**: buys 2× the amount when this month's open is down ≥ a threshold vs. last month's open (default SSO 10%, SPY 5%)
- **Metrics**: market value, actual investment, shares, average cost, multiple, money-weighted annualized return (IRR), max drawdown, comparison with plain DCA
- **Charts**: scroll/pinch to zoom, drag to pan, range buttons, overview navigator, log scale, dark/light theme
- **Chinese / English**: one-click language switch in the top-right corner; the choice is remembered
- **Portfolio mix**: a slider splits the monthly total between SPY and SSO, with live portfolio breakdown, IRR, max drawdown, and result curves across all mixes
- **1-year decline simulation**: set an S&P 500 decline for the next year, spread across trading days along a geometric path, to simulate monthly moves and holdings for SPY (1×) and SSO (2×), optionally with volatility decay

## Files

| File | Description |
|---|---|
| `dashboard.html` | The dashboard (data embedded, works offline) |
| `download_data.py` | Downloads SSO and SPY monthly bars from Yahoo Finance into `data/`; keeps the old data if a download fails |
| `build_dashboard.py` | Embeds the CSVs in `data/` into `dashboard.html` |
| `update.sh` | Runs the two scripts above in order and logs to `logs/update.log` |
| `data/*.csv` | SSO and SPY monthly bars |
| `launchd/com.laikaiyuan.etf-dashboard-update.plist` | macOS scheduled job: runs `update.sh` at 09:00 on the 1st of every month |

## Usage

```bash
pip install yfinance pandas
python3 download_data.py      # download the latest data
python3 build_dashboard.py    # embed it into the dashboard
open dashboard.html
```

### Monthly auto-update (macOS)

The Python path in `update.sh` and the project path in the plist are set for this machine; change them on another computer. Don't keep the project in Desktop / Documents / Downloads — macOS blocks background jobs from accessing those folders.

```bash
cp launchd/com.laikaiyuan.etf-dashboard-update.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.laikaiyuan.etf-dashboard-update.plist
```

## Disclaimer

Data comes from Yahoo Finance; the latest month is incomplete. This project is for historical backtesting and scenario illustration only and is not investment advice.
