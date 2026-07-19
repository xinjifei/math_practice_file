import matplotlib.pyplot as plt
import matplotlib
import random

# 解决中文显示为方框的问题
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# Day 5：随机变量——把随机结果变成数字
# ============================================================

# ============================================================
print("=" * 50)
print("【核心概念】随机变量 = 把随机结果映射成数字")
print("=" * 50)
print("""
  抛硬币："正"→1  "反"→0        → 变成数字才能算"正面率"
  掷骰子：⚀→1  ⚁→2 ... ⚅→6     → 变成数字才能算"平均值"
  三枚硬币正面数：0, 1, 2, 3     → 变成数字才能算"概率分布"

  一句话：随机变量是"还没发生的数字"
  ——你知道可能取哪些值，也知道每个值的概率，但不知道本次具体是几
""")

# ============================================================
print("=" * 50)
print("【任务1】掷骰子1000次——画直方图")
print("=" * 50)

# 模拟掷骰子：random.randint(1, 6) 每次返回1~6之间的整数
rolls = [random.randint(1, 6) for _ in range(1000)]

# 统计每个面出现的次数
counts = [rolls.count(i) for i in range(1, 7)]

print("\n  掷骰子1000次结果：")
for face in range(1, 7):
    bar = '█' * (counts[face - 1] // 5)   # 每5次画一个方块，肉眼比较
    print(f"    面 {face}: {counts[face - 1]:>4} 次  {bar}")

print(f"\n  理论期望: 1000/6 ≈ {1000/6:.1f} 次/面")
print(f"  实际范围: {min(counts)} ~ {max(counts)} 次")
print(f"  💡 六个面出现次数大致相等，但不完全相等——这就是随机")

# ---- 画直方图 ----
plt.figure(figsize=(8, 5))

# hist()：自动分桶、自动统计
plt.hist(rolls, bins=range(1, 8), align='left', rwidth=0.8,
         color='steelblue', edgecolor='white')

# 画理论线
plt.axhline(y=1000 / 6, color='red', linestyle='--', linewidth=2,
            label=f'理论均匀线 ({1000/6:.0f}/面)')

plt.title('掷骰子1000次——直方图', fontsize=14, fontweight='bold')
plt.xlabel('骰子面')
plt.ylabel('出现次数')
plt.xticks([1, 2, 3, 4, 5, 6])    # x轴只标1到6
plt.legend()
plt.grid(True, alpha=0.3, axis='y')  # 只在y轴画网格
plt.tight_layout()
plt.show()

# ============================================================
print("\n" + "=" * 50)
print("【任务2】随机变量：抛三枚硬币，正面数 X = ?")
print("=" * 50)

print("""
  定义：X = 抛三枚硬币，正面的个数
  X 可能的值：0, 1, 2, 3

  概率怎么算？（正/反各50%）
    X=0  →  反反反  →  1/8 = 0.125
    X=1  →  正反反、反正反、反反正  →  3/8 = 0.375
    X=2  →  正正反、正反正、反正正  →  3/8 = 0.375
    X=3  →  正正正  →  1/8 = 0.125
""")


def three_coins_heads():
    """抛三枚硬币，返回正面个数（0~3）"""
    coins = [random.choice(['正', '反']) for _ in range(3)]
    return coins.count('正')  # 统计正面个数


# 模拟 10000 次
samples = [three_coins_heads() for _ in range(10000)]

print("  模拟10000次的结果 vs 理论概率：")
print(f"    {'X值':<8}{'模拟次数':<12}{'模拟频率':<12}{'理论概率':<12}")
print(f"    {'-'*40}")
for x in range(4):
    count = samples.count(x)
    sim_prob = count / 10000  # 模拟频率
    theo_prob = [1/8, 3/8, 3/8, 1/8][x]  # 理论概率
    bar = '█' * int(sim_prob * 80)
    print(f"    {x:<8}{count:<12}{sim_prob:<12.4f}{theo_prob:<12.4f}  {bar}")

print(f"\n  💡 模拟频率 ≈ 理论概率（大数定律再次生效！）")

# ---- 画概率分布图 ----
plt.figure(figsize=(8, 5))

x_values = [0, 1, 2, 3]
theory_prob = [1/8, 3/8, 3/8, 1/8]
sim_prob = [samples.count(x) / 10000 for x in x_values]

# 画柱状图：并排对比理论和模拟
bar_width = 0.35
plt.bar([v - bar_width/2 for v in x_values], theory_prob, bar_width,
        label='理论概率', color='steelblue', edgecolor='white')
plt.bar([v + bar_width/2 for v in x_values], sim_prob, bar_width,
        label='模拟频率（10000次）', color='orange', edgecolor='white')

plt.title('随机变量 X = 抛三枚硬币正面个数 的概率分布', fontsize=14, fontweight='bold')
plt.xlabel('X（正面个数）')
plt.ylabel('概率')
plt.xticks(x_values)
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# ============================================================
print("\n" + "=" * 50)
print("【任务3】思考：股票的#次日涨跌幅#是不是随机变量？")
print("=" * 50)

print("""
  是，次日涨跌幅就是一个随机变量。

  它可能取的值：理论上是 -100% 到 +∞
  但现实中：
    - A股有涨跌停板：-10% ~ +10%（普通股）
    - 美股没有涨跌停，但也极少超过 ±20%

  你无法提前知道明天的具体涨跌幅，但可以基于历史数据
  估计一个"概率分布"——这是后面要学的统计和机器学习的起点。

  类比：
    骰子 → 明天涨跌幅
    六面各1/6 → 小涨40%，小跌35%，大涨10%，大跌10%，横盘5% ...
    单次不确定 → 大量交易后，期望收益浮现
""")

print("=" * 50)
print("今日核心口诀：")
print("  随机变量 = 把不确定的结果，变成可以计算的数字")
print("  知道可能的取值，知道概率，但不知道这次是几")
print("  股票涨跌、骰子点数、硬币正面数 → 都是随机变量")
print("=" * 50)
