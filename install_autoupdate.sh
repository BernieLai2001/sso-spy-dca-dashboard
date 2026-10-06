#!/bin/bash
# 安装 / 卸载每月自动更新（macOS launchd）。
# Install / uninstall the monthly auto-update (macOS launchd).
#
#   ./install_autoupdate.sh            安装（或重新安装）/ install (or reinstall)
#   ./install_autoupdate.sh --uninstall 卸载 / uninstall
set -eu
DIR="$(cd "$(dirname "$0")" && pwd)"
LABEL="com.$(id -un | tr -c 'A-Za-z0-9.\n' '-').etf-dashboard-update"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"

if [ "$(uname)" != "Darwin" ]; then
  echo "仅支持 macOS。其他系统可用 cron / 任务计划程序定时运行 update.sh 或两个 Python 脚本。"
  echo "macOS only. On other systems, schedule update.sh (or the two Python scripts) with cron / Task Scheduler."
  exit 1
fi

launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true

if [ "${1:-}" = "--uninstall" ]; then
  rm -f "$PLIST"
  echo "已卸载 / Uninstalled: $LABEL"
  exit 0
fi

# macOS 不允许后台任务访问「桌面 / 文稿 / 下载」/ macOS blocks background jobs from Desktop, Documents, Downloads
case "$DIR" in
  "$HOME/Desktop"*|"$HOME/Documents"*|"$HOME/Downloads"*)
    echo "项目在「桌面 / 文稿 / 下载」里，macOS 会阻止后台任务访问。请先把项目移到别处（例如 ~/Projects）。"
    echo "The project is inside Desktop / Documents / Downloads, which macOS blocks for background jobs. Move it elsewhere first (e.g. ~/Projects)."
    exit 1 ;;
esac

chmod +x "$DIR/update.sh"
mkdir -p "$HOME/Library/LaunchAgents"
# 路径可能含 & 或 |，先转义再替换 / escape & and | before substituting
esc() { printf '%s' "$1" | sed -e 's/[&|\\]/\\&/g'; }
sed -e "s|__LABEL__|$(esc "$LABEL")|" -e "s|__UPDATE_SH__|$(esc "$DIR/update.sh")|" \
  "$DIR/launchd/etf-dashboard-update.plist.template" > "$PLIST"
plutil -lint "$PLIST" >/dev/null
launchctl bootstrap "$DOMAIN" "$PLIST"

echo "已安装 / Installed: $LABEL"
echo "每月 1 日 09:00 自动运行 / Runs at 09:00 on the 1st of each month: $DIR/update.sh"
echo "立即试运行 / Run now: launchctl kickstart $DOMAIN/$LABEL"
echo "日志 / Log: $DIR/logs/update.log"
