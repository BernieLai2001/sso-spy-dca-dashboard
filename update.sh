#!/bin/bash
# 每月自动更新：下载最新月K数据 → 重新生成仪表盘。由 launchd 定时调用，也可手动运行。
# Monthly auto-update: download the latest monthly bars, then rebuild the dashboard (run by launchd or by hand).
# 日志 / Log: logs/update.log
set -u
cd "$(dirname "$0")" || exit 1
PY=/opt/anaconda3/bin/python3
mkdir -p logs
{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') 开始更新 / Update started ====="
  if "$PY" download_data.py && "$PY" build_dashboard.py; then
    echo "更新成功 / Update succeeded"
  else
    echo "更新失败（已保留旧数据）/ Update failed (previous data kept)"
    osascript -e 'display notification "SSO/SPY 数据更新失败 / Data update failed — see logs/update.log" with title "定投仪表盘 / DCA Dashboard"' 2>/dev/null
    exit 1
  fi
} >> logs/update.log 2>&1
