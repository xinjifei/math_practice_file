# -*- coding: utf-8 -*-
# plot_vectors.py —— 画一组带名字的向量
#
# 输入：字典组成的列表，每个字典 = {向量名: 坐标列表}
#   例：[{"v1": [2, 0]}, {"v2": [0, 0, 4, 0]}]
#   - 2 个数 [x, y]            ：终点，默认起点 (0,0)
#   - 4 个数 [x1, y1, x2, y2]  ：起点 (x1,y1)、终点 (x2,y2)  ← 后两个是终点，不是差值

import numpy as np
import matplotlib.pyplot as plt

# 让中文标题能正常显示（不设的话中文会变方块）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def plot_vectors(vectors, title="向量图"):
    """画一组带名字的向量，名字标在向量末端。

    参数:
        vectors : list[dict]
            每个元素是 {向量名: 坐标列表}。坐标列表两种形式：
              [x, y]             终点，默认起点 (0,0)
              [x1, y1, x2, y2]   起点 (x1,y1)、终点 (x2,y2)
        title   : str
            图顶部的标题

    例子:
        plot_vectors([{"v1": [2, 0]}, {"v2": [0, 0, 4, 0]}], title="测试")
    """
    if not vectors:
        raise ValueError("vectors 不能为空，至少给一个向量")

    names = []      # 存向量名
    coords = []     # 统一存成 [x1, y1, x2, y2]，方便后面取
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
    # n 小 → 相邻颜色隔得远（色差大）；n 大 → 隔得近（色差小）
    # endpoint=False 保证 n 个颜色首尾不重复（否则第 1 个和第 n 个会都是红色）
    colors = plt.cm.hsv(np.linspace(0, 1, n, endpoint=False))

    for i in range(n):
        x1, y1, x2, y2 = coords[i]
        # quiver 的第 3、4 个参数是"位移"（终点 − 起点），所以要自己算差值
        plt.quiver(x1, y1, x2 - x1, y2 - y1,
                   angles="xy", scale_units="xy", scale=1,
                   color=colors[i])
        # 名字标在向量末端（终点）
        plt.text(x2, y2, names[i])

    # 参考轴 + 网格（跟你之前的画法一致）
    plt.axhline(0, color="gray", linestyle="--")
    plt.axvline(0, color="gray", linestyle="--")
    plt.grid(True)

    # 根据所有向量的起点终点，自动定坐标范围，四周留 1 的边
    xs = [c[0] for c in coords] + [c[2] for c in coords]
    ys = [c[1] for c in coords] + [c[3] for c in coords]
    pad = 1
    plt.xlim(min(xs) - pad, max(xs) + pad)
    plt.ylim(min(ys) - pad, max(ys) + pad)

    plt.title(title)
    plt.show()


if __name__ == "__main__":
    # 直接运行本文件时的自测：验证两种输入形式都能画、不报错
    plot_vectors(
        [
            {"v1": [2, 0]},        # 2 个数：默认起点 (0,0)，到 (2,0)
            {"v2": [0, 0, 0, 1]},  # 4 个数：从 (0,0) 到 (0,1)
            {"v3": [1, 1, 3, 100]},  # 4 个数：从 (1,1) 到 (3,1)，起点不在原点
        ],
        title="自测：三种输入",
    )
