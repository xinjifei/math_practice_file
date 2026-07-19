import matplotlib.pyplot as plt
import matplotlib
import random

# 解决中文显示为方框的问题
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']  # 优先用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 防止负号也变成方框

# ============================================================
# Day 2：坐标与图形 —— 模拟30天股价走势
# ============================================================

# ---------- 1. 生成模拟数据 ----------

random.seed(42)                    # 固定随机种子，每次运行结果一样（方便调试）
days = list(range(1, 31))          # 第1天到第30天（x轴）

price = 100                        # 初始股价
prices = []                        # 存放每天的收盘价（y轴）
for day in days:
    change = random.uniform(-4, 4) # 每天随机波动 -4 到 +4 之间
    price = price + change         # 今天的价格 = 昨天的 + 随机波动
    prices.append(round(price, 2)) # 保留两位小数，存入列表

# 打印数据表，看一眼数字
print("=" * 40)
print(f"{'天数':<8}{'股价':<8}")
print("-" * 40)
for d, p in zip(days, prices):
    bar = "▲" if p >= 100 else "▽"  # 高于100用▲，低于100用▽
    print(f"第{d:<3}天  {p:<8.2f} {bar}")
print("=" * 40)
print(f"起始价: 100.00  →  最终价: {prices[-1]:.2f}")
print(f"30天涨跌幅: {prices[-1] - 100:+.2f}")

# ---------- 2. 画图 ----------

plt.figure(figsize=(10, 5))        # 画布大小：宽10英寸，高5英寸

# 画折线（x=天数，y=股价）
plt.plot(days, prices, marker='o', markersize=5, linewidth=2, color='#2c3e50')

# 画初始价格的参考线（虚线）
plt.axhline(y=100, color='red', linestyle='--', alpha=0.5, label='初始价 100')

# ---------- 3. 调成笛卡尔坐标系（十字轴） ----------

ax = plt.gca()                                    # 获取当前坐标轴对象
ax.spines['left'].set_position(('data', 0))       # 左边框移到 x=0（即最左边）
ax.spines['bottom'].set_position(('data', 95))    # 下边框移到 y=95（给图留空间）
ax.spines['right'].set_color('none')              # 隐藏右边框
ax.spines['top'].set_color('none')                # 隐藏上边框

# ---------- 4. 标注拐点 ----------
# 拐点：趋势明显转向的地方。这里用肉眼找几个关键点做示范。

# 第8天：局部低点（价格跌到一个坑）
ax.annotate('低点 ≈ 93',                    # 标注文字
            xy=(8, prices[7]),              # 箭头指向的点（第8天）
            xytext=(12, prices[7] - 8),     # 文字显示位置
            arrowprops=dict(arrowstyle='->', color='blue'),
            fontsize=9, color='blue')

# 第24天：局部高点（涨到一个小山峰）
ax.annotate('高点 ≈ 103',
            xy=(24, prices[23]),
            xytext=(18, prices[23] + 6),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=9, color='red')

# ---------- 5. 装饰 ----------

plt.title('模拟30天股价走势', fontsize=14, fontweight='bold')
plt.xlabel('天数')
plt.ylabel('股价（元）')
plt.legend()                                         # 显示图例（红线"初始价100"）
plt.grid(True, alpha=0.3)                            # 淡色网格
plt.tight_layout()                                   # 防止标签被切掉

# 标出每个点的数值（只标首尾和最高最低，避免太密）
extreme_days = [1, 8, 24, 30]                        # 第1、8、24、30天
for d in extreme_days:
    plt.text(d, prices[d-1] + 1.5, f'{prices[d-1]:.1f}',
             ha='center', fontsize=8, color='gray')

plt.show()
