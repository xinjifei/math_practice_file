# -*- coding: utf-8 -*-
# plot.py —— 一个函数画点 / 向量 / 线（可叠加在同一画布）
#
# 统一入口 plot(layers, ...)，layers 每层靠 type 区分：
#   {"type": "point",  "data": np.array([[x, y], ...]),  # 每行一个 xy
#    "labels": [...], "color": ..., "s": ...}
#   {"type": "vector", "data": [{"v1": [2, 0]}, ...]}    # 沿用旧数据结构
#   {"type": "line",   "data": np.array([[x, y], ...]),  # 每行一个顶点，按行顺序连
#    "color": 不传则自动配色, "linestyle": 默认 "--", "linewidth": 默认 2}
#
# 向量坐标两种形式：
#   - 2 个数 [x, y]            ：终点，默认起点 (0,0)
#   - 4 个数 [x1, y1, x2, y2]  ：起点 (x1,y1)、终点 (x2,y2)  ← 后两个是终点，不是差值

import numpy as np
import matplotlib.pyplot as plt

# 让中文标题能正常显示（不设的话中文会变方块）
# 坑：SimHei 是 Windows 字体，macOS 上根本没装 —— 只写它一个，Mac 上就找不到字体、中文全变方框。
# 所以给一串候选，matplotlib 会跳过没装的、用第一个装了的。
# 顺序：macOS → Windows → Linux → 兜底。matplotlib 3.6+ 支持逐字回退，列表长一点没坏处。
plt.rcParams['font.sans-serif'] = [
    'PingFang SC', 'Hiragino Sans GB', 'Songti SC', 'Heiti SC',   # macOS
    'Microsoft YaHei', 'SimHei',                                   # Windows
    'Noto Sans CJK SC', 'WenQuanYi Micro Hei',                     # Linux
    'Arial Unicode MS',                                            # 兜底
]
plt.rcParams['axes.unicode_minus'] = False

# 没指定颜色时的自动配色：hsv 把色相环均分成 8 份（和向量层同一套思路，
# 只是向量层按本层向量个数分，线层按"画布上已经是第几条线"取）
_AUTO_COLORS = plt.cm.hsv(np.linspace(0, 1, 8, endpoint=False))


def _draw_vectors(ax, layer):
    """往 ax 上画一层向量，返回用到的所有 (x, y) 坐标（用于自动定界）。"""
    vectors = layer["data"]
    if not vectors:
        raise ValueError("vector 层的 data 不能为空，至少给一个向量")

    names = []      # 存向量名
    coords = []     # 统一存成 [x1, y1, x2, y2]
    for d in vectors:
        for name, val in d.items():
            if len(val) == 2:
                names.append(name)
                coords.append([0, 0, val[0], val[1]])   # 只有终点 → 默认起点 (0,0)
            elif len(val) == 4:
                names.append(name)
                coords.append(val)                       # 已经是 [起点, 终点]
            else:
                raise ValueError(
                    f"向量 {name} 的坐标长度必须是 2 或 4，收到的是 {len(val)}"
                )

    n = len(names)
    # 颜色按数量自动生成：hsv 把色相环均匀切成 n 份
    colors = plt.cm.hsv(np.linspace(0, 1, n, endpoint=False))

    for i in range(n):
        x1, y1, x2, y2 = coords[i]
        # quiver 的第 3、4 个参数是"位移"（终点 − 起点），所以要自己算差值
        ax.quiver(x1, y1, x2 - x1, y2 - y1,
                  angles="xy", scale_units="xy", scale=1,
                  color=colors[i])
        ax.text(x2, y2, names[i])          # 名字标在向量末端（终点）

    # 起点 + 终点都算进定界范围
    return [(c[0], c[1]) for c in coords] + [(c[2], c[3]) for c in coords]


def _draw_points(ax, layer):
    """往 ax 上画一层点，返回所有点坐标（用于自动定界）。"""
    pts = np.asarray(layer["data"])
    if pts.ndim != 2 or pts.shape[1] != 2:
        raise ValueError(
            f"point 层的 data 必须是 (n, 2) 矩阵，每行一个 [x, y]，收到形状 {pts.shape}"
        )
    if pts.shape[0] == 0:
        raise ValueError("point 层的 data 不能为空")
    if not np.issubdtype(pts.dtype, np.number):
        raise ValueError(f"point 层的 data 必须是数值，收到 dtype {pts.dtype}")

    labels = layer.get("labels")
    if labels is not None and len(labels) != len(pts):
        raise ValueError(
            f"labels 数量 ({len(labels)}) 要和点的数量 ({len(pts)}) 一致"
        )

    # 除 type/data/labels 外的键都透传给 scatter，并给默认值
    scatter_kwargs = {k: v for k, v in layer.items()
                      if k not in ("type", "data", "labels")}
    if "color" not in scatter_kwargs and "c" not in scatter_kwargs:
        scatter_kwargs["color"] = "tab:blue"
    scatter_kwargs.setdefault("s", 40)

    ax.scatter(pts[:, 0], pts[:, 1], **scatter_kwargs)

    if labels is not None:
        for (x, y), name in zip(pts, labels):
            ax.text(x, y, name)

    return [(float(x), float(y)) for x, y in pts]


def _draw_lines(ax, layer):
    """往 ax 上画一层折线，返回所有顶点坐标（用于自动定界）。"""
    pts = np.asarray(layer["data"])
    if pts.ndim != 2 or pts.shape[1] != 2:
        raise ValueError(
            f"line 层的 data 必须是 (n, 2) 矩阵，每行一个 [x, y]，收到形状 {pts.shape}"
        )
    if not np.issubdtype(pts.dtype, np.number):
        raise ValueError(f"line 层的 data 必须是数值，收到 dtype {pts.dtype}")
    if pts.shape[0] < 2:
        raise ValueError(f"line 层至少要 2 个点才画得出一条线，收到 {pts.shape[0]} 个")

    # 除 type/data 外的键都透传给 plot，并给默认值
    line_kwargs = {k: v for k, v in layer.items()
                   if k not in ("type", "data")}
    if "color" not in line_kwargs:
        # 取色相环上的下一个颜色：连续加几层线时颜色不会撞
        line_kwargs["color"] = _AUTO_COLORS[len(ax.lines) % len(_AUTO_COLORS)]
    line_kwargs.setdefault("linestyle", "--")
    line_kwargs.setdefault("linewidth", 2)

    ax.plot(pts[:, 0], pts[:, 1], **line_kwargs)

    return [(float(x), float(y)) for x, y in pts]


# 类型 → 画图函数的分发表；以后再加新类型，只需再写一个 _draw_* 并在此登记
_DRAWERS = {
    "point": _draw_points,
    "vector": _draw_vectors,
    "line": _draw_lines,
}


def _finalize(ax, all_pts, title):
    """参考轴 + 网格 + 自动定界 + 标题，只做一次。"""
    ax.axhline(0, color="gray", linestyle="--")
    ax.axvline(0, color="gray", linestyle="--")
    ax.grid(True)

    if all_pts:
        xs = [p[0] for p in all_pts]
        ys = [p[1] for p in all_pts]
        pad = 1
        ax.set_xlim(min(xs) - pad, max(xs) + pad)
        ax.set_ylim(min(ys) - pad, max(ys) + pad)

    ax.set_title(title)


def plot(layers, title="图", ax=None, show=True):
    """一个函数画点 / 向量 / 线，可叠加在同一画布。

    参数:
        layers : list[dict]
            每个 dict 是一层，用 type 区分类型：
              {"type": "point",  "data": np.array([[x, y], ...]),
               "labels": [...], "color": "tab:blue", "s": 40}
                data 是 (n, 2) 矩阵，每行一个 [x, y]
              {"type": "vector", "data": [{"v1": [2, 0]}, ...]}
                data 沿用向量数据结构，每个 {名字: 坐标}，坐标 2 或 4 个数
              {"type": "line",   "data": np.array([[x, y], ...]),
               "color": None, "linestyle": "--", "linewidth": 2}
                data 是 (n, 2) 矩阵，每行一个顶点，按行顺序连成一条折线（至少 2 个点）；
                color 不传则自动从 hsv 色相环取色，linestyle 不传则默认虚线
        title : str
            图标题
        ax : matplotlib.axes.Axes 或 None
            指定画布；None 则用当前坐标轴
        show : bool
            True 则画完直接 show

    例子:
        plot([{"type": "point", "data": np.array([[1, 0.5], [2.5, 1]])}])
        plot([{"type": "vector", "data": [{"v1": [2, 0]}]}])
        plot([{"type": "vector", "data": [{"v1": [2, 0]}]},
              {"type": "point",  "data": np.array([[1, 0.5]])}])
        plot([{"type": "line",   "data": np.array([[0, 0], [1, 2], [3, 1]]),
               "color": "tab:green", "linestyle": "--"}])
    """
    if not layers:
        raise ValueError("layers 不能为空，至少给一层")

    if ax is None:
        ax = plt.gca()

    all_pts = []
    for layer in layers:
        t = layer.get("type")
        if t not in _DRAWERS:
            raise ValueError(
                f"未知的图层类型 {t!r}，目前支持：{sorted(_DRAWERS)}"
            )
        all_pts += _DRAWERS[t](ax, layer)

    _finalize(ax, all_pts, title)
    if show:
        plt.show()
    return ax


def plot_vectors(vectors, title="向量图"):
    """画一组带名字的向量（旧接口，内部走 plot，签名不变）。

    参数:
        vectors : list[dict]
            每个元素是 {向量名: 坐标列表}。坐标列表两种形式：
              [x, y]             终点，默认起点 (0,0)
              [x1, y1, x2, y2]   起点 (x1,y1)、终点 (x2,y2)
        title   : str

    例子:
        plot_vectors([{"v1": [2, 0]}, {"v2": [0, 0, 4, 0]}], title="测试")
    """
    return plot([{"type": "vector", "data": vectors}], title=title)


if __name__ == "__main__":
    # 自测：向量 + 线 + 点叠加，验证三种 type 能画到同一画布
    plot(
        [{"type": "vector", "data": [{"v1": [2, 0]},
                                     {"v2": [0, 0, 0, 1]},
                                     {"v3": [1, 1, 3, 2]}]},
         {"type": "line",   "data": np.array([[0.0, 0.0],
                                              [1.0, 2.0],
                                              [2.5, 0.5]])},
         {"type": "line",   "data": np.array([[-1.0, 1.0],
                                              [0.5, -0.5],
                                              [2.0, 1.5]])},
         {"type": "point",  "data": np.array([[1.0, 0.5],
                                              [2.5, 1.0],
                                              [3.0, 2.0]])}],
        title="自测：向量 + 线 + 点叠加",
    )
