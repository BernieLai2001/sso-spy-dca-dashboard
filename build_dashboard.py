"""把 data/ 下的 SSO、SPY 月K CSV 嵌入 dashboard.html，使其双击即可离线打开。

浏览器用 file:// 打开本地页面时无法 fetch CSV，所以把数据直接写进 HTML 的
<!-- ETF_DATA_START --> 与 <!-- ETF_DATA_END --> 之间（可重复运行）。
更新数据流程：python3 download_data.py && python3 build_dashboard.py
"""
import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
HTML = ROOT / "dashboard.html"
TICKERS = ["SSO", "SPY"]


def load(ticker: str) -> dict:
    df = pd.read_csv(DATA_DIR / f"{ticker}_monthly.csv")
    return {
        "dates": [d[:7] for d in df["Date"]],
        "open": [round(x, 6) for x in df["Open"]],
        "close": [round(x, 6) for x in df["Close"]],
        "div": [round(x, 6) for x in df["Dividends"]],
        "split": [x for x in df["Stock Splits"]],
    }


if __name__ == "__main__":
    payload = {t: load(t) for t in TICKERS}
    payload["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    block = (
        "<!-- ETF_DATA_START -->\n<script>window.ETF_DATA = "
        + json.dumps(payload, separators=(",", ":"))
        + ";</script>\n<!-- ETF_DATA_END -->"
    )
    html = HTML.read_text(encoding="utf-8")
    html, n = re.subn(r"<!-- ETF_DATA_START -->.*?<!-- ETF_DATA_END -->", lambda _: block, html, flags=re.S)
    if n != 1:
        raise SystemExit("dashboard.html 中未找到数据占位标记 / data placeholder not found in dashboard.html")
    HTML.write_text(html, encoding="utf-8")
    print(f"已将 {', '.join(TICKERS)} 数据嵌入 / Embedded {', '.join(TICKERS)} data into {HTML}")
