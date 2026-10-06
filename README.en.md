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
| `update.sh` | Runs the two scripts above in order and logs to `logs/update.log`; finds a Python with the dependencies installed (or set `PYTHON`) |
| `requirements.txt` | Python dependencies (yfinance, pandas) |
| `install_autoupdate.sh` | Installs / uninstalls the macOS monthly auto-update, filling in local paths |
| `launchd/etf-dashboard-update.plist.template` | Scheduled-job template: runs `update.sh` at 09:00 on the 1st of every month |
| `data/*.csv` | SSO and SPY monthly bars |

## Quick start

### 1. Just view the dashboard (nothing to install)

Download or clone the repo and open `dashboard.html` in a browser (Windows / macOS / Linux). The data is embedded, so it works offline.

### 2. Update to the latest data (Python 3.9+)

```bash
git clone https://github.com/BernieLai2001/sso-spy-dca-dashboard.git
cd sso-spy-dca-dashboard
pip install -r requirements.txt
python3 download_data.py      # download the latest data (use `python` on Windows)
python3 build_dashboard.py    # embed it into the dashboard
```

On macOS / Linux you can also run `./update.sh`, which does both steps and writes a log.

### 3. Monthly auto-update (macOS only)

```bash
./install_autoupdate.sh               # install: runs update.sh at 09:00 on the 1st of each month
./install_autoupdate.sh --uninstall   # uninstall
```

The installer fills in the paths for your machine. Don't keep the project in Desktop / Documents / Downloads — macOS blocks background jobs there (the installer checks and warns).
On Windows use Task Scheduler, on Linux use cron, to run `download_data.py` and `build_dashboard.py` on a schedule.

## Disclaimer

Data comes from Yahoo Finance; the latest month is incomplete. This project is for historical backtesting and scenario illustration only and is not investment advice.
