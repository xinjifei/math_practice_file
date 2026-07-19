"""
Day 9：期望值 —— "长期平均值"的数学表述

核心概念：
- 期望值 E[X] = Σ(x × P(x))：每个值 × 它的概率，全加起来
- 骰子期望 = 3.5（不是具体结果，是"长期平均"）
- 策略期望收益 > 0 = 长期平均赚钱 ≠ 明天一定赚钱
"""

import random
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 任务 1：模拟骰子 1000 次，验证样本均值 ≈ 3.5
# ============================================================
print("=" * 60)
print("任务 1：模拟骰子 1000 次，验证样本均值 ≈ 3.5")
print("=" * 60)

n = 1000
random.seed(42)  # 固定种子，结果可复现

# 掷 n 次骰子
rolls = [random.randint(1, 6) for _ in range(n)]  # randint(1,6) 含 1 和 6

# 计算累计均值：前 i 次的结果平均值，看它怎么逼近 3.5
cumulative_avg = []
running_sum = 0
for i, r in enumerate(rolls, start=1):
    running_sum += r
    cumulative_avg.append(running_sum / i)

# 最终均值
final_avg = sum(rolls) / n
print(f"掷骰子 {n} 次的样本均值: {final_avg:.3f}")
print(f"与理论期望值 3.5 的差距: {abs(final_avg - 3.5):.3f}")

# 画图：累计均值随次数收敛到 3.5
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(1, n + 1), cumulative_avg, linewidth=1, color='steelblue')
ax.axhline(3.5, color='red', linestyle='--', linewidth=1.5, label='理论期望值 3.5')
ax.set_title(f'骰子模拟：累计均值随次数的变化\n(最终均值 = {final_avg:.3f})', fontsize=13)
ax.set_xlabel('投掷次数')
ax.set_ylabel('累计均值')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# ============================================================
# 任务 2：模拟"胜率 60%、赚 1 赔 1"策略 1000 次，画累计收益曲线
# ============================================================
print("\n" + "=" * 60)
print("任务 2：「胜率 60%、赚 1 赔 1」策略模拟")
print("=" * 60)

# 先手算期望值：
#   E = 0.6 × (+1) + 0.4 × (-1) = 0.6 - 0.4 = 0.2
#   期望值 = +0.2，长期平均每局赚 0.2 元
print("理论期望值 E = 0.6 × (+1) + 0.4 × (-1) = 0.2")

win_rate = 0.6    # 胜率 60%
win_amount = 1    # 赢了赚 1
lose_amount = 1   # 输了赔 1
n_bets = 1000

random.seed(123)
capital = 0  # 初始资金
capital_history = [capital]  # 记录每局后的资金

for _ in range(n_bets):
    if random.random() < win_rate:
        capital += win_amount   # 赢：+1
    else:
        capital -= lose_amount  # 输：-1
    capital_history.append(capital)

print(f"最终资金: {capital}")
print(f"平均每局收益: {capital / n_bets:.3f}")
print(f"注：你可能会看到虽然期望值 > 0，但中途资金曾经严重下跌——")
print(f"    这就是'期望 > 0 ≠ 明天一定赚钱'的含义")

# 画图
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(range(n_bets + 1), capital_history, linewidth=1, color='darkgreen')
ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
# 理论上每局赚 0.2，n 局后期望资金 = 0.2 × n
expected_line = [0.2 * i for i in range(n_bets + 1)]
ax.plot(range(n_bets + 1), expected_line, 'r--', linewidth=1.5,
        label=f'理论期望线 (E=0.2/局)')
ax.set_title(f'「胜率 {win_rate*100:.0f}%、赚 1 赔 1」模拟 {n_bets} 次\n'
             f'期望值 = +0.2/局，最终资金 = {capital}', fontsize=13)
ax.set_xlabel('下注次数')
ax.set_ylabel('累计资金')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("核心结论：")
print("1. 骰子期望值 3.5 = 长期平均，任何单次都掷不出 3.5")
print("2. 期望 > 0 并不等于每次都赚钱——")
print("   胜率 60% 策略照样会连续亏，但长期曲线围绕期望线上下波动")
print("3. 赌场就是靠这个赚钱：每个游戏期望值略 < 0，短期客人可能赢，")
print("   长期赌场稳赚")
print("=" * 60)
