"""
demo_vector_arithmetic.py — 向量加减法的语义运算演示
用 "apple - fruit + vegetable ≈ carrot" 演示和练习不同的语义类比。
练习里你的数据是 king/man/woman，这里的逻辑一模一样，换了一组向量而已。
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. 创建语义向量（2D，方便画图理解）
# ============================================================
# 每个词用一个 2D 坐标表示——这不是真实的 Embedding（真实的是几百维），
# 但向量加减的几何逻辑完全一样。

# apple: 第一维大 = "甜味"方向，第二维正 = "水果类"方向
apple = np.array([0.8, 0.4])

# fruit: 和 apple 接近，但第一维略小（水果这个概念本身不强调甜度）
fruit = np.array([0.6, 0.5])

# vegetable: 第二维为负——蔬菜在"水果类"的反方向
vegetable = np.array([0.3, -0.4])

# ============================================================
# 2. 语义运算：apple - fruit + vegetable
# ============================================================
# apple - fruit：去掉"水果类"成分，留下 apple 独有的"甜/脆"方向
# + vegetable：把这个"甜/脆"方向加到蔬菜上
# 结果 carrot_hat：应该在蔬菜区但有甜脆特征的位置 → 胡萝卜！

carrot_hat = apple - fruit + vegetable  # 逐元素加减：numpy 自动处理

print("apple             =", apple)
print("fruit             =", fruit)
print("vegetable         =", vegetable)
print("apple - fruit     =", apple - fruit, "  ← '甜脆'方向（去掉水果共性）")
print("carrot_hat        =", carrot_hat, "  ← 蔬菜 + 甜脆方向")

# ============================================================
# 3. 画图：四根箭头，看清加法的几何含义
# ============================================================
fig, ax = plt.subplots(figsize=(8, 8))
ax.axhline(y=0, color='gray', linewidth=0.5)  # x 轴参考线
ax.axvline(x=0, color='gray', linewidth=0.5)  # y 轴参考线

# --- 辅助函数：画一根箭头 ---
def draw_vector(vec, color, label, origin=(0, 0)):
    """
    参数说明：
    - vec: numpy 数组，[x, y]，箭头终点坐标（从 origin 出发）
    - color: 颜色名/代码，如 'blue', '#FF0000'
    - label: 图例标签
    - origin: 元组 (x0, y0)，箭头起点，默认原点 (0,0)
    """
    ax.quiver(
        origin[0], origin[1],   # 起点 x, y
        vec[0], vec[1],         # 方向分量 dx, dy
        angles='xy',            # 按数据坐标解释角度（不用屏幕坐标）
        scale_units='xy',       # 缩放单位 = 数据坐标
        scale=1,                # scale=1 → 不缩放，dx,dy 就是终点坐标
        color=color,
        label=label,
        width=0.008,            # 箭头线宽
    )

# 画四个向量
draw_vector(apple,     'red',    'apple')
draw_vector(fruit,     'orange', 'fruit')
draw_vector(vegetable, 'green',  'vegetable')
draw_vector(carrot_hat,'purple', 'carrot_hat (apple - fruit + vegetable)')

# --- 标注文字：在每个箭头终点写上名字 ---
# ax.text(x, y, 'text', ...) 在坐标 (x,y) 处放文字
for vec, name, offset in [
    (apple,      'apple',      (0.02, 0.02)),
    (fruit,      'fruit',      (0.02, 0.02)),
    (vegetable,  'vegetable',  (0.02, -0.08)),
    (carrot_hat, 'carrot_hat', (0.02, 0.02)),
]:
    ax.text(vec[0] + offset[0], vec[1] + offset[1], name, fontsize=10)

# 设置坐标轴
ax.set_xlim(-0.5, 1.5)
ax.set_ylim(-0.8, 1.0)
ax.set_xlabel('甜度方向 →')
ax.set_ylabel('水果类 ↑ / 蔬菜类 ↓')
ax.set_title('向量语义运算：apple - fruit + vegetable ≈ carrot')
ax.legend(loc='lower right')
ax.set_aspect('equal')  # x 和 y 轴比例相同，箭头不被拉伸
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================================
# 关键直觉（对着图看）：
# ============================================================
# - apple - fruit 是一根从 fruit 指向 apple 的箭头 → "甜脆差异"
# - 把这根箭头加到 vegetable 上 → 得到 carrot_hat
# - 向量加法 = 箭头首尾相接
# - 向量减法 = 差异/方向（从减数指向被减数）
#
# 你的练习：把上面的 apple/fruit/vegetable 换成 king/man/woman，
# 看看 carrot_hat 是不是会落在"女王"该在的位置。
