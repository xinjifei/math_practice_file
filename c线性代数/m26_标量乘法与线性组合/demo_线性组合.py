# -*- coding: utf-8 -*-
# demo_线性组合.py —— 参考脚手架
# 演示：标量乘法 + 线性组合 = 用向量"拼"出空间里能到达的位置
#
# ⚠️ 这里用的是【和你练习不同】的向量，只给你看思路。
#    你的练习是 [2,0]/[0,1]（不共线）和 [2,0]/[4,0]（共线）。
#    看完这个 demo，自己动手改数据做练习，别直接跑完当作业交。

import numpy as np              # 数组和数学运算
import matplotlib.pyplot as plt # 画图

# 让中文和负号能正常显示（m24 应该已经见过这两行）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def draw_span(v1, v2, title):
    """画一组向量 v1、v2 的线性组合能覆盖的范围。

    参数:
        v1, v2 : 两个 2D 向量（list 或 numpy 数组，形状 (2,)）
        title  : 图的标题（str）
    """
    v1 = np.array(v1)   # 转成 numpy 数组，后面才能做向量运算
    v2 = np.array(v2)

    n = 300                                    # 随机组合的次数（点多，范围看得清）
    c1 = np.random.uniform(-3, 3, n)           # n 个系数 c1，均匀取在 -3 到 3 之间
    c2 = np.random.uniform(-3, 3, n)           # n 个系数 c2
    #   np.random.uniform(low, high, size)：在 [low, high) 里随机取 size 个数

    # 关键一行：线性组合 = c1*v1 + c2*v2
    # c1 形状 (n,)，v1 形状 (2,) —— 用 c1[:, None] 把 (n,) 变成 (n,1)，
    # 这样才能和 (2,) 的 v1 逐元素相乘，得到 (n,2) 的点集
    points = c1[:, None] * v1 + c2[:, None] * v2

    plt.figure(figsize=(6, 6))
    plt.scatter(points[:, 0], points[:, 1], s=5, alpha=0.4, label='线性组合结果点')
    #   scatter(x, y, s=5, alpha=0.4, label=...)：画散点图
    #       x, y   点的横、纵坐标（这里是两列数组）
    #       s      点的大小
    #       alpha  透明度（0 全透明，1 不透明），重叠多时好看清密度
    #       label  图例里显示的名字

    # 把 v1、v2 本身画出来（从原点 (0,0) 出发，到向量终点）
    # 这里用 plot 画"线段 + 终点红点"，不用 quiver——
    # quiver 的箭头三角头渲染出来像块难辨认的红色形状，反而干扰理解
    for vec, name in [(v1, 'v1'), (v2, 'v2')]:
        plt.plot([0, vec[0]], [0, vec[1]], 'r-', linewidth=2, label=name)
        #   plot(x列表, y列表, 'r-', linewidth=2)：画一条红色实线
        #       [0, vec[0]] = x 的两个端点（原点 0 和 vec 的 x 分量）
        #       [0, vec[1]] = y 的两个端点（原点 0 和 vec 的 y 分量）
        #       'r-' = 红色实线；linewidth=2 = 线宽
        plt.plot(vec[0], vec[1], 'ro', markersize=6)
        #   plot(x, y, 'ro', markersize=6)：在 (vec[0], vec[1]) 画一个红色圆点
        #       'ro' = 红色圆点；markersize=6 = 点的大小

    plt.axhline(0, color='gray', linewidth=0.5)  # 画一条水平的 x 轴参考线
    plt.axvline(0, color='gray', linewidth=0.5)  # 画一条竖直的 y 轴参考线
    plt.axis('equal')       # x/y 轴比例一致，向量的角度才不失真
    plt.legend()            # 显示图例（就是 scatter 里 label 那个名字）
    plt.title(title)        # 图的标题
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


# ============ 实验一：不共线 ============
# v1=[1,2] 指向右上方，v2=[3,1] 指向右下方，两者不共线
# → 它们的线性组合能覆盖整个平面（点散成一片）
draw_span([1, 2], [3, 1], '不共线：线性组合覆盖整个平面')


# ============ 实验二：共线 ============
# v2 = 2*v1，两个向量落在同一条直线上
# → 线性组合只能覆盖这条线（所有点挤在一条斜线上）
draw_span([1, 2], [2, 4], '共线：线性组合只能覆盖一条线')
