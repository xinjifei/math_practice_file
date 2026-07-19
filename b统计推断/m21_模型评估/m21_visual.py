"""m21 R² 与模型评估——渐进可视化教学
图表 1：R² ≈ 0.85（强相关）——线解释了大部分波动
图表 2：R² ≈ 0.10（弱相关）——线几乎没用
图表 3：R² ≈ 0.01（不相关）——线就是一条平均水平线
"""

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from scipy.stats import linregress

np.random.seed(42)
n = 60

# ============================================================
# 三组模拟数据：强 / 弱 / 无
# ============================================================
x = np.random.normal(0, 1, n)

# 强相关：Y ≈ 2X + 小噪音
y_strong = 2 * x + np.random.normal(0, 0.8, n)

# 弱相关：Y ≈ 0.5X + 大噪音
y_weak = 0.5 * x + np.random.normal(0, 2.5, n)

# 不相关：Y 纯噪音，跟 X 没关系
y_none = np.random.normal(0, 2, n)

datasets = [
    (x, y_strong, "#3b82f6", "强相关"),
    (x, y_weak, "#f59e0b", "弱相关"),
    (x, y_none, "#ef4444", "不相关"),
]

# ============================================================
# 三张子图
# ============================================================
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=("", "", ""),
    shared_yaxes=False,
)

for idx, (xi, yi, color, label) in enumerate(datasets):
    col = idx + 1
    res = linregress(xi, yi)
    a, b, r = res.intercept, res.slope, res.rvalue
    r2 = r ** 2

    x_line = np.linspace(xi.min(), xi.max(), 100)
    y_line = a + b * x_line

    # 散点
    fig.add_trace(go.Scatter(
        x=xi, y=yi, mode="markers",
        marker=dict(size=8, color=color, opacity=0.55),
        showlegend=False,
        hovertemplate="x: %{x:.2f}<br>y: %{y:.2f}<extra></extra>",
    ), row=1, col=col)

    # 回归线
    fig.add_trace(go.Scatter(
        x=x_line, y=y_line, mode="lines",
        line=dict(color=color, width=3),
        showlegend=False,
    ), row=1, col=col)

    # 标题直接写 R²
    subtitle = (
        f"<b>{label}</b><br>"
        f"<span style='font-size:20px;color:{color}'>R² = {r2:.3f}</span><br>"
        f"<span style='font-size:12px;color:#94a3b8'>X 解释了 Y 波动的 {r2*100:.0f}%</span>"
    )
    fig.add_annotation(
        xref="x domain", yref="y domain",
        x=0.5, y=1.08,
        text=subtitle,
        showarrow=False,
        font=dict(size=13),
        row=1, col=col,
    )

fig.update_layout(
    title=dict(
        text="<b>R² 告诉你回归线「有用」的程度</b>——从 0.81（好用）到 0.00（没用）",
        font=dict(size=16)
    ),
    template="plotly_dark",
    height=450,
    margin=dict(l=50, r=30, t=80, b=50),
)

# x/y 轴标签只能在子图上手动加
fig.update_xaxes(title_text="X", zeroline=True, zerolinecolor="#555", row=1, col=1)
fig.update_xaxes(title_text="X", zeroline=True, zerolinecolor="#555", row=1, col=2)
fig.update_xaxes(title_text="X", zeroline=True, zerolinecolor="#555", row=1, col=3)
fig.update_yaxes(title_text="Y", zeroline=True, zerolinecolor="#555", row=1, col=1)

out = r"D:\math_practice_file\b统计推断\m21_模型评估\m21_visual.html"
fig.write_html(out,
    include_plotlyjs=True,
    config=dict(responsive=True, displayModeBar=False),
)
print(f"已保存: {out}")

import webbrowser
webbrowser.open(out)
