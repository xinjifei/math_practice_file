"""
Demo: 2D 向量可视化 + 长度计算
这是参考脚手架——展示 plt.quiver() 用法和向量长度公式，不替你做练习。
练习的三个向量 (3,2), (-1,4), (0,-3) 你要自己写代码画。
"""
import matplotlib.pyplot as plt
import numpy as np

# ===== 1. 画一个向量 =====

# plt.quiver() 参数逐行说明：
# quiver(x, y, dx, dy, angles='xy', scale_units='xy', scale=1, color='...')
#   x, y   — 箭头起点的坐标（向量从哪出发？这里是原点 0,0）
#   dx, dy — 箭头的 x 方向分量和 y 方向分量（向量 [dx, dy]）
#   angles='xy'   — 告诉 matplotlib："我的 dx,dy 就是数据坐标轴上的 x,y 变化量"
#                    不加这个参数的话，matplotlib 会对箭头做奇怪的缩放
#   scale_units='xy' — 配合 angles='xy'，确保箭头的长度单位 = 坐标轴单位一致
#   scale=1         — 不放缩箭头长度。不加的话箭头可能被自动缩放得不像数据坐标
#   color           — 箭头颜色（可选）

# 画向量 [3, 2]：从原点(0,0)出发，x方向走3，y方向走2
plt.quiver(0, 0, 3, 2, angles='xy', scale_units='xy', scale=1, color='blue')

# ===== 2. 设置坐标轴 =====
# xlim/ylim：设定 x 轴和 y 轴的显示范围，让箭头出现在画面中间
plt.xlim(-5, 5)
plt.ylim(-5, 5)

# axhline/axvline：画水平线和竖直线穿过原点，作为参考线
# y=0 → 水平 x 轴；x=0 → 竖直 y 轴
# color='gray', linestyle='--' → 灰色虚线，不抢眼
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
plt.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)

# grid(True)：显示网格线，方便读数
plt.grid(True, alpha=0.3)  # alpha=0.3 → 透明度，让网格不那么显眼

# ===== 3. 画多个向量 =====
# 你可以一次 quiver 画多支箭——把多个向量的起点、分量放到列表/数组里

# origins  = [[0,0], [0,0], [0,0]] — 三支箭都从原点出发
# dxs = [3, -1,  0] — 三支箭的 x 分量
# dys = [2,  4, -3] — 三支箭的 y 分量
#
# 注意：如果传列表给 quiver，它会自动拆包。x 参数取 origins 第一列，y 取第二列
# 更简单的写法是用 [0,0,0] 表示三个起点的 x 坐标都是 0

plt.figure()  # 新建一张图
plt.quiver([0, 0, 0], [0, 0, 0], [3, -1, 0], [2, 4, -3],
           angles='xy', scale_units='xy', scale=1,
           color=['red', 'green', 'purple'])  # 每支箭单独颜色

plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
plt.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)
plt.grid(True, alpha=0.3)

# ===== 4. 计算向量长度 =====
# 向量 [x, y] 的长度 = √(x² + y²) —— 勾股定理
# numpy 里：np.sqrt(x**2 + y**2)

def vector_length(x, y):
    """返回向量 [x, y] 的长度"""
    return np.sqrt(x**2 + y**2)

# 直接算：
# [3, 2]   → √(9 + 4)  = √13 ≈ 3.606
# [-1, 4]  → √(1 + 16) = √17 ≈ 4.123
# [0, -3]  → √(0 + 9)  = √9  = 3.0

vectors = [(3, 2), (-1, 4), (0, -3)]
for x, y in vectors:
    length = vector_length(x, y)
    print(f"向量 [{x:>2}, {y:>2}] 的长度 = √({x}² + {y}²) = {length:.3f}")

# 找最长的：
longest = max(vectors, key=lambda v: vector_length(v[0], v[1]))
print(f"\n最长的向量是 {longest}，长度 = {vector_length(*longest):.3f}")

# 显示所有图
plt.show()
