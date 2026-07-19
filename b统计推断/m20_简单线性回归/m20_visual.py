"""m20 简单线性回归——渐进可视化教学
图表 1：只有散点——你能看出 X 和 Y 的关系吗？
图表 2：一条烂线 vs 一条好线——什么叫"更接近"？
图表 3：回归线 + 残差——最小二乘法到底最小化了什么？
图表 4：三个不同斜率——b=1.2 / 0.3 / -0.5 各长什么样？
输出：单个 HTML 页面，4 张图满宽竖向排列
"""

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from scipy.stats import linregress

# ============================================================
# 模拟数据
# ============================================================
np.random.seed(42)
n = 60
market_return = np.random.normal(0.0005, 0.015, n)

true_beta = 1.1
true_alpha = 0.0002
noise = np.random.normal(0, 0.008, n)
stock_return = true_alpha + true_beta * market_return + noise

res = linregress(market_return, stock_return)
b, a = res.slope, res.intercept
x_line = np.linspace(market_return.min(), market_return.max(), 100)
y_line = a + b * x_line

bad_slope = -0.5
bad_intercept = 0.002
y_bad = bad_intercept + bad_slope * x_line

step = 5
residual_x = market_return[::step]
residual_y = stock_return[::step]
residual_y_pred = a + b * residual_x

# ============================================================
# 图表 1：只有散点
# ============================================================
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=market_return, y=stock_return, mode="markers",
    marker=dict(size=9, color="#3b82f6", opacity=0.7),
    name="每日收益率",
    hovertemplate="大盘: %{x:.2%}<br>个股: %{y:.2%}<extra></extra>"
))
fig1.update_layout(
    title=dict(text="<b>图1：只看数据</b>——沪深300 vs 个股 日收益率", font=dict(size=16)),
    xaxis=dict(title="沪深300 日收益率", tickformat=".1%", zeroline=True, zerolinecolor="#555"),
    yaxis=dict(title="个股 日收益率", tickformat=".1%", zeroline=True, zerolinecolor="#555"),
    template="plotly_dark",
    height=500,
    margin=dict(l=60, r=30, t=60, b=60),
)

# ============================================================
# 图表 2：烂线 vs 好线
# ============================================================
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=market_return, y=stock_return, mode="markers",
    marker=dict(size=9, color="#94a3b8", opacity=0.6),
    name="数据点"
))
fig2.add_trace(go.Scatter(
    x=x_line, y=y_bad, mode="lines",
    line=dict(color="#ef4444", width=2.5, dash="dash"),
    name="烂线（斜率-0.5，方向都反了）"
))
fig2.add_trace(go.Scatter(
    x=x_line, y=y_line, mode="lines",
    line=dict(color="#22c55e", width=3),
    name=f"回归线（b={b:.2f}，最小二乘）"
))
fig2.update_layout(
    title=dict(text="<b>图2：哪条线更好？</b>——绿线比红线更'接近'所有点", font=dict(size=16)),
    xaxis=dict(title="沪深300 日收益率", tickformat=".1%", zeroline=True, zerolinecolor="#555"),
    yaxis=dict(title="个股 日收益率", tickformat=".1%", zeroline=True, zerolinecolor="#555"),
    template="plotly_dark",
    height=500,
    margin=dict(l=60, r=30, t=60, b=60),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
)

# ============================================================
# 图表 3：回归线 + 残差
# ============================================================
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=x_line, y=y_line, mode="lines",
    line=dict(color="#22c55e", width=3),
    name=f"Ŷ = {a:.4f} + {b:.2f}·X"
))
fig3.add_trace(go.Scatter(
    x=market_return, y=stock_return, mode="markers",
    marker=dict(size=9, color="#3b82f6", opacity=0.7),
    name="实际值 Yᵢ"
))
for i in range(len(residual_x)):
    fig3.add_trace(go.Scatter(
        x=[residual_x[i], residual_x[i]],
        y=[residual_y[i], residual_y_pred[i]],
        mode="lines",
        line=dict(color="#f59e0b", width=1.5),
        showlegend=(i == 0),
        name="残差（竖直距离）" if i == 0 else None,
        hoverinfo="skip"
    ))
    fig3.add_trace(go.Scatter(
        x=[residual_x[i]], y=[residual_y_pred[i]],
        mode="markers",
        marker=dict(size=5, color="#f59e0b"),
        showlegend=False,
        hoverinfo="skip"
    ))
fig3.update_layout(
    title=dict(
        text="<b>图3：最小二乘法</b>——最小化这些<span style='color:#f59e0b'>黄色竖线</span>的<span style='color:#f59e0b'>平方和</span>",
        font=dict(size=16)
    ),
    xaxis=dict(title="沪深300 日收益率", tickformat=".1%", zeroline=True, zerolinecolor="#555"),
    yaxis=dict(title="个股 日收益率", tickformat=".1%", zeroline=True, zerolinecolor="#555"),
    template="plotly_dark",
    height=500,
    margin=dict(l=60, r=30, t=60, b=60),
)

# ============================================================
# 图表 4：三个不同 Beta
# ============================================================
fig4 = make_subplots(rows=1, cols=3,
    subplot_titles=(
        "<b>b = 1.2 高 Beta</b><br>大盘+1% → 个股+1.2%",
        "<b>b = 0.3 低 Beta</b><br>大盘+1% → 个股+0.3%",
        "<b>b = −0.5 负 Beta</b><br>大盘+1% → 个股−0.5%"
    ),
    shared_yaxes=True,
)

betas = [1.2, 0.3, -0.5]
colors = ["#ef4444", "#f59e0b", "#22c55e"]

for idx, (beta, color) in enumerate(zip(betas, colors)):
    col = idx + 1
    y_sim = 0.0002 + beta * market_return + np.random.normal(0, 0.006, n)
    fig4.add_trace(go.Scatter(
        x=market_return, y=y_sim, mode="markers",
        marker=dict(size=7, color=color, opacity=0.6),
        showlegend=False,
    ), row=1, col=col)
    r = linregress(market_return, y_sim)
    y_fit = r.intercept + r.slope * x_line
    fig4.add_trace(go.Scatter(
        x=x_line, y=y_fit, mode="lines",
        line=dict(color=color, width=3),
        showlegend=False,
    ), row=1, col=col)
    fig4.add_trace(go.Scatter(
        x=x_line, y=x_line,
        mode="lines",
        line=dict(color="#666", width=1, dash="dot"),
        showlegend=False,
    ), row=1, col=col)

fig4.update_layout(
    title=dict(text="<b>图4：斜率 b 就是 Beta</b>——个股对大盘的敏感度", font=dict(size=16)),
    template="plotly_dark",
    height=450,
    margin=dict(l=60, r=30, t=80, b=60),
)
fig4.update_xaxes(title_text="大盘", tickformat=".1%", row=1, col=1)
fig4.update_xaxes(title_text="大盘", tickformat=".1%", row=1, col=2)
fig4.update_xaxes(title_text="大盘", tickformat=".1%", row=1, col=3)
fig4.update_yaxes(title_text="个股", tickformat=".1%", row=1, col=1)

# ============================================================
# 组装成一个 HTML 页面
# ============================================================
# fig1 内嵌 plotly.js（避免 CDN 被墙），其余只输出图表 div
html_fig1 = pio.to_html(
    fig1, include_plotlyjs=True, full_html=False,
    config=dict(responsive=True, displayModeBar=False)
)
html_rest = []
for fig in [fig2, fig3, fig4]:
    html_rest.append(pio.to_html(
        fig, include_plotlyjs=False, full_html=False,
        config=dict(responsive=True, displayModeBar=False)
    ))

page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 24px 16px;
    background: #0f172a;
    font-family: -apple-system, "Microsoft YaHei", sans-serif;
  }}
  .chart-wrap {{
    width: 100%;
    max-width: 1000px;
    margin: 0 auto 12px auto;
  }}
  .chart-wrap .plotly-graph-div,
  .chart-wrap .js-plotly-plot {{
    width: 100% !important;
  }}
  @media (min-width: 1200px) {{
    .chart-wrap {{ max-width: 1100px; }}
  }}
</style>
</head>
<body>
<div class="chart-wrap">{html_fig1}</div>
<div class="chart-wrap">{html_rest[0]}</div>
<div class="chart-wrap">{html_rest[1]}</div>
<div class="chart-wrap">{html_rest[2]}</div>
</body>
</html>"""

out_path = r"D:\math_practice_file\b统计推断\m20_简单线性回归\m20_charts.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(page)

import webbrowser
webbrowser.open(out_path)
print(f"已打开: {out_path}")
