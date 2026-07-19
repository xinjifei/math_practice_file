"""m20 练习：用真实数据算一只股票的 Beta
沪深300 (X) vs 平安银行 (Y) → 拟合回归线 Ŷ = a + bX
"""

import sys
sys.path.insert(0, "D:/math_practice_file/数据源获取/script")
from get_data import get_stock_data
import akshare as ak
import pandas as pd
import numpy as np
from scipy.stats import linregress
import plotly.graph_objects as go

# ============================================================
# 1. 获取数据
# ============================================================
# 个股：平安银行
df_stock = get_stock_data(
    symbol="sz000001",
    stock_name="平安银行",
    start_date="20250623",
    end_date="20260623",
)

# 大盘：沪深300 指数
df_index = ak.stock_zh_index_daily(symbol="sh000300")
df_index["date"] = pd.to_datetime(df_index["date"])
df_index = df_index[(df_index["date"] >= "2025-06-23") & (df_index["date"] <= "2026-06-23")]

# ============================================================
# 2. 对齐日期，算日收益率
# ============================================================
df_stock["date"] = pd.to_datetime(df_stock["date"])
df_index["date"] = pd.to_datetime(df_index["date"])

merged = pd.merge(df_stock[["date", "close"]], df_index[["date", "close"]],
                  on="date", suffixes=("_stock", "_index"))
merged["ret_stock"] = merged["close_stock"].pct_change()
merged["ret_index"] = merged["close_index"].pct_change()
merged = merged.dropna()

X = merged["ret_index"].values   # 大盘收益率
Y = merged["ret_stock"].values   # 个股收益率

# ============================================================
# 3. 回归 —— 就这一行
# ============================================================
result = linregress(X, Y)
a = result.intercept   # Alpha（截距）
b = result.slope       # Beta（斜率）
r = result.rvalue      # 相关系数

print("=" * 50)
print(f"  Alpha (截距 a)  = {a:.6f}  → 大盘不涨不跌时，个股的基准收益")
print(f"  Beta  (斜率 b)  = {b:.2f}    → 大盘涨 1%，个股预期涨 {b:.2f}%")
print(f"  相关系数 r       = {r:.3f}   → 两只'同涨同跌'的强度")
print(f"  R^2             = {r**2:.3f}  → 大盘能解释个股 {r**2*100:.0f}% 的波动")
print("=" * 50)

# ============================================================
# 4. 画图：散点 + 回归线 + 标注
# ============================================================
x_line = np.linspace(X.min(), X.max(), 100)
y_line = a + b * x_line

fig = go.Figure()

# 散点
fig.add_trace(go.Scatter(
    x=X, y=Y, mode="markers",
    marker=dict(size=8, color="#3b82f6", opacity=0.6),
    name="每日收益率",
    hovertemplate="沪深300: %{x:.2%}<br>平安银行: %{y:.2%}<extra></extra>",
))

# 回归线
fig.add_trace(go.Scatter(
    x=x_line, y=y_line, mode="lines",
    line=dict(color="#f59e0b", width=2.5),
    name=f"Ŷ = {a:.4f} + {b:.2f}·X",
))

# 标注 Beta
fig.add_annotation(
    x=x_line[70], y=a + b * x_line[70],
    text=f"<b>β = {b:.2f}</b>",
    showarrow=True, arrowhead=0,
    ax=40, ay=-30,
    font=dict(size=18, color="#f59e0b"),
    bgcolor="rgba(15,23,42,0.8)",
)

fig.update_layout(
    title=dict(text=f"<b>平安银行 Beta = {b:.2f}</b>——大盘涨1%，个股预期涨{b:.2f}%", font=dict(size=16)),
    xaxis=dict(title="沪深300 日收益率", tickformat=".1%", zeroline=True, zerolinecolor="#555"),
    yaxis=dict(title="平安银行 日收益率", tickformat=".1%", zeroline=True, zerolinecolor="#555"),
    template="plotly_dark",
    height=520,
    margin=dict(l=60, r=30, t=60, b=60),
)

# 存 HTML
out = r"D:\math_practice_file\b统计推断\m20_简单线性回归\m20_result.html"
fig.write_html(out, config=dict(responsive=True, displayModeBar=False))
print(f"已保存: {out}")

import webbrowser
webbrowser.open(out)
