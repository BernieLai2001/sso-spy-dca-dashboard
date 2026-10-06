#!/bin/bash
# 每月自动更新：下载最新月K数据 → 重新生成仪表盘。由 launchd 定时调用，也可手动运行。
# Monthly auto-update: download the latest monthly bars, then rebuild the dashboard (run by launchd or by hand).
# 日志 / Log: logs/update.log
#
# Python 选择 / Python selection:
#   设置了环境变量 PYTHON 就用它；否则依次尝试常见位置，选第一个已装好 yfinance 和 pandas 的。
#   Uses $PYTHON if set; otherwise the first common python3 that has yfinance and pandas installed.
set -u
cd "$(dirname "$0")" || exit 1
mkdir -p logs

find_python() {
  local c
  for c in ${PYTHON:-} \
           "$HOME/anaconda3/bin/python3" "$HOME/miniconda3/bin/python3" /opt/anaconda3/bin/python3 /opt/miniconda3/bin/python3 \
           /opt/homebrew/bin/python3 /usr/local/bin/python3 "$(command -v python3 2>/dev/null)" /usr/bin/python3; do
    [ -n "$c" ] && [ -x "$c" ] && "$c" -c "import yfinance, pandas" >/dev/null 2>&1 && { echo "$c"; return 0; }
  done
  return 1
}

{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') 开始更新 / Update started ====="
  if ! PY=$(find_python); then
    echo "找不到装有 yfinance 和 pandas 的 Python，请先运行：pip install -r requirements.txt"
    echo "No Python with yfinance and pandas found. Run: pip install -r requirements.txt"
    echo "更新失败（已保留旧数据）/ Update failed (previous data kept)"
    exit 1
  fi
  echo "Python: $PY"
  if "$PY" download_data.py && "$PY" build_dashboard.py; then
    echo "更新成功 / Update succeeded"
  else
    echo "更新失败（已保留旧数据）/ Update failed (previous data kept)"
    osascript -e 'display notification "SSO/SPY 数据更新失败 / Data update failed — see logs/update.log" with title "定投仪表盘 / DCA Dashboard"' 2>/dev/null
    exit 1
  fi
} >> logs/update.log 2>&1
