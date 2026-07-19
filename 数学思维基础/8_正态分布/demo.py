"""
Day 8：正态分布 —— 为什么"钟形曲线"无处不在

核心概念：
- 正态分布 = 中间高、两边低、左右对称的钟形
- μ = 均值（中心在哪），σ = 标准差（钟的胖瘦）
- μ ± 1σ ≈ 68%，μ ± 2σ ≈ 95%

练习任务：
1. 用 np.random.normal(0, 1, 10000) 生成标准正态数据，画直方图
2. 验证：数据落在 [-1, 1] ≈ 68%？落在 [-2, 2] ≈ 95%？
3. 改 μ=0.01, σ=0.03（模拟 A 股日均收益约 0.01%，波动约 3%），画分布图
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy.stats import norm

# 设置中文字体（Windows 上用 Microsoft YaHei）
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# ============================================================
# 任务 1：标准正态分布（μ=0, σ=1）—— 画直方图 + 叠加钟形曲线
# ============================================================
print("=" * 60)
print("任务 1 & 2：标准正态分布 & 68%/95% 规则验证")
print("=" * 60)

# 参数
mu = 0       # 均值
sigma = 3    # 标准差
n = 10000    # 样本量

# 生成数据
np.random.seed(42)  # 固定随机种子，保证结果可复现
data = np.random.normal(mu, sigma, n)

# 画直方图
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ---- 左图：直方图 + 钟形曲线 ----
ax = axes[0]
counts, bins, patches = ax.hist(data, bins=50, density=True, alpha=0.6, color='steelblue', edgecolor='white')
# 叠加理论正态曲线
x = np.linspace(mu - 4*sigma, mu + 4*sigma, 500)
pdf = norm.pdf(x, mu, sigma)
ax.plot(x, pdf, 'r-', linewidth=2, label='理论正态曲线 N(0, 1)')

# 标注 ±1σ 和 ±2σ 区域
for k, color, alpha, label in [
    (1, 'orange', 0.25, '±1σ (约 68%)'),
    (2, 'green', 0.15, '±2σ (约 95%)'),
]:
    x_fill = np.linspace(mu - k*sigma, mu + k*sigma, 200)
    ax.fill_between(x_fill, norm.pdf(x_fill, mu, sigma),
                    alpha=alpha, color=color, label=label)
ax.set_title('标准正态分布 N(0, 1)\n直方图 + 钟形曲线', fontsize=13)
ax.set_xlabel('值')
ax.set_ylabel('概率密度')
ax.legend(fontsize=8)
ax.axvline(mu, color='gray', linestyle='--', linewidth=1, label=f'μ={mu}')

# ---- 右图：68% 和 95% 规则验证 ----
ax = axes[1]

# 计算实际比例
within_1sigma = np.mean((data >= mu - 1*sigma) & (data <= mu + 1*sigma)) * 100
within_2sigma = np.mean((data >= mu - 2*sigma) & (data <= mu + 2*sigma)) * 100
within_3sigma = np.mean((data >= mu - 3*sigma) & (data <= mu + 3*sigma)) * 100

# 理论值
theory_1 = 68.27
theory_2 = 95.45
theory_3 = 99.73

# 柱状图对比
categories = ['±1σ', '±2σ', '±3σ']
actual = [within_1sigma, within_2sigma, within_3sigma]
expected = [theory_1, theory_2, theory_3]

x_pos = np.arange(len(categories))
width = 0.35

bars1 = ax.bar(x_pos - width/2, actual, width, label='实际值 (n=10000)',
               color='steelblue', edgecolor='white')
bars2 = ax.bar(x_pos + width/2, expected, width, label='理论值',
               color='lightcoral', edgecolor='white')

# 在柱子上标注数值
for bar, val in zip(bars1, actual):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
for bar, val in zip(bars2, expected):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_title('正态分布经验规则验证\n实际 vs 理论', fontsize=13)
ax.set_ylabel('数据占比 (%)')
ax.set_xticks(x_pos)
ax.set_xticklabels(categories)
ax.legend(fontsize=9)
ax.set_ylim(0, 110)

plt.tight_layout()
plt.show()
print(f"\n验证结果：")
print(f"  数据在 ±1σ 内: {within_1sigma:.2f}%（理论 {theory_1:.2f}%）")
print(f"  数据在 ±2σ 内: {within_2sigma:.2f}%（理论 {theory_2:.2f}%）")
print(f"  数据在 ±3σ 内: {within_3sigma:.2f}%（理论 {theory_3:.2f}%）")


# ============================================================
# 任务 3：模拟 A 股日均收益分布（μ=0.01%, σ=3%）
# ============================================================
print("\n" + "=" * 60)
print("任务 3：模拟 A 股日均收益分布")
print("=" * 60)

mu_stock = 0.01     # 日均收益约 0.01%
sigma_stock = 3.0   # 日波动约 3%

# 生成数据
stock_returns = np.random.normal(mu_stock, sigma_stock, n)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ---- 左图：收益分布直方图 + 钟形曲线 ----
ax = axes[0]
ax.hist(stock_returns, bins=60, density=True, alpha=0.6, color='darkgreen', edgecolor='white')
x_stock = np.linspace(mu_stock - 4*sigma_stock, mu_stock + 4*sigma_stock, 500)
pdf_stock = norm.pdf(x_stock, mu_stock, sigma_stock)
ax.plot(x_stock, pdf_stock, 'r-', linewidth=2, label=f'正态曲线 N({mu_stock}, {sigma_stock}²)')

# 标注重要区间
for k, color, alpha, label in [
    (1, 'orange', 0.25, f'±1σ [{mu_stock-sigma_stock:.1f}%, {mu_stock+sigma_stock:.1f}%]'),
    (2, 'green', 0.15, f'±2σ [{mu_stock-2*sigma_stock:.1f}%, {mu_stock+2*sigma_stock:.1f}%]'),
]:
    x_f = np.linspace(mu_stock - k*sigma_stock, mu_stock + k*sigma_stock, 200)
    ax.fill_between(x_f, norm.pdf(x_f, mu_stock, sigma_stock),
                    alpha=alpha, color=color, label=label)

ax.axvline(0, color='black', linestyle='--', linewidth=1, label='收益=0（不赚不亏）')
ax.set_title(f'A 股日均收益模拟\nμ={mu_stock}%, σ={sigma_stock}%（约合日均收益分布）', fontsize=13)
ax.set_xlabel('日收益率 (%)')
ax.set_ylabel('概率密度')
ax.legend(fontsize=7.5)

# ---- 右图：累计收益视角 — 252 个交易日模拟 ----
ax = axes[1]
np.random.seed(123)
trading_days = 252  # 一年约 252 个交易日
daily_returns = np.random.normal(mu_stock/100, sigma_stock/100, trading_days)  # 转为小数
cumulative = (1 + daily_returns).cumprod() * 100  # 从 100 开始

ax.plot(range(1, trading_days + 1), cumulative, color='darkgreen', linewidth=1.5)
ax.axhline(100, color='gray', linestyle='--', linewidth=1, label='初始值 100')
ax.set_title('模拟一年（252 个交易日）累计收益\n假设每日收益 ~ N(0.01%, 3%²)', fontsize=13)
ax.set_xlabel('交易日')
ax.set_ylabel('资产价值（初始=100）')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 统计
neg_days = np.mean(stock_returns < 0) * 100
extreme_up = np.mean(stock_returns > mu_stock + 2*sigma_stock) * 100
extreme_down = np.mean(stock_returns < mu_stock - 2*sigma_stock) * 100

print(f"\nA股收益模拟统计：")
print(f"  日均收益均值: {np.mean(stock_returns):.2f}%")
print(f"  日收益标准差: {np.std(stock_returns):.2f}%")
print(f"  下跌交易日占比: {neg_days:.1f}%")
print(f"  大涨（>μ+2σ={mu_stock+2*sigma_stock:.1f}%）概率: {extreme_up:.1f}%")
print(f"  大跌（<μ-2σ={mu_stock-2*sigma_stock:.1f}%）概率: {extreme_down:.1f}%")

print("\n" + "=" * 60)
print("核心结论：")
print("1. 标准正态分布：μ ± 1σ ≈ 68%，μ ± 2σ ≈ 95%")
print("2. 正态分布由两个参数完全决定：μ（中心位置）和 σ（离散程度）")
print("3. 金融收益率常用正态假设——大量微小因素叠加 → 趋向正态（中心极限定理）")
print("=" * 60)
