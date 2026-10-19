# demo_annualize.py
# 演示：把"每天的小数"换算成"一年的大数"——年化收益率 和 年化波动率。
#
#   年化收益 ≈ μ_daily × 252        ← 因为收益率本身可以相加
#   年化波动 ≈ σ_daily × √252       ← 因为可加的是【方差】，标准差是方差开根号
#
# ⚠️ 演示参数：μ_daily = 0.0008、σ_daily = 0.010、3 个随机种子。
#    你练习要用的是 μ = 0.0005、σ = 0.015、5 个种子 —— 均值和波动都不同，
#    另外练习还要把 std 和 std×√252 这两个量级并排打出来。

import numpy as np
from function.plot import plot


# ---- 1. 一个乘 252、一个乘 √252：这两个系数是从哪来的 ----
TRADING_DAYS = 252          # 一年有多少个交易日（美股惯例 252；A 股约 242~244）
mu_daily = 0.0008           # 日收益率的均值：平均每天涨 0.08%
sigma_daily = 0.010         # 日收益率的标准差：每天的起伏大概 1%

# 收益率直接乘天数：一天平均涨 0.08%，一年（252 个交易日）就是 252 个 0.08% 加起来。
# 这一步成立，靠的是昨天学的那条——多期收益率可以直接相加。
annual_return = mu_daily * TRADING_DAYS

# 波动率不能这样乘。先把"能相加的东西"找出来：能相加的是【方差】，不是标准差。
#   ** 是 Python 的乘方：0.010 ** 2 = 0.0001
annual_var = sigma_daily ** 2 * TRADING_DAYS

# 标准差 = 方差的算术平方根。所以：
#   年化波动 = √(σ² × 252) = σ × √252
annual_vol = np.sqrt(annual_var)

print("【1】两个系数怎么来的")
print(f"  日收益均值 {mu_daily:.4f} × {TRADING_DAYS} = 年化收益 {annual_return:.4f}"
      f"（{annual_return:.2%}）")
print(f"  日波动 {sigma_daily:.4f} → 日方差 {sigma_daily ** 2:.6f}"
      f" × {TRADING_DAYS} = 年方差 {annual_var:.6f}")
print(f"    → 开根号 = 年化波动 {annual_vol:.4f}（{annual_vol:.2%}）")
print(f"  验算：σ × √252 = {sigma_daily * np.sqrt(TRADING_DAYS):.4f}　← 和上面一致")
# 记住这个差别：收益乘 252（约 252 倍），波动乘 15.87（√252）。同一个"一年"，
# 两个数被放大得完全不是一个量级。


# ---- 2. 模拟 3 条同参数路径：年化收益 vs 实际赚到 ----
# 模拟天数和上面的 TRADING_DAYS 一致 = 正好一年。
# 为什么必须一致：下面要比"年化外推"和"实际赚到"，两边得是同一段时间。
# 否则比出来的是"一年 vs 四个月"的差，不是"算术 vs 几何"的差。
n_days = TRADING_DAYS

# np.random.default_rng(seed)：造一个随机数发生器，相当于"随机数的水龙头"。
#   参数 seed 是随机种子 —— 同一个种子，每次跑出来的随机数序列完全一样。
#   换个种子 = 换一条"可能的未来"。不固定种子的话每次结果都不同，就没法对比。
#
# zip(列表A, 列表B)：把两个列表按位置配对，循环时一次同时拿到两样东西。
colors = ["tab:blue", "tab:orange", "tab:green"]

x = np.arange(1, n_days + 1)   # X 轴：第 1 天到最后一天
layers = []                    # 攒图层，最后一次性交给 plot()

for seed, color in zip([1, 2, 3], colors):
    rng = np.random.default_rng(seed)

    # rng.normal(loc=..., scale=..., size=...)：从正态分布里抽随机数。
    #   loc   = 均值（平均每天涨多少）
    #   scale = 标准差（每天起伏多大）
    #   size  = 抽多少个（= 多少天）
    returns = rng.normal(loc=mu_daily, scale=sigma_daily, size=n_days)

    # 年化收益：这一组的日速度 × 252，外推到一年
    annual_est = returns.mean() * TRADING_DAYS

    # 年化波动：用这一组数据自己估出来的日标准差 × √252
    #   std(ddof=1)：样本标准差，除以 (n-1) 而不是 n。
    #   ddof = "delta degrees of freedom"（自由度修正），金融数据通常取 1。
    vol_est = returns.std(ddof=1) * np.sqrt(TRADING_DAYS)

    # 实际这一年赚了多少：每天乘一次 (1 + r)，一路乘下去得到净值。
    #   np.cumprod 是累乘（cumulative product）：[1.1, 0.9] → [1.1, 0.99]
    # 注意这里没乘 252 —— 这是真金白银走完 120 天赚到的，不是外推出来的。
    wealth = np.cumprod(1 + returns)
    actual = wealth[-1] - 1

    # 假设每天都恰好赚到这一组的平均收益，一年下来是多少？
    #   ** 是乘方：(1 + μ) ** 252 = "把同一个倍率连乘 252 次"。
    # 实际路径有高有低，终值【一定不超过】这个数（Jensen 不等式）——
    # 差的这一块就是"波动拖累"，明天 Day 42 专门算它。
    smooth = (1 + returns.mean()) ** TRADING_DAYS - 1

    print(f"\n  种子 {seed}：年化收益 {annual_est:+.2%}　年化波动 {vol_est:.2%}"
          f"　实际这一年 {actual:+.2%}")
    print(f"           若每天恰好赚均值 {smooth:+.2%}"
          f"　实际 - 这个 = {actual - smooth:+.2%}　← 波动拖累")

    # 累计收益率（%）：(净值 - 1) × 100。
    #   乘 100 是为了躲开 plot() 的自动留白（上下各留 1）——不乘的话
    #   0.05 这个量级的曲线会被压成贴着 0 的一条直线。
    # np.column_stack：把两列一维数组拼成 (n, 2) 矩阵，plot() 的 point 层要这个形状。
    curve = np.column_stack([x, (wealth - 1) * 100])
    layers.append({"type": "point", "data": curve, "color": color, "s": 10})

plot(layers, title="三条累计收益率曲线（同参数、不同种子，%）：同样一年，终点差很多")

# 三组的 μ、σ 完全一样，但年化收益各不相同 —— 因为 μ_daily 是各自样本算出来的，
# 样本均值本身也是随机的。实际收益差得更狠：路径不同，复利的终点就不同。
