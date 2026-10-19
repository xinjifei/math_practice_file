# demo_real_stocks.py
# 真实数据版：三只 A 股一年的真实日线，检验年化公式。
#
#   外推：只拿【第一个月】的日收益估 μ 和 σ → μ×252、σ×√252
#   实际：拿【整一年】的价格和日收益 → 真正的一年收益、真正的年化波动
#   放一起看：年初用一个月的样本外推出来的数，和全年现实差多远。
#
# 数据来源：和 数据源获取/script/get_data.py 是同一个 akshare 接口
#          （ak.stock_zh_a_daily），只改了两处：
#            1) adjust="qfq" 前复权。get_data.py 里是 adjust=""（不复权），
#               碰到分红除权那天价格会凭空跳水，算出来的收益率是假的。
#            2) 不写死 Windows 路径 D:/...，也不落盘。

import numpy as np
import matplotlib.pyplot as plt   # 只用来开两个子图；画图仍然全部走 function/plot.py 的 plot()
import akshare as ak

from function.plot import plot


TRADING_DAYS = 252       # 一年约多少个交易日
MONTH_DAYS = 21          # 一个月约多少个交易日（21 × 12 ≈ 252）
START, END = "20251001", "20260930"

STOCKS = [
    ("sz000001", "平安银行"),
    ("sz000858", "五粮液"),
    ("sz300750", "宁德时代"),
]


rows = []
for symbol, name in STOCKS:
    # 拉日线。返回的 df 里有一列 close（收盘价），行按日期升序
    df = ak.stock_zh_a_daily(symbol=symbol,
                             start_date=START,
                             end_date=END,
                             adjust="qfq")
    close = df["close"].to_numpy(dtype=float)

    # 日收益率：今天收盘 / 昨天收盘 - 1。
    #   close[1:] 是"今天"到"最后一天"，close[:-1] 是"第一天"到"倒数第二天"
    #   n 个价格 → n-1 个收益率（和 Day 40 那个坑一样）
    r = close[1:] / close[:-1] - 1

    # ---- 第一个月：只有 21 个样本 ----
    r_month = r[:MONTH_DAYS]
    r_est = r_month.mean() * TRADING_DAYS                    # 年化收益 = 日均 × 252
    v_est = r_month.std(ddof=1) * np.sqrt(TRADING_DAYS)      # 年化波动 = 日标准差 × √252

    # ---- 整一年：真正发生了什么 ----
    r_real = close[-1] / close[0] - 1                        # 首尾价格之比（几何，不是相加）
    v_real = r.std(ddof=1) * np.sqrt(TRADING_DAYS)

    rows.append({"name": name, "days": len(close),
                 "r_est": r_est, "r_real": r_real,
                 "v_est": v_est, "v_real": v_real})


# ---- 打表：每只股票一小块，省得为中文对齐发愁 ----
print(f"\n区间 {START} → {END}")
for x in rows:
    print(f"\n{x['name']}（{x['days']} 个交易日）")
    print(f"  年化收益   外推 {x['r_est']:>7.2%}    实际 {x['r_real']:>7.2%}"
          f"    误差 {x['r_real'] - x['r_est']:>+7.2%}")
    print(f"  年化波动   外推 {x['v_est']:>7.2%}    实际 {x['v_real']:>7.2%}"
          f"    误差 {x['v_real'] - x['v_est']:>+7.2%}")


# ---- 画图：两张子图，一张收益率、一张波动率 ----
xs = np.arange(1, len(rows) + 1)          # X 轴：三只股票的位置 1、2、3


def col(key):
    """把某个字段取出来，转成 plot() 要的 (n, 2) 矩阵；×100 换成百分数。"""
    return np.column_stack([xs, [row[key] * 100 for row in rows]])


labels = [row["name"] for row in rows]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

plot([{"type": "point", "data": col("r_est"), "color": "tab:blue", "s": 90, "labels": labels},
      {"type": "point", "data": col("r_real"), "color": "tab:orange", "s": 90}],
     title="年化收益率（%）：蓝 = 第一个月外推，橙 = 整年实际",
     ax=axes[0], show=False)

plot([{"type": "point", "data": col("v_est"), "color": "tab:blue", "s": 90, "labels": labels},
      {"type": "point", "data": col("v_real"), "color": "tab:orange", "s": 90}],
     title="年化波动率（%）：蓝 = 第一个月外推，橙 = 整年实际",
     ax=axes[1], show=False)

plt.tight_layout()
plt.show()

# 看完最该记住的不是哪只股票，而是这三条：
#
# 1) 两条公式是【换算】，不是【预测】。它们只负责把已有的数换到"年"这把尺子上，
#    不保证明年的数长这样。平安银行用第一个月外推 +40.89%，全年实际只有 +9.36%。
#
# 2) 误差的量级不对称：收益乘 252，波动只乘 √252 ≈ 15.9。同一个"一个月"的估计误差，
#    在收益上被放大 252 倍，在波动上只放大 15.9 倍。
#
# 3) 但波动外推也不等于准 —— 五粮液第一个月特别平静（外推 12.54%），
#    全年实际却是 22.61%。原因是波动率自己会变（波动聚集），
#    一个月的 σ 代表不了一整年。教材把"波动率期限结构"划掉了，
#    这里你能亲眼看到它存在。
