# -*- coding: utf-8 -*-
# demo_sharpe.py
# 演示：Sharpe Ratio = (年化收益 − 无风险利率) / 年化波动
#                      └── 超额收益 ──┘   └── 风险 ──┘
#
# 一句话：每承担 1 单位风险，赚到了多少「超过无风险利率」的钱。
#
# ⚠️ 演示参数：策略 X（年化 20%、σ=30%）、策略 Y（年化 8%、σ=8%），rf = 3%。
#    练习要的是 A（年化 30%、σ=25%）、B（年化 18%、σ=10%），rf = 2% ——
#    数字完全不同，别把 demo 的输出当成练习的答案。

import sys
from pathlib import Path

# 让 import function.plot 能找到仓库根目录下的 function/ 包。
#   __file__            : 当前脚本的路径
#   .resolve()          : 转成绝对路径
#   .parents[2]         : 往上两层 = d计算思维 的上一层 = 仓库根目录
#   sys.path.insert(0, …): 把这个目录插到模块搜索路径的最前面
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
from function.plot import plot


# ---- 参数（全部集中在开头，方便一次改） ----
RF = 0.03              # 无风险利率，年化 3%（国债这类"躺着也能拿"的收益）
N_DAYS = 252           # 一年的交易日数，年化换算的分母
X_RET, X_VOL = 0.20, 0.30    # 策略 X：年化收益 20%，年波动 30%
Y_RET, Y_VOL = 0.08, 0.08    # 策略 Y：年化收益 8%，年波动 8%


def simulate_daily_returns(annual_ret, annual_vol, n_days=N_DAYS, seed=0):
    """按给定的年化参数，模拟一条日收益序列。

    参数:
        annual_ret : 期望的年化收益（小数，0.2 = 20%）
        annual_vol : 年化波动（小数，0.3 = 30%）
        n_days     : 模拟多少天
        seed       : 随机种子。固定它 → 每次运行结果一样，方便对照
    返回:
        numpy 一维数组，长度 n_days，每个元素是当天的收益率
    """
    # np.random.default_rng(seed)：新建一个随机数生成器（新写法，比旧 np.random.seed 好）。
    #   同一个 seed → 产生同一串随机数 → 结果可复现。
    rng = np.random.default_rng(seed)

    # 年化 → 日：均值直接除以 252（一天赚年化收益的 1/252）
    mu_d = annual_ret / N_DAYS
    # 波动年化 → 日化，要除以 √252，不是 252。
    #   记住这条路：日波动 × √252 = 年波动（拍，因为波动的方差随天数是线性叠加的）
    sig_d = annual_vol / np.sqrt(N_DAYS)

    # rng.normal(均值, 标准差, 个数)：从正态分布里抽 n_days 个数。
    #   这里把每天收益当成独立正态 —— 是个简化假设，真实市场有肥尾和聚集，今天先不管。
    return rng.normal(mu_d, sig_d, n_days)


def annualize(daily):
    """把日收益序列折算成年化收益 + 年化波动，返回 (年收益, 年波动)。"""
    # daily.mean()：算术平均。乘 252 就是年化收益。
    ann_ret = daily.mean() * N_DAYS
    # daily.std(ddof=1)：样本标准差。ddof=1 表示除以 (n−1) 而不是 n（样本估计的标准做法）。
    #   再乘 √252 —— 波动走 √t 路径，和上面除以 √252 正好互相抵消。
    ann_vol = daily.std(ddof=1) * np.sqrt(N_DAYS)
    return ann_ret, ann_vol


def sharpe_annual(ann_ret, ann_vol, rf=RF):
    """年化 Sharpe：给定年化收益、年化波动、无风险利率，返回 Sharpe。"""
    # 分子：超额收益 = 你赚的 − 躺着也能赚的。只留"承担风险换来的那部分"。
    # 分母：波动。收益除以风险 → "每单位风险换多少超额收益"。
    return (ann_ret - rf) / ann_vol


# ---- 1. 模拟两条日收益序列 ----
daily_x = simulate_daily_returns(X_RET, X_VOL, seed=8)   # 策略 X
daily_y = simulate_daily_returns(Y_RET, Y_VOL, seed=33)  # 策略 Y

# ---- 2. 年化，再算 Sharpe ----
ann_ret_x, ann_vol_x = annualize(daily_x)
ann_ret_y, ann_vol_y = annualize(daily_y)

sharpe_x = sharpe_annual(ann_ret_x, ann_vol_x)
sharpe_y = sharpe_annual(ann_ret_y, ann_vol_y)

print(f"无风险利率 rf = {RF:.1%}")
print(f"{'策略':<6}{'年化收益':>10}{'年化波动':>10}{'Sharpe':>10}")
print(f"{'X':<6}{ann_ret_x:>9.2%}{ann_vol_x:>10.2%}{sharpe_x:>10.2f}")
print(f"{'Y':<6}{ann_ret_y:>9.2%}{ann_vol_y:>10.2%}{sharpe_y:>10.2f}")

# 盯住这两行：X 的收益是 Y 的两倍多，但 Sharpe 反而更低。
#   X 靠的是"敢赌"，Y 靠的是"稳"——每单位风险换来的超额收益，Y 更划算。


# ---- 3. 验证两种算法等价：日 Sharpe × √252 == 年化 Sharpe ----
# 日 Sharpe = 日超额收益均值 / 日波动；年化只要再乘 √252。
daily_sharpe_x = (daily_x.mean() - RF / N_DAYS) / daily_x.std(ddof=1)
print(f"\n校验 X：日Sharpe × √252 = {daily_sharpe_x * np.sqrt(N_DAYS):.4f}"
      f"   年化Sharpe = {sharpe_x:.4f}   ← 应该相等")


# ---- 4. 画净值曲线：亲眼看 σ 大的人抖成什么样 ----
# np.cumprod(1 + daily)：把日收益率逐日连乘 → 从 1 块变成多少块（复利）。
#   np.arange(1, N_DAYS + 1)：横轴天数 1, 2, …, 252。
days = np.arange(1, N_DAYS + 1)
nav_x = np.cumprod(1 + daily_x)
nav_y = np.cumprod(1 + daily_y)

layers = [
    # line 层：data 是 (n, 2) 矩阵，每行一个顶点 [x, y]，按行顺序连成折线。
    {"type": "line",
     "data": np.column_stack([days, nav_x]),
     "color": "tab:red", "linestyle": "-"},
    {"type": "line",
     "data": np.column_stack([days, nav_y]),
     "color": "tab:blue", "linestyle": "-"},
]
plot(layers, title="净值曲线：策略 X（红，高收益高波动） vs Y（蓝，低收益低波动）")

# 看完问自己一句：如果这笔钱明年就要用（不能承受中途腰斩），你选哪条？
