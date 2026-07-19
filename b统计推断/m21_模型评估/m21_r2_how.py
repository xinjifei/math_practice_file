"""m21：R² 是怎么算出来的——一张图讲清楚
上排：总变异（每个点到均值线的距离平方和）
下排：残差（每个点到回归线的距离平方和）
R² = 1 - 残差平方和 / 总变异平方和
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import linregress

np.random.seed(42)
n = 40
x = np.random.normal(0, 1, n)
y = 1.5 * x + np.random.normal(0, 1.2, n)

res = linregress(x, y)
a, b = res.slope, res.intercept
y_mean = np.mean(y)
y_pred = a * x + b
r2 = res.rvalue ** 2

x_line = np.linspace(x.min(), x.max(), 100)

# ============================================================
# 上排：总变异 —— 每个点到均值线的距离
# ============================================================
fig1 = go.Figure()

# 均值水平线
fig1.add_trace(go.Scatter(
    x=x_line, y=[y_mean] * len(x_line), mode="lines",
    line=dict(color="#64748b", width=2, dash="dash"),
    name=f"均值 Ȳ = {y_mean:.2f}（没有回归线时，你能做的最佳猜测）"
))

# 散点
fig1.add_trace(go.Scatter(
    x=x, y=y, mode="markers",
    marker=dict(size=9, color="#3b82f6", opacity=0.65),
    name="数据点"
))

# 每个点到均值线的竖直距离（隔几个点画）
step = 3
for i in range(0, n, step):
    fig1.add_trace(go.Scatter(
        x=[x[i], x[i]], y=[y[i], y_mean],
        mode="lines",
        line=dict(color="#ef4444", width=1.5),
        showlegend=(i == 0),
        name="到均值的距离（总变异）" if i == 0 else None,
        hoverinfo="skip",
    ))

ss_tot = np.sum((y - y_mean) ** 2)

fig1.update_layout(
    title=dict(
        text=f"<b>上：总变异</b>——每个点到<span style='color:#ef4444'>均值线</span>的距离平方和 = {ss_tot:.2f}",
        font=dict(size=15)
    ),
    xaxis=dict(title="X", zeroline=True, zerolinecolor="#555"),
    yaxis=dict(title="Y", zeroline=True, zerolinecolor="#555"),
    template="plotly_dark",
    height=420,
    margin=dict(l=50, r=30, t=60, b=50),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
)

# ============================================================
# 下排：残差 —— 每个点到回归线的距离
# ============================================================
fig2 = go.Figure()

# 均值水平线（做对比）
fig2.add_trace(go.Scatter(
    x=x_line, y=[y_mean] * len(x_line), mode="lines",
    line=dict(color="#64748b", width=2, dash="dash"),
    name=f"均值 Ȳ = {y_mean:.2f}"
))

# 回归线
fig2.add_trace(go.Scatter(
    x=x_line, y=a * x_line + b, mode="lines",
    line=dict(color="#22c55e", width=3),
    name=f"回归线 Ŷ = {a:.2f}X + {b:.2f}"
))

# 散点
fig2.add_trace(go.Scatter(
    x=x, y=y, mode="markers",
    marker=dict(size=9, color="#3b82f6", opacity=0.65),
    name="数据点"
))

# 每个点到回归线的竖直距离（残差）
for i in range(0, n, step):
    fig2.add_trace(go.Scatter(
        x=[x[i], x[i]], y=[y[i], y_pred[i]],
        mode="lines",
        line=dict(color="#f59e0b", width=1.5),
        showlegend=(i == 0),
        name="残差（回归线没解释掉的）" if i == 0 else None,
        hoverinfo="skip",
    ))

ss_res = np.sum((y - y_pred) ** 2)

fig2.update_layout(
    title=dict(
        text=f"<b>下：残差</b>——每个点到<span style='color:#f59e0b'>回归线</span>的距离平方和 = {ss_res:.2f}",
        font=dict(size=15)
    ),
    xaxis=dict(title="X", zeroline=True, zerolinecolor="#555"),
    yaxis=dict(title="Y", zeroline=True, zerolinecolor="#555"),
    template="plotly_dark",
    height=420,
    margin=dict(l=50, r=30, t=60, b=50),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
)

# ============================================================
# 组装成一个 HTML 页面，两张图上下排列
# ============================================================
import plotly.io as pio

html_top = pio.to_html(fig1, include_plotlyjs=True, full_html=False,
                       config=dict(responsive=True, displayModeBar=False))
html_bot = pio.to_html(fig2, include_plotlyjs=False, full_html=False,
                       config=dict(responsive=True, displayModeBar=False))

page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 20px 16px 40px;
    background: #0f172a;
    font-family: -apple-system, "Microsoft YaHei", sans-serif;
    color: #e2e8f0;
  }}
  .chart-wrap {{
    width: 100%;
    max-width: 900px;
    margin: 0 auto 8px auto;
  }}
  .formula-box {{
    max-width: 900px;
    margin: 16px auto;
    padding: 20px 24px;
    background: #1e293b;
    border-left: 3px solid #22c55e;
    border-radius: 4px;
    font-size: 17px;
    line-height: 2;
  }}
  .formula-box .big {{
    font-size: 22px;
    color: #f59e0b;
    font-weight: bold;
  }}
</style>
</head>
<body>
<div class="chart-wrap">{html_top}</div>

<div class="formula-box">
  <b>R² 的计算就是比较这两张图：</b><br><br>
  R² = 1 − <span style="color:#f59e0b">残差平方和</span> / <span style="color:#ef4444">总变异平方和</span><br>
  <span class="big">R² = 1 − {ss_res:.2f} / {ss_tot:.2f} = {r2:.3f}</span><br><br>
  <span style="color:#94a3b8;font-size:14px;">
  上图的红色距离大 → 数据本身就散 → 分母大<br>
  下图的黄色距离小 → 回归线收紧了 → 分子小<br>
  → R² = 0.{int(r2*1000):03d}，回归线解释了 {r2*100:.0f}% 的波动
  </span>
</div>

<div class="chart-wrap">{html_bot}</div>
</body>
</html>"""

out = r"D:\math_practice_file\b统计推断\m21_模型评估\m21_r2_how.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(page)

import webbrowser
webbrowser.open(out)
print(f"已保存: {out}")
