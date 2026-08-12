"""
Demo: 2D 向量可视化 + 长度计算（Plotly 版）
功能同 demo_vectors.py，改用 plotly——图表可交互（缩放、悬停看坐标）。
"""
import plotly.graph_objects as go
import numpy as np

# ===== 画多个向量 =====

# 创建每条箭头的注释标签
vectors = [(3, 2), (-1, 4), (0, -3)]
colors = ['blue', 'green', 'purple']

# go.Figure() — 创建一个空图表对象，之后往里加"轨迹"（trace）
fig = go.Figure()

for (x, y), color in zip(vectors, colors):
    # go.Scatter 画线（mode='lines+markers' = 线 + 端点标记）
    # x=[0, x] — 从原点到 (x, y) 的线段
    # y=[0, y]
    # marker=[dict(size=0), dict(size=8)] — 起点不画点，终点画大点→箭头来指示方向
    # line=dict(width=3) — 线宽
    fig.add_trace(go.Scatter(
        x=[0, x],
        y=[0, y],
        mode='lines+markers',
        marker=dict(
            size=[0, 8],           # 起点 0（不显示），终点 8px 圆点
            color=color,   # 终点颜色（起点 size=0 不显示）
            symbol='arrow',        # 终点用箭头形状（plotly 内置 arrow 符号）
            angleref='previous'    # 箭头方向指向线的来向（即从起点来的方向）
        ),
        line=dict(color=color, width=3),
        name=f'[{x}, {y}]'  # 图例中显示的名称
    ))

# ===== 设置坐标轴 =====
fig.add_hline(y=0, line=dict(color='gray', dash='dash', width=1))
fig.add_vline(x=0, line=dict(color='gray', dash='dash', width=1))

fig.update_xaxes(range=[-5, 5], title='x')
fig.update_yaxes(range=[-5, 5], title='y')

# 等比例坐标轴——1 单位在 x 和 y 轴上一样长，否则箭头角度会变形
fig.update_layout(
    title='2D 向量可视化',
    xaxis=dict(scaleanchor='y', scaleratio=1),  # x 轴单位 = y 轴单位
    width=600,
    height=600,
)

fig.show()

# ===== 计算向量长度 =====
def vector_length(x, y):
    """返回向量 [x, y] 的长度 = √(x²+y²)"""
    return np.sqrt(x**2 + y**2)

print("向量长度：")
for x, y in vectors:
    length = vector_length(x, y)
    print(f"  [{x:>2}, {y:>2}] 长度 = √({x}² + {y}²) = {length:.3f}")

longest = max(vectors, key=lambda v: vector_length(v[0], v[1]))
print(f"\n最长的是 {longest}，长度 = {vector_length(*longest):.3f}")
