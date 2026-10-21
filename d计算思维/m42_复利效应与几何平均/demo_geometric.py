# demo_geometric.py
# 演示：同一组年收益，用两种"平均"算出来，结果能差出一大截。
#
#   算术平均 = (r1 + r2 + ... + rn) / n                    ← 脑子里那个"平均"
#   几何平均 = [(1+r1)(1+r2)...(1+rn)] ** (1/n) - 1        ← 账户里每年实际赚的
#
# ⚠️ 演示参数：期望年收益 8%、σ = 30%、6 年、种子 18。
#    练习要做的是期望 10%、σ = 20%、10 年，另有一组换 σ 的对比 ——
#    参数不同，别把 demo 的数字当成练习的答案。

import numpy as np
from function.plot import plot

# ---- 参数（全集中在开头，改一处，下面全跟着变） ----
YEARS = 6           # 模拟几年
mu = 0.08           # 年收益率的期望：平均每年 8%
sigma = 0.30        # 年收益率的标准差：年与年之间起伏 30%
seed = 18           # 随机种子：固定它就固定这一条"可能的未来"

# np.random.default_rng(seed)：造一个随机数发生器（"随机数的水龙头"）。
#   参数 seed 是种子——同一个种子每次跑出来的数完全一样；
#   换一个种子 = 换一条可能的未来。
rng = np.random.default_rng(seed)

# rng.normal(loc=..., scale=..., size=...)：从正态分布里抽随机数。
#   loc   = 均值（平均每年涨多少）
#   scale = 标准差（年与年之间起伏多大）
#   size  = 抽几个（= 几年）
returns = rng.normal(loc=mu, scale=sigma, size=YEARS)

print("【1】这 6 年的年收益率")
# f"{r:+.2%}"：格式化成百分比、保留两位小数、正数前面带 + 号
# "  ".join(...)：把每个字符串用两个空格连起来，一行打完
print("  " + "  ".join(f"{r:+.2%}" for r in returns))


# ---- 2. 两种平均 ----

# 算术平均：加起来除以个数。就是你平时说的"平均"。
arith = returns.mean()

# 几何平均，拆成三步看：
#   1 + returns            → 每年的"倍率"：[1.5, 0.6] 这种
#   np.prod(1 + returns)   → 全部乘起来 = 期末净值（倍率）
#                             np.prod 是累乘（product），[1.5, 0.6] → 0.9
#   ** (1 / YEARS)         → 开 n 次方：哪个固定倍率连乘 6 次正好等于它
#   - 1                    → 扣掉本金，变回收益率
geo = np.prod(1 + returns) ** (1 / YEARS) - 1

# 期末总收益：净值减 1
total = np.prod(1 + returns) - 1

print("\n【2】两种平均")
print(f"  算术平均  {arith:+.2%}")
print(f"  几何平均  {geo:+.2%}")
print(f"  差额      {arith - geo:.2%}   ← 波动吃掉的那一块")
print(f"  6 年总收益 {total:+.2%}")

# 假想路径：假设每年都恰好赚到"算术平均"这么多。
#   这是算术平均对应的世界，**现实里不存在**
#   —— 每年收益都被硬拉成同一个数，路径一点也不波动。
smooth_total = (1 + arith) ** YEARS - 1
print(f"  若每年都恰好赚算术平均，6 年：{smooth_total:+.2%}"
      f"　　（真实是 {total:+.2%}，差 {total - smooth_total:+.2%}）")

# 差距的近似量级：σ² / 2。
# 别记推导，记结论 —— 波动翻倍，侵蚀变四倍（因为是平方）。
print(f"  参考：σ²/2 = {sigma ** 2 / 2:.2%}"
      f"　← 和上面的差额 {arith - geo:.2%} 同一量级")


# ---- 3. 回本不对称：跌下去的坑，填起来要更多 ----
# 亏 40% 后账户剩 0.6。要回到 1，需要涨 (1 / 0.6) - 1。
loss = 0.40
need = 1 / (1 - loss) - 1
print("\n【3】回本要涨多少")
print(f"  亏 {loss:.0%} → 剩 {(1 - loss):.2f} → 要涨 {need:.2%} 才回本")
# 同理：+50%/−40% 两年，算术平均 5%，期末却是 0.9 —— 亏了 10%


# ---- 4. 画出来：真实路径 vs 平滑路径 ----
# 净值从"第 0 年 = 1.0"开始。
# np.concatenate([起点数组, 逐年数组])：把两段拼成一个数组。
#   [[1.0]] 是一行一列的二维数组，和 np.cumprod 的输出形状能拼上
#   —— 为什么套一层 []：np.concatenate 只认"数组列表"
# np.cumprod(1 + returns)：累乘，[1.5, 0.6] → [1.5, 0.9]
wealth = np.concatenate([[1.0], np.cumprod(1 + returns)])

# 平滑路径：每年都乘 (1 + 算术平均)，第 t 年是 (1+arith) 的 t 次方。
# np.arange(0, YEARS + 1)：0,1,2,...,6（含终点，所以 +1）
smooth = (1 + arith) ** np.arange(0, YEARS + 1)

# X 轴：第 0 年到第 6 年
x = np.arange(0, YEARS + 1)

# 净值是 1 左右的数，乘 100 换成百分比。
#   plot() 会自动给上下各留 1 的边距；不放大到百分数，
#   几条贴着 1.0 的曲线会被压成一条直线，看不出差。
# np.column_stack([列A, 列B])：把两列一维数组并成 (n, 2) 矩阵，
#   line 层的 data 要的就是这个形状（每行一个顶点，按行顺序连成折线）。
#
# line 层的参数：
#   data       (n, 2) 矩阵，至少 2 个点，否则连不成线
#   color      线色；不传会自动从色相环取下一个颜色
#   linestyle  线型；不传默认 "--"（虚线），想要实线就写 "-"
#   linewidth  线宽；不传默认 2
real_layer = {
    "type": "line",
    "data": np.column_stack([x, (wealth - 1) * 100]),
    "color": "tab:blue",
    "linestyle": "-",     # 实际路径画实线，和"假想"的虚线分开
}
smooth_layer = {
    "type": "line",
    "data": np.column_stack([x, (smooth - 1) * 100]),
    "color": "tab:orange",
    "linestyle": "--",
}

# 把两条线的终点单独做成一层，用 labels 标上名字。
#   point 层的 labels 是"每个点一个字符串"，点的数量要和标签数量一致。
#   np.array([[x, y]]) 是一个 1 行 2 列的矩阵 —— 一个点。
end_real = {
    "type": "point",
    "data": np.array([[YEARS, (wealth[-1] - 1) * 100]]),
    "labels": [f"实际 {(wealth[-1] - 1):+.1%}"],
    "color": "tab:blue",
    "s": 60,
}
end_smooth = {
    "type": "point",
    "data": np.array([[YEARS, (smooth[-1] - 1) * 100]]),
    "labels": [f"平滑 {(smooth[-1] - 1):+.1%}"],
    "color": "tab:orange",
    "s": 60,
}

plot(
    [real_layer, smooth_layer, end_real, end_smooth],
    title="实际路径 vs 每年都赚算术平均的平滑路径（累计收益 %）",
)

# 看图上两条线的终点：算术平均画出来的那条平滑线永远在上面
# （算术平均 ≥ 几何平均）。差的那一截，就是波动从你口袋里拿走的东西。
