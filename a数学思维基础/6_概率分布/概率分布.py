import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 解决中文显示为方框的问题
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# Day 6：概率分布——一张图描述所有可能性
# ============================================================

print("=" * 50)
print("前置知识回顾")
print("=" * 50)
print("""
  Day 5 学的：随机变量 = 把随机结果映射成数字
  今天进一步：把所有"可能值 + 概率"打包画成一张图 → 概率分布图

  两种类型：
    离散分布 → 值之间"有缝"，用柱子画（bar）
    连续分布 → 值之间"无缝"，用曲线画（hist + curve）
""")

# ============================================================
print("=" * 50)
print("【任务1】离散概率分布：骰子的6根柱子")
print("=" * 50)

faces = [1, 2, 3, 4, 5, 6]
prob_each = 1 / 6  # 公平骰子，每面概率相等

print(f"\n  骰子有 6 个面，每面概率 = 1/6 ≈ {prob_each:.4f}")
print(f"  六个概率加起来 = {prob_each * 6:.0f}（必然事件）")
print(f"  这是离散分布：因为值只有 1,2,3,4,5,6，没有 2.3 或 4.7")

# ---- 画图 ----
fig, axes = plt.subplots(1, 3, figsize=(16, 5))  # 1行3列，三张图并排对比

# 左图：骰子——离散均匀分布
axes[0].bar(faces, [prob_each] * 6, color='steelblue', edgecolor='white', width=0.6)
axes[0].set_title('离散分布：骰子点数', fontsize=13, fontweight='bold')
axes[0].set_xlabel('点数')
axes[0].set_ylabel('概率')
axes[0].set_xticks(faces)
axes[0].set_ylim(0, 0.35)
axes[0].grid(True, alpha=0.3, axis='y')
# 标注：每个柱子上写概率
for f in faces:
    axes[0].text(f, prob_each + 0.005, f'{prob_each:.3f}', ha='center', fontsize=10)

# ============================================================
print("\n" + "=" * 50)
print("【任务2】连续概率分布：10000个模拟收益率")
print("=" * 50)

# np.random.normal(loc=均值, scale=标准差, size=数量)
# loc=0 → 以0为中心（涨跌各半）
# scale=2 → 波动幅度约±2%
returns = np.random.normal(loc=0, scale=2, size=10000)

print(f"\n  生成了 {len(returns)} 个模拟日收益率")
print(f"  均值(loc)=0% → 平均不涨不跌")
print(f"  标准差(scale)=2% → 大部分日子在 ±2% 之间")
print(f"  实际生成: 均值={returns.mean():.3f}%, 标准差={returns.std():.3f}%")
print(f"  最大值={returns.max():.2f}%, 最小值={returns.min():.2f}%")
print(f"  💡 这是连续分布：值可以是 -1.37%, 0.05%, 2.41%... 任意小数")

# ---- 中图：直方图（柱状） ----
counts, bins, patches = axes[1].hist(
    returns, bins=50,                # 分成50个桶
    density=True,                    # y轴显示概率密度（不是次数）
    color='steelblue', edgecolor='white', alpha=0.8
)
axes[1].set_title('连续分布：模拟日收益率\n（直方图，50个桶）', fontsize=13, fontweight='bold')
axes[1].set_xlabel('日收益率（%）')
axes[1].set_ylabel('概率密度')
axes[1].grid(True, alpha=0.3, axis='y')

# ---- 右图：拟合平滑曲线 ----
axes[2].hist(returns, bins=50, density=True,
             color='lightgray', edgecolor='white', alpha=0.5)

# 用正态分布公式手算一条平滑曲线叠上去
# 公式：f(x) = 1/(σ√2π) * e^(-(x-μ)²/(2σ²))

# 生成一条平滑的 x 轴
x_smooth = np.linspace(returns.min(), returns.max(), 200)
# 用正态分布的公式算对应的 y（概率密度）
mu, sigma = returns.mean(), returns.std()
y_smooth = (1 / (sigma * np.sqrt(2 * np.pi))) * \
           np.exp(-0.5 * ((x_smooth - mu) / sigma) ** 2)

axes[2].plot(x_smooth, y_smooth, 'r-', linewidth=2.5, label='拟合正态曲线')
axes[2].set_title('连续分布：模拟日收益率\n（曲线拟合）', fontsize=13, fontweight='bold')
axes[2].set_xlabel('日收益率（%）')
axes[2].set_ylabel('概率密度')
axes[2].legend()
axes[2].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# ============================================================
print("\n" + "=" * 50)
print('【任务3】对比：为什么一个"平"一个"鼓"？')
print("=" * 50)

print("""
  骰子（离散）—— 6根柱子一样高，所以"平"：
    原因：每面概率相等（均匀分布）
    每个值 1~6 的可能性完全相同
    柱子图最能表达：每个值一根柱子，高度 = 概率

  收益率（连续）—— 中间高两边低，"鼓"起来：
    原因：小涨小跌很常见，大涨大跌很罕见
    0% 附近的日子最多 → 中间隆起
    ±5% 的日子很少 → 两边塌下去
    曲线最能表达：值太密了，用柱子得画无限根，连成曲线才好看

  关键区别总结：
    ┌──────────┬──────────────┬──────────────┐
    │          │   离散分布    │   连续分布    │
    ├──────────┼──────────────┼──────────────┤
    │ 取值     │ 有限个，可数  │ 无限个，任意值│
    │ 例子     │ 骰子、硬币    │ 收益率、身高  │
    │ 画法     │ 柱子(bar)    │ 曲线(hist)   │
    │ 概率读法 │ 柱子高度     │ 曲线下面积    │
    │ 图形特点 │ 平的/阶梯状  │ 鼓的/山形    │
    └──────────┴──────────────┴──────────────┘
""")

# ---- 额外：正态分布说明 ----
print("=" * 50)
print("今日核心口诀：")
print("  概率分布 = 一张图，把随机变量所有可能性装进去")
print("  离散 → 柱子（值之间有缝，能数完）")
print("  连续 → 曲线（值之间无缝，数不完）")
print("  正态分布 = 中间鼓、两边塌的山 → 大多数自然现象都这样")
print("=" * 50)
