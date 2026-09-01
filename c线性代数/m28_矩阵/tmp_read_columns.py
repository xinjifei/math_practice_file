# -*- coding: utf-8 -*-
"""
tmp_read_columns.py —— 完整演绎「看列读矩阵」：输出 = 列的线性组合

用一个具体例子走完四步：
  矩阵 M = [[2,1],[1,3]]，向量 v = [3,2]

  看列：列1=[2,1]=新 x 轴，列2=[1,3]=新 y 轴
  输出 w = 3·列1 + 2·列2 = [8,9]

图里约定：
  灰虚线 = 原坐标轴
  红      = 列1（新 x 轴）
  蓝      = 列2（新 y 轴）
  黑      = 输入 v
  绿      = 输出 w
"""

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

M = np.array([[2, 1], [1, 3]])
v = np.array([3, 2])
col1 = M[:, 0]   # [2,1]
col2 = M[:, 1]   # [1,3]
w = M @ v        # [8,9]

fig, axes = plt.subplots(1, 4, figsize=(21, 5.2))
LIM = (-1, 10)


def base(ax, title):
    ax.axhline(0, color="gray", linestyle="--", linewidth=1)
    ax.axvline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_aspect("equal")
    ax.set_xlim(*LIM)
    ax.set_ylim(*LIM)
    ax.grid(True, alpha=0.25)
    ax.set_title(title, fontsize=12)


# ── 第 1 步：旧坐标里，v 是几份 x 轴 + 几份 y 轴 ──
ax = axes[0]
base(ax, "第1步：旧坐标里，v = 3份x轴 + 2份y轴")
ax.quiver(0, 0, v[0], v[1], angles="xy", scale_units="xy", scale=1, color="black")
ax.plot([v[0], v[0]], [0, v[1]], "k:", linewidth=1)   # 竖直虚线分量
ax.plot([0, v[0]], [v[1], v[1]], "k:", linewidth=1)   # 水平虚线分量
ax.text(v[0], v[1], " v=[3,2]", fontsize=11)

# ── 第 2 步：矩阵把两根轴换成两列 ──
ax = axes[1]
base(ax, "第2步：矩阵把 x轴→列1、y轴→列2")
ax.quiver(0, 0, col1[0], col1[1], angles="xy", scale_units="xy", scale=1, color="tab:red")
ax.quiver(0, 0, col2[0], col2[1], angles="xy", scale_units="xy", scale=1, color="tab:blue")
ax.text(col1[0], col1[1], "列1=[2,1]", color="tab:red", fontsize=11)
ax.text(col2[0], col2[1], "列2=[1,3]", color="tab:blue", fontsize=11)

# ── 第 3 步：沿新轴走 v 的份数 ──
ax = axes[2]
base(ax, "第3步：沿新轴走 v 的份数")
ax.quiver(0, 0, col1[0], col1[1], angles="xy", scale_units="xy", scale=1,
          color="tab:red", alpha=0.35)   # 新轴（淡）
ax.quiver(0, 0, col2[0], col2[1], angles="xy", scale_units="xy", scale=1,
          color="tab:blue", alpha=0.35)
c1 = 3 * col1   # [6,3]
c2 = 2 * col2   # [2,6]
ax.quiver(0, 0, c1[0], c1[1], angles="xy", scale_units="xy", scale=1, color="tab:red")
ax.quiver(0, 0, c2[0], c2[1], angles="xy", scale_units="xy", scale=1, color="tab:blue")
ax.text(c1[0], c1[1], "3·列1=[6,3]", color="tab:red", fontsize=11)
ax.text(c2[0], c2[1], "2·列2=[2,6]", color="tab:blue", fontsize=11)

# ── 第 4 步：平行四边形合成 → 落点 w ──
ax = axes[3]
base(ax, "第4步：平行四边形合成 → 落点 w")
ax.quiver(0, 0, c1[0], c1[1], angles="xy", scale_units="xy", scale=1, color="tab:red")
ax.quiver(0, 0, c2[0], c2[1], angles="xy", scale_units="xy", scale=1, color="tab:blue")
ax.plot([c1[0], w[0]], [c1[1], w[1]], "tab:blue", linestyle=":", linewidth=1.5)  # 补边1
ax.plot([c2[0], w[0]], [c2[1], w[1]], "tab:red", linestyle=":", linewidth=1.5)   # 补边2
ax.quiver(0, 0, w[0], w[1], angles="xy", scale_units="xy", scale=1, color="tab:green")
ax.text(c1[0], c1[1], "3·列1", color="tab:red", fontsize=10)
ax.text(c2[0], c2[1], "2·列2", color="tab:blue", fontsize=10)
ax.text(w[0], w[1], " w=[8,9]", color="tab:green", fontsize=11)

fig.suptitle("看列的完整演绎：输出 w = v[0]·列1 + v[1]·列2（矩阵 [[2,1],[1,3]]，v=[3,2]）",
             fontsize=15)
fig.tight_layout(rect=[0, 0, 1, 0.94])

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_read_columns.png")
plt.savefig(out, dpi=110, bbox_inches="tight")
print("已保存:", out)
