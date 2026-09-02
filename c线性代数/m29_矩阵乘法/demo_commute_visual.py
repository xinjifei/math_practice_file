# -*- coding: utf-8 -*-
"""
demo_commute_visual.py —— 图解：矩阵乘法为什么有时可交换、有时不可交换

核心思想：同一个向量 v 走两条路，看终点合不合。
  蓝路（先 B 后 A）：v → B@v → A@(B@v) = (A@B)@v
  红路（先 A 后 B）：v → A@v → B@(A@v) = (B@A)@v

  两条路的终点重合 → 顺序无所谓 → 可交换
  两条路的终点分开 → 顺序重要   → 不可交换

画法沿用 function/plot_vectors.py 的风格：灰色虚线参考轴 + 网格 + SimHei 中文。
"""
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 两个固定颜色：蓝 = 先B后A，红 = 先A后B
BLUE = "#2578b3"
RED = "#dd2424"


def draw_case(ax, A, B, v, name_A, name_B, title):
    """在一个子图上画一个 case：v 走蓝、红两条路。

    A, B  : 两个 2x2 矩阵
    v     : 原始向量 [x, y]
    name_A, name_B : 两个矩阵的短名，用来标中间步骤
    """
    v = np.array(v, dtype=float)

    # —— 算两条路的中间点和终点 ——
    Bv = B @ v            # 蓝路中间点：先做 B
    ABv = A @ Bv          # 蓝路终点：再做 A = (A@B)@v
    Av = A @ v            # 红路中间点：先做 A
    BAv = B @ Av          # 红路终点：再做 B = (B@A)@v

    # —— 画原始向量 v（灰色虚线，从原点到 v）——
    ax.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1,
              color='gray', linestyle='--', width=0.006)

    # —— 蓝路：先 B 后 A（两段首尾相接的实线箭头）——
    ax.quiver(v[0], v[1], Bv[0] - v[0], Bv[1] - v[1],
              angles='xy', scale_units='xy', scale=1, color=BLUE, width=0.006)
    ax.quiver(Bv[0], Bv[1], ABv[0] - Bv[0], ABv[1] - Bv[1],
              angles='xy', scale_units='xy', scale=1, color=BLUE, width=0.006)

    # —— 红路：先 A 后 B ——
    ax.quiver(v[0], v[1], Av[0] - v[0], Av[1] - v[1],
              angles='xy', scale_units='xy', scale=1, color=RED, width=0.006)
    ax.quiver(Av[0], Av[1], BAv[0] - Av[0], BAv[1] - Av[1],
              angles='xy', scale_units='xy', scale=1, color=RED, width=0.006)

    # —— 标中间步骤（"先做的人"动了什么）——
    ax.text(Bv[0], Bv[1], f' {name_B}', color=BLUE, fontsize=8, alpha=0.75)
    ax.text(Av[0], Av[1], f' {name_A}', color=RED, fontsize=8, alpha=0.75)
    ax.text(v[0], v[1], ' v', color='gray', fontsize=9)

    # —— 标两个终点（蓝点 vs 红点）——
    same = np.allclose(ABv, BAv)
    ax.plot(ABv[0], ABv[1], 'o', color=BLUE, markersize=9, zorder=5)
    ax.plot(BAv[0], BAv[1], 'o', color=RED, markersize=9, zorder=5)
    if not same:
        # 不重合时，各自标坐标，学生一眼看出"差在哪"
        ax.text(ABv[0], ABv[1], f' ({ABv[0]:.0f},{ABv[1]:.0f})', color=BLUE, fontsize=8)
        ax.text(BAv[0], BAv[1], f' ({BAv[0]:.0f},{BAv[1]:.0f})', color=RED, fontsize=8)

    # —— 结论写进标题 ——
    conclusion = '终点重合 → 可交换' if same else '终点分开 → 不可交换'
    ax.set_title(f'{title}\n{conclusion}', fontsize=11)

    # —— 参考轴 + 网格 + 等比例 ——
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    ax.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    ax.grid(True, linewidth=0.4)
    ax.set_aspect('equal')

    # —— 自动定范围，四周留 1.2 的边 ——
    pts = np.array([v, Bv, ABv, Av, BAv])
    pad = 1.2
    ax.set_xlim(pts[:, 0].min() - pad, pts[:, 0].max() + pad)
    ax.set_ylim(pts[:, 1].min() - pad, pts[:, 1].max() + pad)


fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 情况1：拉伸x × 翻转y —— 对角×对角，可交换（你第1题错的那个）
draw_case(axes[0, 0],
          A=np.array([[2, 0], [0, 1]]),      # 拉 x 两倍
          B=np.array([[1, 0], [0, -1]]),     # 翻 y
          v=[2, 1], name_A='拉x', name_B='翻y',
          title='① 拉伸x × 翻转y')

# 情况2：旋转90° × 非均匀拉伸 —— 不可交换（你第2题对的那个）
draw_case(axes[0, 1],
          A=np.array([[0, -1], [1, 0]]),     # 旋转 90°
          B=np.array([[3, 0], [0, 2]]),      # 拉 x 三倍、y 两倍（不均匀）
          v=[1, 1], name_A='旋转90°', name_B='拉x3y2',
          title='② 旋转90° × 非均匀拉伸')

# 情况3：均匀放大 × 旋转90° —— 可交换（你第6题错的那个）
draw_case(axes[1, 0],
          A=np.array([[2, 0], [0, 2]]),      # 均匀放大 2 倍
          B=np.array([[0, -1], [1, 0]]),     # 旋转 90°
          v=[1, 1], name_A='均匀放大', name_B='旋转90°',
          title='③ 均匀放大 × 旋转90°')

# 情况4：旋转180° × 旋转90° —— 可交换（角度相加）
draw_case(axes[1, 1],
          A=np.array([[0, -1], [1, 0]]),     # 旋转 90°
          B=np.array([[-1, 0], [0, -1]]),    # 旋转 180°
          v=[1, 1], name_A='旋转90°', name_B='旋转180°',
          title='④ 旋转180° × 旋转90°')

# 整图标题 + 图例（图例说明两条路各自是谁）
fig.suptitle('矩阵乘法可交换性：同一个 v 走两条路，看终点合不合', fontsize=13)
from matplotlib.lines import Line2D
legend_handles = [
    Line2D([0], [0], color='gray', linestyle='--', label='原始 v'),
    Line2D([0], [0], color=BLUE, label='先B后A  →  (A@B)@v'),
    Line2D([0], [0], color=RED, label='先A后B  →  (B@A)@v'),
]
fig.legend(handles=legend_handles, loc='lower center', ncol=3, fontsize=10)

fig.tight_layout(rect=[0, 0.04, 1, 0.95])
out = 'demo_commute_visual.png'
plt.savefig(out, dpi=110, bbox_inches='tight')
print('已保存', out)
