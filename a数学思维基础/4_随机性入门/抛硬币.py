import matplotlib.pyplot as plt
import matplotlib
import random

# 解决中文显示为方框的问题
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# Day 4：什么是"随机"？——确定性 vs 随机性
# ============================================================

# ============================================================
print("=" * 50)
print("【任务1】模拟抛硬币：10次 vs 1000次")
print("=" * 50)


def flip_coin(times):
    """
    抛硬币 times 次，返回正面次数和正面比例
    用 random.choice(['正', '反']) 模拟每次的结果
    """
    heads = 0  # 正面计数
    for _ in range(times):
        result = random.choice(['正', '反'])  # 随机选一个，50%概率
        if result == '正':
            heads += 1
    return heads, heads / times


# 抛10次
heads_10, ratio_10 = flip_coin(10)
print(f"\n  抛 10 次:")
print(f"    正面: {heads_10} 次, 反面: {10 - heads_10} 次")
print(f"    正面比例: {ratio_10:.2f} ({heads_10}/10)")

# 抛1000次
heads_1000, ratio_1000 = flip_coin(1000)
print(f"\n  抛 1000 次:")
print(f"    正面: {heads_1000} 次, 反面: {1000 - heads_1000} 次")
print(f"    正面比例: {ratio_1000:.3f} ({heads_1000}/1000)")

# 抛10000次
heads_10000, ratio_10000 = flip_coin(10000)
print(f"\n  抛 10000 次:")
print(f"    正面: {heads_10000} 次, 反面: {10000 - heads_10000} 次")
print(f"    正面比例: {ratio_10000:.4f} ({heads_10000}/10000)")

print(f"\n  💡 规律：次数越多，正面比例越接近 0.5（50%）")

# ============================================================
print("\n" + "=" * 50)
print("【任务2】累计正面比例——观察它如何收敛到0.5")
print("=" * 50)

total_flips = 2000                         # 总共抛 2000 次
heads_count = 0                            # 当前正面累计数
cumulative_ratios = []                     # 存每次抛完后的正面比例

for i in range(1, total_flips + 1):        # i 从 1 到 2000
    result = random.choice(['正', '反'])
    if result == '正':
        heads_count += 1
    cumulative_ratios.append(heads_count / i)  # 第 i 次后的正面比例

# ---- 画图 ----
plt.figure(figsize=(12, 5))

# 子图1：累计比例变化
x = list(range(1, total_flips + 1))
plt.plot(x, cumulative_ratios, linewidth=0.5, color='blue', alpha=0.8)

# 画 0.5 的参考线
plt.axhline(y=0.5, color='red', linestyle='--', linewidth=2, label='理论值 0.5')

# 标注前期波动大
plt.annotate('前期波动很大\n10次时可能是0.3或0.7',
             xy=(10, cumulative_ratios[9]),
             xytext=(300, 0.75),
             arrowprops=dict(arrowstyle='->', color='gray'),
             fontsize=9, color='gray')

# 标注后期稳定
plt.annotate(f'2000次后≈{cumulative_ratios[-1]:.3f}\n已非常接近0.5',
             xy=(2000, cumulative_ratios[-1]),
             xytext=(1400, cumulative_ratios[-1] + 0.1),
             arrowprops=dict(arrowstyle='->', color='green'),
             fontsize=9, color='green')

plt.title('累计正面比例变化（共2000次）', fontsize=14, fontweight='bold')
plt.xlabel('抛硬币次数')
plt.ylabel('累计正面比例')
plt.ylim(0, 1)                     # 比例范围 0~1
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================================
print("\n" + "=" * 50)
print("【任务3】回答：为什么10次可能是3:7，10000次接近5:5？")
print("=" * 50)

print("""
  一句话：偶然 × 大数 → 偶然被淹没

  抛 10 次：
    - 每次结果对比例影响很大（一次就是 1/10 = 10%）
    - 运气稍微偏一点就 3:7 或 7:3
    - 所以"看起来"随机性很强

  抛 10000 次：
    - 每次结果对比例影响极小（一次只有 1/10000 = 0.01%）
    - 正反面概率各 50%，大量重复后，偶然的偏差互相抵消
    - 结果必然趋近 50% ≈ 50%

  这就是"大数定律"的直觉：
    单次 → 不可预测
    大量 → 规律浮现

  保险公司就靠这个赚钱：
    - 他们不知道"你"会不会今年生病
    - 但他们知道：100万个人里，大约有多少人今年会生病
    - 根据这个比例定价，总保费 > 总理赔，就稳赚
""")

print("=" * 50)
print("今日核心口诀：")
print("  确定性：同样输入 → 同样输出（f(x)=2x+1）")
print("  随机性：同样条件 → 结果可能不同（抛硬币）")
print("  随机 ≠ 没规律：量大之后，比例稳定 → 这就是概率")
print("=" * 50)
