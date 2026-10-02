# -*- coding: utf-8 -*-
# tmp.py —— 挑下降目标函数：4 个候选，一次跑完挑一个
#
# 你的三条要求：
#   ① 任何高度上的切面都是正圆
#   ② 看起来像个坑，最低点在 (0, 0)、z = 0
#   ③ 偏导你自己推得出来 —— 所以四个都保持简单
#
# 写法：四个候选全写成 f = g(x² + y²)。
#   只跟"离原点多远"有关 → 每个高度的切面必然是正圆
#   （连开方都不用，看的是平方和）。
#   将来放进你的代码里（参数是向量）时，把 x² + y² 换成 Σwᵢ² 就完事了，四个都适用。
#
# 跑法：在项目根目录执行  python c_1梯度下降/tmp.py
#   依次弹 4 个窗口，一个候选一张，关掉一个看下一个。
#   窗口想放大缩小就改下面的 x_range / z_range。

import numpy as np
from function.plot_3d import plot_surface_3d


# ---- 候选 1：抛物面。最简的碗 ----
def bowl(x, y):
    return x**2 + y**2


# ---- 候选 2：四次碗。坑底特别平 ----
def quartic_bowl(x, y):
    r2 = x**2 + y**2
    return r2**2


# ---- 候选 3：真坑。平底 → 陡壁 → 平沿 ----
def well(x, y):
    r2 = x**2 + y**2
    return 1 - np.exp(-r2)


# ---- 候选 4：宽底坑。坑底更宽更平 ----
def wide_well(x, y):
    r2 = x**2 + y**2
    return 1 - np.exp(-r2**2)


CANDIDATES = [
    {
        "n": 1,
        "label": "抛物面",
        "f": bowl,
        "formula": "f = x^2 + y^2",
        "x_range": (0, 1.5),
        "z_range": (0, 5),
        "shape": "一个匀称的碗。底不平、沿不缓，从底往外一路变陡 —— 只有「慢→快」两段，没有第三段。"
                 "好处是你要的每一样它都占，而且导数最短。",
    },
    {
        "n": 2,
        "label": "四次碗",
        "f": quartic_bowl,
        "formula": "f = (x^2 + y^2)^2",
        "x_range": (0, 1.0),
        "z_range": (0, 4),
        "shape": "坑底平得夸张（贴着原点几乎不动），一出中心就猛地陡起来 —— 还是「慢→快」两段，"
                 "但第一段比候选 1 长得多。全程不下沉到负值，最低点稳稳在原点。",
    },
    {
        "n": 3,
        "label": "真坑",
        "f": well,
        "formula": "f = 1 - e^-(x^2 + y^2)",
        "x_range": (0, 1.5),
        "z_range": (0, 1.1),
        "shape": "三段的「慢→快→慢」全在：坑底圆润平缓，中段最陡，出了中段又渐渐摊平，"
                 "外围是一片高度 ≈ 1 的平地 —— 这才是地上那种坑。"
                 "代价是多一个 e，链式法则多套一层。",
    },
    {
        "n": 4,
        "label": "宽底坑",
        "f": wide_well,
        "formula": "f = 1 - e^-(x^2 + y^2)^2",
        "x_range": (0, 2.0),
        "z_range": (0, 1.1),
        "shape": "和候选 3 同族，但坑底宽得多、平得多：离原点还有一段距离时几乎还是零，"
                 "之后才突然陡起来，最后同样摊平成平地。想看得见「快到底时走不动」就选它。",
    },
]


# 不同半径上的高度。看相邻两列的差——差小的那一段就是「慢」。
RADII = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]

print("离原点的半径 r  →")
print(f"{'':<6}" + "".join(f"{r:>9.2f}" for r in RADII))
print("-" * (6 + 9 * len(RADII)))
for c in CANDIDATES:
    vals = [float(c["f"](r, 0.0)) for r in RADII]
    print(f"{c['n']:<6}" + "".join(f"{v:>9.4f}" for v in vals))
print("（每行是同一个候选，从左到右越走越远；两列之间差得越少 = 那一段越平）\n")


for c in CANDIDATES:
    title = f"候选 {c['n']} · {c['label']}   {c['formula']}"
    print(f"\n===== {title} =====")
    print(f"形状：{c['shape']}")
    plot_surface_3d(c["f"],
                    x_range=c["x_range"],
                    z_range=c["z_range"],
                    n=140,
                    title=title)
