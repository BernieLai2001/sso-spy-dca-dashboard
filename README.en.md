# Compound Returns of an Index Fund vs. a Leveraged ETF

[中文](README.md) | **English**

Compares monthly dollar-cost averaging (DCA) into **SSO (ProShares Ultra S&P500, 2× long the S&P 500)** and **SPY (S&P 500 ETF)** from SSO's launch (June 2006) to today. The dashboard is a single offline HTML page with the data embedded — just double-click to open it.

## Features

- **Monthly DCA**: buys **whole shares** at the monthly bar's **open**; buys 1 share when the price is above the monthly amount
- **Split restoration**: Yahoo's split-adjusted prices are restored to the actual traded prices, and share counts double in split months
- **Expense ratio** (SSO 0.89%, SPY 0.0945%, editable) and **dividend reinvestment**
- **Buy the dip**: buys 2× the amount when this month's open is down ≥ a threshold vs. last month's open (default SSO 10%, SPY 5%)
- **Metrics**: market value, actual investment, shares, average cost, multiple, money-weighted annualized return (IRR) and the ETF's own time-weighted return, max drawdown, comparison with plain DCA
- **Charts**: scroll/pinch to zoom, drag to pan, range buttons, overview navigator, log scale, dark/light theme
- **Chinese / English**: one-click language switch in the top-right corner
- **Remembers your settings**: all inputs and the theme are restored next time (stored in the browser); "Reset" in the top-right restores the defaults
- **Portfolio mix**: a slider splits the monthly total between SPY and SSO, with live portfolio breakdown, IRR, max drawdown, and result curves across all mixes
- **Risk-free & inflation comparison**: "10Y Treasury DCA" and "inflation break-even" lines on the main chart; cards show real (after-inflation) return, excess return vs the 10Y Treasury and the Sharpe ratio; an "Amounts in" selector shows nominal, today's or start-month dollars (the latter two inflation-adjusted); a "How inflation eats your money" panel shows purchasing-power erosion
- **Valuation (Shiller CAPE)**: current value and its percentile since 1871 and over the last 40 years, long-run and 40-year average lines, the record high, earnings yield (1 ÷ CAPE) vs the 10Y Treasury, and its path since 1920 (the DCA period shaded light blue)
- **Retirement**: monthly living cost after retiring at 65 (manual, default $3,000, or US income per capita × a pension replacement rate; rising with inflation), funded either by the portfolio (the rest keeps growing; shows how long it lasts) or by an annuity (premium, paying years, monthly / yearly payout; shows the shortfall and break-even age)
- **Historical volatility**: rolling 12-month annualized volatility of SPY and SSO, with current, period-average and peak values; when the decline simulation is on, the volatility set there is marked on the chart
- **Decline simulation**: set a length (1–120 months, default 12) and the S&P 500's decline over that period, spread across trading days along a geometric path, to simulate monthly moves and holdings for SPY (1×) and SSO (2×), optionally with volatility decay from an S&P 500 annual volatility you enter (SSO's is set automatically to 2×), and a shaded ±1σ volatility range (on both the cumulative-change chart and the main portfolio-value chart); includes an "effect of volatility on SSO" curve (SSO's change over the simulation period for S&P 500 volatility 0%–80%, against SPY and a naive 2×)

## Files

| File | Description |
|---|---|
| `dashboard.html` | The dashboard (data embedded, works offline) |
| `download_data.py` | Downloads SSO and SPY monthly bars from Yahoo Finance, the 10Y Treasury yield (GS10) and CPI (CPIAUCSL) from FRED, the S&P 500 Shiller CAPE from multpl.com, and US personal income per capita from FRED into `data/`; keeps the old data if a download fails |
| `build_dashboard.py` | Embeds the CSVs in `data/` into `dashboard.html` |
| `update.sh` | Runs the two scripts above in order and logs to `logs/update.log`; finds a Python with the dependencies installed (or set `PYTHON`) |
| `requirements.txt` | Python dependencies (yfinance, pandas, lxml) |
| `install_autoupdate.sh` | Installs / uninstalls the macOS monthly auto-update, filling in local paths |
| `launchd/etf-dashboard-update.plist.template` | Scheduled-job template: runs `update.sh` at 09:00 on the 1st of every month |
| `data/*.csv` | SSO and SPY monthly bars; `MACRO_monthly.csv` holds the 10Y yield and CPI; `PE_monthly.csv` holds the Shiller CAPE; `INCOME_quarterly.csv` holds US personal income per capita |

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

Market data comes from Yahoo Finance (the latest month is incomplete); rates and CPI come from FRED; CAPE from multpl.com. This project is for historical backtesting and scenario illustration only and is not investment advice.
