# -*- coding: utf-8 -*-
# plot_3d.py —— 三维画图工具（基于 plotly），干三件事：
#   1) plot_3d / plot_vectors_3d：画点 / 向量，可叠加在同一画布
#   2) plot_surface_3d：画二元函数 z = f(x, y) 的曲面
#
# 和二维版 plot.py 完全同构，只是坐标从二维升到三维：
#   统一入口 plot_3d(layers, ...)，layers 每层靠 type 区分：
#     {"type": "point",  "data": np.array([[x, y, z], ...]),  # 每行一个 xyz
#      "labels": [...], "color": ..., "s": ...}
#     {"type": "vector", "data": [{"v1": [x, y, z]}, ...]}    # 沿用旧数据结构
#
# point 层的 numpy 数组会自动补零：
#   - 1 个数 [x]            → (x, 0, 0)
#   - 2 个数 [x, y]         → (x, y, 0)
#   - 3 个数 [x, y, z]      → 原样
#
# 向量坐标两种形式：
#   - 3 个数 [x, y, z]                  ：终点，默认起点 (0,0,0)
#   - 6 个数 [x1, y1, z1, x2, y2, z2]   ：起点 (x1,y1,z1)、终点 (x2,y2,z2)

import colorsys

import numpy as np
import plotly.graph_objects as go


def _pad_to_3d(data):
    """把 point 层的 data 规整成 (n, 3) 矩阵，缺的维度补零。

    支持：标量（一个点）、一维数组（一个点）、二维矩阵（n 个点）。
    """
    pts = np.asarray(data, dtype=float)
    if pts.ndim == 0:            # 标量 → 一个点 (x, 0, 0)
        pts = pts.reshape(1, 1)
    elif pts.ndim == 1:          # [x] / [x, y] / [x, y, z] → 一个点
        pts = pts.reshape(1, -1)

    n, k = pts.shape
    if n == 0:
        raise ValueError("point 层的 data 不能为空")

    if k == 1:
        pts = np.pad(pts, ((0, 0), (0, 2)))   # → [x, 0, 0]
    elif k == 2:
        pts = np.pad(pts, ((0, 0), (0, 1)))   # → [x, y, 0]
    elif k == 3:
        pass
    else:
        raise ValueError(
            f"point 层每行的坐标维度必须是 1、2 或 3，收到的是 {k}"
        )
    return pts


def _draw_points_3d(fig, layer):
    """往 fig 上画一层三维散点，返回所有点坐标（用于自动定界）。"""
    pts = _pad_to_3d(layer["data"])

    labels = layer.get("labels")
    if labels is not None and len(labels) != len(pts):
        raise ValueError(
            f"labels 数量 ({len(labels)}) 要和点的数量 ({len(pts)}) 一致"
        )

    # 颜色 / 大小沿用二维版的习惯：color 默认 tab:blue 的 hex，s / size 都认
    color = layer.get("color", "#1f77b4")
    size = layer.get("s", layer.get("size", 2))

    mode = "markers+text" if labels is not None else "markers"
    fig.add_trace(go.Scatter3d(
        x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
        mode=mode, text=labels,
        marker=dict(color=color, size=size),
        showlegend=False,
    ))

    return [tuple(float(v) for v in p) for p in pts]


def _draw_vectors_3d(fig, layer):
    """往 fig 上画一层三维向量，返回用到的所有端点坐标（用于自动定界）。"""
    vectors = layer["data"]
    if not vectors:
        raise ValueError("vector 层的 data 不能为空，至少给一个向量")

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

    n = len(names)
    # 颜色算法和二维版一致：HSV 色相环均匀切成 n 份，首尾不重复
    colors = [
        "#%02x%02x%02x" % tuple(int(c * 255) for c in colorsys.hsv_to_rgb(i / n, 1.0, 1.0))
        for i in range(n)
    ]

    for i, (name, (p1, p2)) in enumerate(zip(names, segs)):
        color = colors[i]
        x1, y1, z1 = p1
        x2, y2, z2 = p2

        # 箭头杆：一条从起点到终点的线段
        fig.add_trace(go.Scatter3d(
            x=[x1, x2], y=[y1, y2], z=[z1, z2], mode="lines",
            line=dict(color=color, width=6), showlegend=False))

        # 终点：用点标记，并把名字标在旁边
        fig.add_trace(go.Scatter3d(
            x=[x2], y=[y2], z=[z2], mode="markers+text", text=[name],
            marker=dict(color=color, size=2),
            textfont=dict(color=color, size=12), showlegend=False))

    return [tuple(p1) for p1, p2 in segs] + [tuple(p2) for p1, p2 in segs]


# 类型 → 画图函数的分发表；以后加"线"等新类型，只需再写一个 _draw_*_3d 并在此登记
_DRAWERS_3D = {
    "point": _draw_points_3d,
    "vector": _draw_vectors_3d,
}


def _finalize_3d(fig, all_pts, title):
    """三根参考轴 + 自动定界 + 标题，只做一次。"""
    # 先算所有坐标的绝对最大值，用来定参考轴长度（四周留 1 的边）
    flat = [c for p in all_pts for c in p]
    rng = max((abs(c) for c in flat), default=1) + 1

    # 三根穿过原点的灰色虚线参考轴（对应二维版里的 axhline / axvline）
    ax_color = "gray"
    ax_x = go.Scatter3d(
        x=[-rng, rng], y=[0, 0], z=[0, 0], mode="lines",
        line=dict(color=ax_color, width=2, dash="dash"), showlegend=False)
    ax_y = go.Scatter3d(
        x=[0, 0], y=[-rng, rng], z=[0, 0], mode="lines",
        line=dict(color=ax_color, width=2, dash="dash"), showlegend=False)
    ax_z = go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[-rng, rng], mode="lines",
        line=dict(color=ax_color, width=2, dash="dash"), showlegend=False)

    # 参考轴先 add 到末尾，再整体挪到最底层，别盖住数据
    # （plotly 的 fig.data 只能整体重排，必须用 fig.data 里实际存的对象，不能插新建的 trace）
    fig.add_trace(ax_x)
    fig.add_trace(ax_y)
    fig.add_trace(ax_z)
    fig.data = fig.data[-3:] + fig.data[:-3]

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


def plot_3d(layers, title="图", show=True):
    """一个函数画三维点 / 向量，可叠加在同一画布（plotly）。

    参数:
        layers : list[dict]
            每个 dict 是一层，用 type 区分类型：
              {"type": "point",  "data": np.array([[x, y, z], ...]),
               "labels": [...], "color": "#1f77b4", "s": 8}
                data 是 (n, 3) 矩阵（也支持 (n,1)/(n,2)/标量/一维，自动补零到三维）
              {"type": "vector", "data": [{"v1": [x, y, z]}, ...]}
                data 沿用向量数据结构，每个 {名字: 坐标}，坐标 3 或 6 个数
        title : str
            图标题
        show : bool
            True 则画完直接 show

    返回:
        plotly.graph_objects.Figure

    例子:
        plot_3d([{"type": "point", "data": np.array([[1, 2, 3]])}])
        plot_3d([{"type": "vector", "data": [{"v1": [2, 0, 0]}]}])
        plot_3d([{"type": "vector", "data": [{"v1": [1, 0, 0]}]},
                 {"type": "point",  "data": np.array([[1, 1, 1]])}])
    """
    if not layers:
        raise ValueError("layers 不能为空，至少给一层")

    fig = go.Figure()

    all_pts = []
    for layer in layers:
        t = layer.get("type")
        if t not in _DRAWERS_3D:
            raise ValueError(
                f"未知的图层类型 {t!r}，目前支持：{sorted(_DRAWERS_3D)}"
            )
        all_pts += _DRAWERS_3D[t](fig, layer)

    _finalize_3d(fig, all_pts, title)
    if show:
        fig.show()
    return fig


def plot_vectors_3d(vectors, title="向量图"):
    """画一组带名字的三维向量（旧接口，内部走 plot_3d，签名不变）。

    参数:
        vectors : list[dict]
            每个元素是 {向量名: 坐标列表}。坐标列表两种形式：
              [x, y, z]                 终点，默认起点 (0,0,0)
              [x1, y1, z1, x2, y2, z2]  起点 (x1,y1,z1)、终点 (x2,y2,z2)
        title   : str

    例子:
        plot_vectors_3d([{"v1": [1, 2, 3]}, {"v2": [0, 0, 0, 1, 2, 3]}], title="测试")
    """
    return plot_3d([{"type": "vector", "data": vectors}], title=title)


def _check_range(rng, name):
    """校验一个 (min, max) 区间，返回规整成 float 的 (lo, hi)。"""
    try:
        lo, hi = rng
        lo, hi = float(lo), float(hi)
    except (TypeError, ValueError):
        raise ValueError(
            f"{name} 必须是 (min, max) 两个数，收到的是 {rng!r}"
        ) from None
    if not lo < hi:
        raise ValueError(f"{name} 要满足 min < max，收到的是 ({lo}, {hi})")
    return lo, hi


def _eval_grid(f, X, Y):
    """在网格 X、Y 上对 f 求值，返回和 X 同形状的 Z。

    f 的三种写法都认：
      - 整块吃数组（最快，numpy 的自然写法）→ 一次算完
      - 只吃标量（比如里面有 if x > 0:）────→ 自动退化成逐点算
      - 返回常数（比如 lambda x, y: 3）─────→ 自动铺满整个网格
    """
    try:
        Z = np.array(f(X, Y), dtype=float)
    except Exception:
        # f 不吃数组 → 逐点喂标量。n×n 个点，n 大时会明显变慢
        Z = np.empty(X.shape, dtype=float)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = f(X[i, j], Y[i, j])

    if Z.ndim == 0:                          # 返回标量 → 铺满
        Z = np.full(X.shape, float(Z))
    if Z.shape != X.shape:
        raise ValueError(
            f"f 在网格上算出的形状是 {Z.shape}，应该和网格 {X.shape} 一致"
        )
    return Z


def _mask_jumps(Z, factor=0.5):
    """把"跨过奇点"的采样点抹成 nan，让曲面在那里留洞。

    为什么不能只把 inf 换成 nan 就完事——奇点不一定正好落在采样点上：
      - 正好踩中：算出 inf → 上一步已经换成 nan 了
      - 夹在两个采样点中间：算出个巨大的**有限值**，上一步抓不到。
        plotly 会拿它去定 z 轴范围，整张曲面被压成一块平板。
        实测 1/(x*y) 在 n=60 时最大到 387，而函数正常值就在 ±1 附近。

    判据：相邻两点之差 > factor × 函数值的典型跨度（p99 - p1）。
    正常的陡函数（比如 x**10）相邻差再大也小于自己的跨度，不会误伤；
    跨过奇点的那一对差的是两个爆炸值，必定超标。

    factor 实测标定（n=60，窗口 ±3）：
      0.2 → 开始误删正常的 x**10（360 个点）
      0.5 → 奇点全压回合理范围，正常函数一个不删  ← 用它
      1.0 → 太松，tan 一个洞都不留
    """
    finite = Z[np.isfinite(Z)]
    if finite.size == 0:
        return Z
    span = np.percentile(finite, 99) - np.percentile(finite, 1)
    if not span > 0:
        return Z                     # 常数函数，没有跨度可比，直接放过
    thr = factor * span

    bad = np.zeros(Z.shape, dtype=bool)      # 含 nan 处的 diff 也是 nan，
                                             # nan > thr 为 False，不会误标

    dx = np.abs(np.diff(Z, axis=1)) > thr    # 沿 x 方向的相邻差
    bad[:, :-1] |= dx
    bad[:, 1:] |= dx                         # 跳变两侧都抹掉，洞才对称

    dy = np.abs(np.diff(Z, axis=0)) > thr    # 沿 y 方向同理
    bad[:-1, :] |= dy
    bad[1:, :] |= dy

    Z[bad] = np.nan
    return Z


def plot_surface_3d(f, x_range=(-3, 3), y_range=(-3, 3), n=60,
                    mask_jumps=True,
                    title="曲面", show=True, **surface_kwargs):
    """画二元函数 z = f(x, y) 的三维曲面（plotly）。

    参数:
        f : callable
            二元函数 f(x, y)。整块吃 numpy 数组最快；
            只吃标量（里面有 if 之类）也行，会自动退化成逐点算；
            返回常数也行，会自动铺成一个水平面。
        x_range : (xmin, xmax)
            x 的窗口，要求 xmin < xmax
        y_range : (ymin, ymax)
            y 的窗口，要求 ymin < ymax
        n : int
            每个方向的采样点数，网格是 n×n。至少 2，越大越平滑也越慢
        mask_jumps : bool
            True（默认）自动把跨过奇点的采样点抹成洞，细节见 _mask_jumps。
            不处理的话 1/(x*y)、tan(x) 这类函数的巨大值会把 z 轴拉到天上，
            整张曲面压成一块平板。正常函数不受影响，可以关掉对比看看。
        title : str
            图标题
        show : bool
            True 则画完直接 show
        **surface_kwargs
            透传给 plotly 的 go.Surface，
            比如 colorscale="Viridis"、opacity=0.9、showscale=False、contours=...

    返回:
        plotly.graph_objects.Figure（可以继续 add_trace 叠别的东西，见文件末尾示例）

    例子:
        plot_surface_3d(lambda x, y: x**2 + y**2)
        plot_surface_3d(lambda x, y: np.sin(x) * np.cos(y), n=100)
        plot_surface_3d(lambda x, y: 1 / (x * y), n=120)             # 奇点自动留洞
        plot_surface_3d(lambda x, y: 1 if x * y > 0 else 0)          # 只吃标量也能画
    """
    if not callable(f):
        raise ValueError(f"f 必须是个函数，收到的是 {type(f).__name__}")

    x_range = _check_range(x_range, "x_range")
    y_range = _check_range(y_range, "y_range")

    n = int(n)
    if n < 2:
        raise ValueError(f"n 至少是 2（少于 2 个点连不成面），收到的是 {n}")

    xs = np.linspace(x_range[0], x_range[1], n)
    ys = np.linspace(y_range[0], y_range[1], n)
    X, Y = np.meshgrid(xs, ys)

    Z = _eval_grid(f, X, Y)
    # 奇点算出的 ±inf 换成 nan → 曲面在那里留洞。
    # 不换的话 plotly 会拿 ±inf 去定 z 轴范围，整张曲面被压成一块平板。
    Z[~np.isfinite(Z)] = np.nan
    if mask_jumps:
        Z = _mask_jumps(Z)      # 奇点夹在两个采样点中间的情况，见 _mask_jumps

    fig = go.Figure(go.Surface(x=xs, y=ys, z=Z, **surface_kwargs))
    fig.update_layout(
        title=title,
        scene=dict(
            aspectmode="data",       # 三轴等比例，曲面不变形（和 _finalize_3d 一个道理）
            xaxis=dict(title="x"),
            yaxis=dict(title="y"),
            zaxis=dict(title="z"),
        ),
    )
    if show:
        fig.show()
    return fig


if __name__ == "__main__":
    # ---- plot_3d：画点 / 向量，可叠加在同一画布 ----
    plot_3d(
        [{"type": "vector", "data": [{"v1": [2, 0, 0]},
                                     {"v2": [0, 0, 0, 0, 1, 0]},
                                     {"v3": [1, 1, 1, 3, 2, 3]}]},
         {"type": "point",  "data": np.array([[1.0, 0.5, 0.0],
                                              [2.5, 1.0, 1.0],
                                              [3.0, 2.0, 2.0]])}],
        title="三维向量 + 点叠加",
    )

    # ---- plot_surface_3d：画二元函数 z = f(x, y) 的曲面。参数要点：----
    #   f               —— 直接传函数对象，不加括号
    #   x_range/y_range —— 定义域窗口，两边可以不一样大
    #   n               —— 每个方向采样点数，越大越平滑也越慢
    #   mask_jumps      —— 跨过奇点的采样点自动抹成洞（默认开）
    # 返回的 fig 还能继续 add_trace 往上叠东西（比如下降路径）
    plot_surface_3d(lambda x, y: np.sin(x) * np.cos(y),
                    x_range=(-2 * np.pi, 2 * np.pi),
                    y_range=(-2 * np.pi, 2 * np.pi),
                    n=100,
                    title="z = sin(x)·cos(y)")

