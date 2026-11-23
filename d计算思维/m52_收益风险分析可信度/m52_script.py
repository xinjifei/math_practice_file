from pathlib import Path
import numpy as np
import pandas as pd

path = Path.home() / "stu/py_practice_file/practice_data_source/index_daily/000300.csv"

df = pd.read_csv(path)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["close"] = pd.to_numeric(df["close"], errors="coerce")

# 1. 检查原始数据
assert df["date"].notna().all(), "存在无效日期"
assert not df["date"].duplicated().any(), "存在重复日期"
assert df["close"].notna().all(), "存在缺失收盘价"
assert (df["close"] > 0).all(), "存在非正收盘价"

df = df.sort_values("date").reset_index(drop=True)

# 2. 计算日收益（保留对应日期）
df["return"] = df["close"].pct_change()
returns = df.dropna(subset=["return"]).copy()

# 3. 最后315个有效收益
assert len(returns) >= 315, "有效收益不足315条"

recent = returns.tail(315).reset_index(drop=True)
analysis = recent.iloc[:252].copy()
test = recent.iloc[252:].copy()


def calculate_metrics(data):
    r = data["return"]

    # 任务A：平均日收益
    mean_return = r.mean()

    # 任务B：样本标准差（ddof=1）
    std_return = r.std(ddof=1)

    # 任务C：实际复合收益
    compound_return = (1 + r).prod() - 1

    # 最大回撤：以本段起点净值1作为初始峰值
    equity = np.r_[1.0, np.cumprod(1 + r.to_numpy())]
    peaks = np.maximum.accumulate(equity)
    max_drawdown = (equity / peaks - 1).min()

    return mean_return, std_return, compound_return, max_drawdown


results = {}
for name, data in [("分析段", analysis), ("留出段", test)]:
    mean, std, compound, mdd = calculate_metrics(data)
    results[name] = (mean, std, compound, mdd)

    print(f"\n{name}")
    print("日期：", data["date"].min().date(),
          "至", data["date"].max().date())
    print("样本量：", len(data))
    print(f"平均日收益：{mean:.4%}")
    print(f"样本标准差：{std:.4%}")
    print(f"实际复合收益：{compound:.4%}")
    print(f"最大回撤：{mdd:.4%}")

# 4. 两段同口径对照
# 实际复合收益对应的天数不同（252 与 63），不能直接比大小；
# 这里另外按同样的 252 个交易日折算成年化收益，再比较。
TRADING_DAYS = 252


def annualized_return(compound_return, n_days):
    return (1 + compound_return) ** (TRADING_DAYS / n_days) - 1


print("\n两段对照（同口径）")
for name, data in [("分析段", analysis), ("留出段", test)]:
    mean, std, compound, mdd = results[name]
    annual = annualized_return(compound, len(data))
    print(f"{name}：平均日收益 {mean:.4%}，样本标准差 {std:.4%}，"
          f"最大回撤 {mdd:.4%}，按252日折算的年化收益 {annual:.4%}")

analysis_annual = annualized_return(results["分析段"][2], len(analysis))
test_annual = annualized_return(results["留出段"][2], len(test))

print(f"平均日收益之差（分析段 − 留出段）："
      f"{results['分析段'][0] - results['留出段'][0]:.4%}")
print(f"样本标准差之差（分析段 − 留出段）："
      f"{results['分析段'][1] - results['留出段'][1]:.4%}")
print(f"最大回撤之差（分析段 − 留出段）："
      f"{results['分析段'][3] - results['留出段'][3]:.4%}")
print(f"年化收益之差（分析段 − 留出段）：{analysis_annual - test_annual:.4%}")

# 5. 20 日亏损比例：两段用不同方法各算一次
# 分析段：有放回独立重抽样 20 个日收益，复利后看是否小于 0。
# 留出段：只按历史时间顺序取连续 20 日窗口，数其中亏损窗口的比例。
WINDOW_DAYS = 20
N_PATHS = 10_000
SEED = 52

rng = np.random.default_rng(SEED)
analysis_r = analysis["return"].to_numpy()
idx = rng.integers(0, len(analysis_r), size=(N_PATHS, WINDOW_DAYS))
paths = analysis_r[idx]
path_returns = np.prod(1 + paths, axis=1) - 1
bootstrap_loss_ratio = (path_returns < 0).mean()

test_r = test["return"].to_numpy()
window_returns = np.array([
    np.prod(1 + test_r[i:i + WINDOW_DAYS]) - 1
    for i in range(len(test_r) - WINDOW_DAYS + 1)
])
rolling_loss_ratio = (window_returns < 0).mean()

print(f"\n20 日亏损比例")
print(f"分析段独立重抽样（{N_PATHS} 条路径，seed={SEED}）："
      f"{bootstrap_loss_ratio:.2%}")
print(f"留出段连续 20 日窗口（{len(window_returns)} 个重叠窗口）："
      f"{rolling_loss_ratio:.2%}")
print(f"留出段窗口中亏损个数：{int((window_returns < 0).sum())}"
      f"/{len(window_returns)}")

