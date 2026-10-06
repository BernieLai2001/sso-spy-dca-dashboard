"""下载 SSO（ProShares Ultra S&P500，2倍做多标普500）与 SPY 的月K线数据，保存为 CSV。

数据来源：Yahoo Finance（通过 yfinance）
下载失败或数据异常时不会覆盖已有 CSV，并以非零状态退出。
"""
import sys
from pathlib import Path

import pandas as pd
import yfinance as yf

DATA_DIR = Path(__file__).resolve().parent / "data"
TICKERS = ["SSO", "SPY"]
COLUMNS = ["Open", "High", "Low", "Close", "Adj Close", "Volume", "Dividends", "Stock Splits"]


def download_monthly(ticker: str) -> Path:
    df = yf.Ticker(ticker).history(period="max", interval="1mo", auto_adjust=False)
    df = df.dropna(subset=["Close"])
    if df.empty or not set(COLUMNS) <= set(df.columns):
        raise RuntimeError(f"{ticker}: 下载结果为空或缺少字段 / download is empty or missing columns")
    df.index = df.index.tz_localize(None).date
    df.index.name = "Date"
    df = df[COLUMNS]

    out = DATA_DIR / f"{ticker}_monthly.csv"
    if out.exists():
        old = pd.read_csv(out)
        if len(df) < len(old):
            raise RuntimeError(f"{ticker}: 新数据只有 {len(df)} 行，少于已有的 {len(old)} 行，放弃覆盖 / "
                               f"only {len(df)} rows, fewer than the existing {len(old)}; not overwriting")
    tmp = out.with_suffix(".csv.tmp")
    df.to_csv(tmp)
    tmp.replace(out)
    print(f"{ticker}: {len(df)} 条月度数据 / monthly rows, {df.index[0]} ~ {df.index[-1]} -> {out}")
    return out


if __name__ == "__main__":
    DATA_DIR.mkdir(exist_ok=True)
    failed = False
    for t in TICKERS:
        try:
            download_monthly(t)
        except Exception as e:  # 单个失败不影响另一个；保留旧文件
            print(f"[失败 / FAILED] {e}", file=sys.stderr)
            failed = True
    sys.exit(1 if failed else 0)
