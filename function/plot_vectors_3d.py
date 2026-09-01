# -*- coding: utf-8 -*-
# plot_vectors_3d.py —— 画一组带名字的三维向量（基于 plotly）
#
# 和 plot_vectors.py 一样的功能，只是坐标从二维升到三维。
# 输入格式不变：字典组成的列表，每个字典 = {向量名: 坐标列表}
#   - 3 个数 [x, y, z]                 ：终点，默认起点 (0,0,0)
#   - 6 个数 [x1, y1, z1, x2, y2, z2]  ：起点 (x1,y1,z1)、终点 (x2,y2,z2)

import colorsys

import plotly.graph_objects as go


def plot_vectors_3d(vectors, title="向量图"):
    """画一组带名字的三维向量，名字标在向量末端。

    参数:
        vectors : list[dict]
            每个元素是 {向量名: 坐标列表}。坐标列表两种形式：
              [x, y, z]                 终点，默认起点 (0,0,0)
              [x1, y1, z1, x2, y2, z2]  起点 (x1,y1,z1)、终点 (x2,y2,z2)
        title   : str
            图顶部的标题

    例子:
        plot_vectors_3d([{"v1": [1, 2, 3]}, {"v2": [0, 0, 0, 1, 2, 3]}], title="测试")
    """
    if not vectors:
        raise ValueError("vectors 不能为空，至少给一个向量")

    names = []
    segs = []   # 每个元素 = (起点 [x,y,z], 终点 [x,y,z])
    for d in vectors:
        for name, val in d.items():
            if len(val) == 3:
                names.append(name)
                segs.append(([0, 0, 0], list(val)))   # 只有终点 → 默认起点原点
            elif len(val) == 6:
                names.append(name)
                segs.append((list(val[:3]), list(val[3:])))
            else:
                raise ValueError(
                    f"向量 {name} 的坐标长度必须是 3 或 6，收到的是 {len(val)}"
                )

    # 颜色算法和二维版 plot_vectors.py 一致：HSV 色相环均匀切成 n 份，
    # n 小 → 相邻颜色隔得远；n 大 → 隔得近；首尾不重复（第 1 个和第 n 个不会都是红）
    n = len(names)
    colors = [
        "#%02x%02x%02x" % tuple(int(c * 255) for c in colorsys.hsv_to_rgb(i / n, 1.0, 1.0))
        for i in range(n)
    ]

    fig = go.Figure()

    # 先算所有坐标的绝对最大值，用来定参考轴长度（四周留 1 的边）
    flat = [c for p1, p2 in segs for c in (p1 + p2)]
    rng = max((abs(c) for c in flat), default=1) + 1

    # 三根穿过原点的灰色虚线参考轴（对应二维版里的 axhline / axvline）
    ax_color = "gray"
    fig.add_trace(go.Scatter3d(
        x=[-rng, rng], y=[0, 0], z=[0, 0], mode="lines",
        line=dict(color=ax_color, width=2, dash="dash"), showlegend=False))
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[-rng, rng], z=[0, 0], mode="lines",
        line=dict(color=ax_color, width=2, dash="dash"), showlegend=False))
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[-rng, rng], mode="lines",
        line=dict(color=ax_color, width=2, dash="dash"), showlegend=False))

    for i, (name, (p1, p2)) in enumerate(zip(names, segs)):
        color = colors[i]
        x1, y1, z1 = p1
        x2, y2, z2 = p2

        # 箭头杆：一条从起点到终点的线段
        fig.add_trace(go.Scatter3d(
            x=[x1, x2], y=[y1, y2], z=[z1, z2], mode="lines",
            line=dict(color=color, width=6), showlegend=False))

        # 终点：用点标记，并把名字标在旁边（用点代替 3D 箭头头）
        fig.add_trace(go.Scatter3d(
            x=[x2], y=[y2], z=[z2], mode="markers+text", text=[name],
            marker=dict(color=color, size=2),
            textfont=dict(color=color, size=12), showlegend=False))

    fig.update_layout(
        title=title,
        scene=dict(
            aspectmode="data",   # 三轴等比例，向量不变形
            xaxis=dict(title="x"),
            yaxis=dict(title="y"),
            zaxis=dict(title="z"),
        ),
        showlegend=False,
    )

    fig.show()


if __name__ == "__main__":
    # 直接运行本文件时的自测：验证两种输入形式都能画、不报错
    plot_vectors_3d(
        [
            {"v1": [2, 0, 0]},          # 3 个数：默认起点原点，到 (2,0,0)
            {"v2": [0, 0, 0, 0, 1, 0]},  # 6 个数：从 (0,0,0) 到 (0,1,0)
            {"v3": [1, 1, 1, 3, 2, 3]},  # 6 个数：从 (1,1,1) 到 (3,2,3)
        ],
        title="自测：三维向量",
    )
