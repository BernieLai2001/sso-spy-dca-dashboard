# 指数基金和杠杆ETF的复合收益率计算

**中文** | [English](README.en.md)

对比 **SSO（ProShares Ultra S&P500，2 倍做多标普 500）** 与 **SPY（标普 500 ETF）** 从 SSO 成立（2006-06）至今每月定投的价值增长。仪表盘是一个离线 HTML 页面，数据已嵌入其中，双击即可打开。

## 功能

- **每月定投**：按月K **开盘价**买入**整数股**；价格高于定投金额时买 1 股
- **拆股还原**：把 Yahoo 的拆股调整价格还原为当时真实成交价，拆股当月持股数随之翻倍
- **扣除管理费**（SSO 0.89%、SPY 0.0945%，可改）与 **股息红利再投资**
- **下跌加倍**：本月开盘价较上月开盘价下跌 ≥ 阈值（默认 SSO 10%、SPY 5%）时按 2 倍金额买入
- **指标**：市值、实际投入、持股数、平均持仓成本价、收益倍数、资金加权年化收益（IRR）、最大回撤、与普通定投对比
- **图表**：滚轮/双指缩放、拖动平移、区间快捷按钮、缩略导航条、对数坐标、深色/浅色
- **中英文切换**：右上角按钮一键切换 中文 / English，并记住上次的选择
- **组合配置**：每月总投入按滑块比例分给 SPY 和 SSO，即时显示组合市值构成、IRR、最大回撤，以及不同比例的结果曲线
- **无风险收益与通胀对比**：主图加入「同期国债定投」和「通胀保值线」；卡片显示扣通胀的实际年化、相对十年期国债的超额收益、夏普比率；「通货膨胀的侵蚀」面板展示购买力缩水
- **未来一年下跌测算**：设定 S&P500 一年跌幅，按几何路径分摊到每个交易日，测算 SPY（1 倍）和 SSO（2 倍）每月涨跌与持仓变化，可加入波动损耗

## 文件

| 文件 | 说明 |
|---|---|
| `dashboard.html` | 仪表盘（数据已嵌入，可离线打开） |
| `download_data.py` | 从 Yahoo Finance 下载 SSO、SPY 月K数据，从 FRED 下载十年期国债收益率（GS10）和 CPI（CPIAUCSL），保存到 `data/`；失败时不覆盖旧数据 |
| `build_dashboard.py` | 把 `data/` 里的 CSV 嵌入 `dashboard.html` |
| `update.sh` | 依次运行以上两个脚本，日志写入 `logs/update.log`；会自动找到装有依赖的 Python（也可用环境变量 `PYTHON` 指定） |
| `requirements.txt` | Python 依赖（yfinance、pandas） |
| `install_autoupdate.sh` | 安装 / 卸载 macOS 每月自动更新，自动填入本机路径 |
| `launchd/etf-dashboard-update.plist.template` | 定时任务模板：每月 1 日 09:00 运行 `update.sh` |
| `data/*.csv` | SSO、SPY 月K数据；`MACRO_monthly.csv` 为十年期国债收益率与 CPI |

## 快速开始

### 1. 只看仪表盘（不用装任何东西）

下载或克隆仓库后，用浏览器打开 `dashboard.html` 即可（Windows / macOS / Linux 都可以）。数据已嵌入页面，离线可用。

### 2. 更新到最新数据（需要 Python 3.9+）

```bash
git clone https://github.com/BernieLai2001/sso-spy-dca-dashboard.git
cd sso-spy-dca-dashboard
pip install -r requirements.txt
python3 download_data.py      # 下载最新数据（Windows 用 python）
python3 build_dashboard.py    # 嵌入仪表盘
```

macOS / Linux 也可以直接运行 `./update.sh`，它会依次执行以上两步并写日志。

### 3. 每月自动更新（仅 macOS）

```bash
./install_autoupdate.sh               # 安装：每月 1 日 09:00 自动运行 update.sh
./install_autoupdate.sh --uninstall   # 卸载
```

安装脚本会自动填入你电脑上的路径。项目不要放在「桌面 / 文稿 / 下载」里，macOS 不允许后台任务访问这些文件夹（脚本会检查并提示）。
Windows 可用「任务计划程序」、Linux 可用 cron 定时运行 `download_data.py` 和 `build_dashboard.py`。

## 说明

行情数据来自 Yahoo Finance，最后一个月为未完结月份；利率与 CPI 来自 FRED。本项目仅作历史回测与情景演示，不构成投资建议。
