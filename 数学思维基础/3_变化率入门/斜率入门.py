import matplotlib.pyplot as plt
import matplotlib
import random

# 解决中文显示为方框的问题
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# Day 3：变化率入门——斜率的直觉
# ============================================================

print("=" * 50)
print("【任务1】手算10天价格变化的平均斜率")
print("=" * 50)

# 斜率公式：Δy / Δx = (y₂ - y₁) / (x₂ - x₁)
# 翻译成人话：x每走1步，y平均变化了多少

x1, y1 = 1, 10      # 第1天，价格10元
x2, y2 = 10, 12     # 第10天，价格12元

delta_x = x2 - x1           # x变了多少天
delta_y = y2 - y1           # y变了多少元
slope = delta_y / delta_x   # 平均每天涨多少元

print(f"  第{x1}天: {y1}元  →  第{x2}天: {y2}元")
print(f"  Δx = {x2} - {x1} = {delta_x} 天")
print(f"  Δy = {y2} - {y1} = {delta_y:+.0f} 元")
print(f"  斜率 = Δy / Δx = {delta_y} / {delta_x} ≈ {slope:.2f} 元/天")
print(f"  含义：平均每天涨 {slope:.2f} 元，10天总共涨了 {delta_y} 元")
print()

# ---------- 用代码验算 ----------
print("【验算】如果每天固定涨 0.22 元：")
for day in range(1, 11):
    price = 10 + slope * (day - 1)   # 起始10 + 每天涨0.22
    print(f"    第{day:>2}天: {price:.2f}元")
print()

# ============================================================
print("=" * 50)
print("【任务2】画图对比：陡峭上涨 vs 缓慢上涨")
print("=" * 50)

x = list(range(0, 11))  # 0到10

# 陡峭线：y = 2x + 1，斜率 = 2（每走1步涨2）
y_steep = [2 * i + 1 for i in x]

# 缓慢线：y = 0.3x + 3，斜率 = 0.3（每走1步涨0.3）
y_slow = [0.3 * i + 3 for i in x]

# ---- 画图 ----
plt.figure(figsize=(10, 5))

plt.plot(x, y_steep, marker='o', linewidth=2, label='陡峭：斜率=2（涨很快）')
plt.plot(x, y_slow,  marker='s', linewidth=2, label='缓慢：斜率=0.3（涨很慢）')

# ---- 在图上标出斜率的几何含义 ----
# 对陡峭线：x从1到3，Δx=2，Δy=4，斜率=2
plt.annotate('Δx=2\nΔy=4\n斜率=4/2=2',
             xy=(3, 7), xytext=(5, 5),
             arrowprops=dict(arrowstyle='->', color='blue'),
             fontsize=10, color='blue',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.5))

# 对缓慢线：x从0到10，Δx=10，Δy=3，斜率=0.3
plt.annotate('Δx=10\nΔy=3\n斜率=3/10=0.3',
             xy=(10, 6), xytext=(7, 8),
             arrowprops=dict(arrowstyle='->', color='green'),
             fontsize=10, color='green',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.5))

plt.title('斜率对比：陡峭 vs 缓慢', fontsize=14, fontweight='bold')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ============================================================
print("=" * 50)
print("【任务3】回头看Day2的30天股价图，估算前后15天的平均斜率")
print("=" * 50)

# 用同样的随机种子重现Day2的数据
random.seed(42)
days = list(range(1, 31))
price = 100
prices = []
for day in days:
    change = random.uniform(-4, 4)
    price = price + change
    prices.append(round(price, 2))

# 前15天：第1天 → 第15天
first_start_price = prices[0]    # 第1天
first_end_price = prices[14]     # 第15天
first_slope = (first_end_price - first_start_price) / (15 - 1)

# 后15天：第16天 → 第30天
second_start_price = prices[15]  # 第16天
second_end_price = prices[29]    # 第30天
second_slope = (second_end_price - second_start_price) / (30 - 16)

print(f"\n  前15天（第1→15天）:")
print(f"    价格: {first_start_price:.2f} → {first_end_price:.2f}")
print(f"    变化: {first_end_price - first_start_price:+.2f} 元")
print(f"    平均斜率: {first_slope:+.2f} 元/天")

print(f"\n  后15天（第16→30天）:")
print(f"    价格: {second_start_price:.2f} → {second_end_price:.2f}")
print(f"    变化: {second_end_price - second_start_price:+.2f} 元")
print(f"    平均斜率: {second_slope:+.2f} 元/天")

print(f"\n  结论:")
if first_slope > second_slope:
    print(f"    前15天涨得更快（{first_slope:.2f} > {second_slope:.2f}），后15天减速了")
elif first_slope < second_slope:
    print(f"    后15天涨得更快（{second_slope:.2f} > {first_slope:.2f}），在加速上涨")
else:
    print(f"    前后15天涨速差不多")

# ---- 画分段图 ----
plt.figure(figsize=(10, 5))

# 整个30天的折线
plt.plot(days, prices, marker='o', markersize=4, linewidth=2, label='30天股价')

# 前15天：用红色虚线连接首尾，表示平均趋势
plt.plot([1, 15], [first_start_price, first_end_price],
         'r--', linewidth=2, label=f'前15天平均趋势（斜率={first_slope:.2f}）')

# 后15天：用绿色虚线连接首尾
plt.plot([16, 30], [second_start_price, second_end_price],
         'g--', linewidth=2, label=f'后15天平均趋势（斜率={second_slope:.2f}）')

# 拐点分割线
plt.axvline(x=15.5, color='gray', linestyle=':', alpha=0.5)
plt.text(15.5, max(prices) + 1, '← 前15天 | 后15天 →', ha='center', fontsize=10, color='gray')

plt.title('Day2股价回顾：前15天 vs 后15天的平均斜率', fontsize=14, fontweight='bold')
plt.xlabel('天数')
plt.ylabel('股价（元）')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\n" + "=" * 50)
print("今日核心口诀：")
print("  斜率 = Δy / Δx = 每走一步x，y变化了多少")
print("  正斜率 = 涨，负斜率 = 跌")
print("  斜率大 = 变化猛，斜率小 = 变化缓")
print("=" * 50)
