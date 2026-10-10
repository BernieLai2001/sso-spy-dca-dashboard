"""下载 SSO（ProShares Ultra S&P500，2倍做多标普500）与 SPY 的月K线数据，以及
十年期美债收益率（无风险收益基准）和 CPI（通货膨胀），保存为 CSV。

数据来源：Yahoo Finance（通过 yfinance）；FRED 公开 CSV（GS10、CPIAUCSL，无需 API key）；
multpl.com（标普 500 席勒市盈率 CAPE，1871 年起月度）
下载失败或数据异常时不会覆盖已有 CSV，并以非零状态退出。
"""
import sys
from pathlib import Path

import pandas as pd
import yfinance as yf

DATA_DIR = Path(__file__).resolve().parent / "data"
TICKERS = ["SSO", "SPY"]
COLUMNS = ["Open", "High", "Low", "Close", "Adj Close", "Volume", "Dividends", "Stock Splits"]
# FRED：GS10 = 十年期国债收益率（月均，%）；CPIAUCSL = CPI（城市所有消费者，季调，1982-84=100）
FRED_SERIES = {"GS10": "GS10", "CPI": "CPIAUCSL"}
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
# multpl.com：标普 500 席勒市盈率（CAPE = 价格 ÷ 过去 10 年经通胀调整的平均盈利）
# 不用普通 P/E：它按过去 12 个月的报告利润计算，2009 年盈利塌陷时会飙到 100 倍以上，容易误导
PE_PAGES = {"CAPE": "https://www.multpl.com/shiller-pe/table/by-month"}


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


def download_macro() -> Path:
    """十年期国债收益率与 CPI 合并为一张月度表 / 10Y yield and CPI merged into one monthly table."""
    frames = []
    for col, sid in FRED_SERIES.items():
        s = pd.read_csv(FRED_CSV.format(sid))
        s.columns = ["Date", col]
        s["Date"] = pd.to_datetime(s["Date"])
        s[col] = pd.to_numeric(s[col], errors="coerce")
        frames.append(s.dropna().set_index("Date"))
    df = pd.concat(frames, axis=1).sort_index()
    df = df[df.index >= "1990-01-01"]
    if df.empty or df["GS10"].dropna().empty or df["CPI"].dropna().empty:
        raise RuntimeError("FRED: 下载结果为空 / empty download")
    out = DATA_DIR / "MACRO_monthly.csv"
    tmp = out.with_suffix(".csv.tmp")
    df.to_csv(tmp, index_label="Date", date_format="%Y-%m-%d")
    tmp.replace(out)
    print(f"GS10 至 / through {df['GS10'].last_valid_index().date()}，CPI 至 / through "
          f"{df['CPI'].last_valid_index().date()} -> {out}")
    return out


def download_pe() -> Path:
    """标普 500 席勒市盈率 CAPE（月度）/ S&P 500 Shiller CAPE (monthly)."""
    import io
    import re
    import urllib.request

    frames = []
    for col, url in PE_PAGES.items():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
        t = pd.read_html(io.StringIO(html))[0]
        t.columns = ["Date", col]
        t["Date"] = pd.to_datetime(t["Date"], errors="coerce").dt.to_period("M").dt.to_timestamp()
        # 数值前可能带估算标记（如 †），只取数字 / strip estimate markers
        t[col] = pd.to_numeric(t[col].astype(str).str.extract(r"([\d.]+)")[0], errors="coerce")
        frames.append(t.dropna().drop_duplicates("Date").set_index("Date"))
    df = pd.concat(frames, axis=1).sort_index()
    if len(df) < 1000:
        raise RuntimeError(f"CAPE 数据只有 {len(df)} 行，可能页面结构变了 / only {len(df)} rows; page layout may have changed")
    out = DATA_DIR / "PE_monthly.csv"
    tmp = out.with_suffix(".csv.tmp")
    df.to_csv(tmp, index_label="Date", date_format="%Y-%m-%d")
    tmp.replace(out)
    print(f"CAPE：{df.index.min().date()} ~ {df.index.max().date()}，{len(df)} 个月 -> {out}")
    return out


if __name__ == "__main__":
    DATA_DIR.mkdir(exist_ok=True)
    failed = False
    for job in [lambda t=t: download_monthly(t) for t in TICKERS] + [download_macro, download_pe]:
        try:
            job()
        except Exception as e:  # 单个失败不影响其他；保留旧文件
            print(f"[失败 / FAILED] {e}", file=sys.stderr)
            failed = True
    sys.exit(1 if failed else 0)
