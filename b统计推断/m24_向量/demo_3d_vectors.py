"""
3D 向量可视化：国王 / 皇后 / 男乞丐 / 女乞丐
x=男人程度（正=男, 负=女）, y=财富（正=富, 负=穷）, z=皇室程度（正=贵族, 负=底层）
"""
import plotly.graph_objects as go
import numpy as np

#               x(男)  y(富)  z(贵)
king     = np.array([ 0.9,  0.7,  0.9])   # 国王: 男+, 富+, 贵+
queen    = np.array([-0.9,  0.7,  0.9])   # 皇后: 男-(=女), 富+, 贵+
beggar_m = np.array([ 0.9, -0.7, -0.9])   # 男乞丐: 男+, 富-, 贵-
beggar_f = np.array([-0.9, -0.7, -0.9])   # 女乞丐: 男-(=女), 富-, 贵-

def add_vector(fig, vec, color, name):
    """往 fig 里添加一条从原点出发的 3D 向量"""
    fig.add_trace(go.Scatter3d(
        x=[0, vec[0]], y=[0, vec[1]], z=[0, vec[2]],
        mode='lines+markers',
        marker=dict(size=[0, 6], color=color),
        line=dict(color=color, width=6),
        name=f'{name} [{vec[0]:.1f}, {vec[1]:.1f}, {vec[2]:.1f}]'
    ))

fig = go.Figure()
add_vector(fig, king,     'gold',        '国王')
add_vector(fig, queen,    'crimson',     '皇后')
add_vector(fig, beggar_m, 'saddlebrown', '男乞丐')
add_vector(fig, beggar_f, 'darkorange',  '女乞丐')

fig.update_layout(
    title='3D 词向量空间',
    scene=dict(
        xaxis=dict(title='男人程度', range=[-1, 1]),
        yaxis=dict(title='财富',     range=[-1, 1]),
        zaxis=dict(title='皇室程度', range=[-1, 1]),
        aspectmode='cube',
    ),
    width=900,
    height=750,
    margin=dict(l=20, r=20, t=50, b=20),
)

fig.show()
