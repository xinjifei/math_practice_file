# note 里的思想实验：两个策略的 Sharpe 列表，均值都是 10，但“稳不稳”完全不同
# 每个元素 = 一次回测得到的 Sharpe；对它们求均值，就是“平均 Sharpe”这个统计量

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pathlib import Path


CJK_FONT = FontProperties(fname="/System/Library/Fonts/Hiragino Sans GB.ttc")


def bootstrap_mean(values: list, reps: int = 10_000, seed: int = 49) -> np.ndarray:
    """有放回地抽 len(values) 个观测，重复 reps 次，返回每次重抽样得到的均值。"""
    values = np.array(values)
    rng = np.random.default_rng(seed)   # 固定种子，每次运行结果一样
    n = len(values)
    means = np.empty(reps)
    for i in range(reps):
        # replace=True 就是“有放回”：抽到过的观测仍留在样本池里，可以被再次抽中
        resample = rng.choice(values, size=n, replace=True)
        means[i] = resample.mean()
    return means


A = [0] * 9 + [100]   # 9 次 0，1 次 100
B = [10] * 10         # 10 次全是 10

a_means = bootstrap_mean(A)
b_means = bootstrap_mean(B)

print("======== 点估计 vs 经验分布 ========")
for name, values, means in [("A", A, a_means), ("B", B, b_means)]:
    lo, hi = np.percentile(means, [5, 95])
    print(f"{name}: 原样本均值={np.mean(values):6.2f} | "
          f"bootstrap均值={means.mean():6.2f} | "
          f"标准差={means.std():6.2f} | "
          f"90%区间=[{lo:.2f}, {hi:.2f}]")

print("\n======== A 的重抽样细节 ========")
print(f"重抽样均值出现过的取值: {np.unique(np.round(a_means, 2))}")
print(f"（理论上只可能是 0, 10, 20, ..., 100，即“抽中 100 的次数 × 10”）")
print(f"均值=0 的比例: {np.mean(a_means == 0):.3f}（理论 P(10 次都没抽中 100) = 0.9^10 = {0.9**10:.3f}）")
print(f"均值>10 的比例: {np.mean(a_means > 10):.3f}")
print(f"B 的重抽样均值全部等于 10: {np.all(b_means == 10)}")

a_lo, a_hi = np.percentile(a_means, [5, 95])
print(f"\n观察：B 的分布宽度为 0 —— 样本里本来就没有变化，bootstrap 变不出变化；"
      f"A 的 90% 区间是 [{a_lo:.0f}, {a_hi:.0f}]，{np.mean(a_means == 0):.0%} 的重抽样均值直接归零。")

# 两张直方图并排：同样的点估计 10，分布一个摊到 0~100，一个缩成一个尖峰
figure, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
bins = np.arange(-2.5, 105, 5)   # 每 5 一格，0/10/.../100 都落在格子正中
for axis, title, means in [
    (axes[0], "A: 9 个 0 + 1 个 100", a_means),
    (axes[1], "B: 10 个 10", b_means),
]:
    axis.hist(means, bins=bins, color="#4C78A8", edgecolor="white")
    axis.set_title(title, fontproperties=CJK_FONT)
    axis.set_xlabel("每次重抽样得到的平均 Sharpe", fontproperties=CJK_FONT)
    axis.set_xlim(-5, 105)
axes[0].set_ylabel("出现次数", fontproperties=CJK_FONT)
figure.suptitle("思想实验：均值都是 10，Bootstrap 分布完全不同", fontproperties=CJK_FONT)
figure.tight_layout()

out_path = Path(__file__).resolve().parent / "m49_bootstrap_thought_experiment.png"
figure.savefig(out_path, dpi=150)
print(f"\n图已保存: {out_path.name}")
