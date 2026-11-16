"""
实现一次蒙特卡洛模拟

收益就是每天持有股票的收益，没有策略收益

需要回答：如果还是像这样一直持有，未来20天亏钱的概率是多少
"""
import csv
from pathlib import Path

import numpy as np

# 收盘价数据使用沪深 300 历史日线；此处计算普通日收益率。
DATA_PATH = Path.home() / "stu/py_practice_file/practice_data_source/index_daily/000300.csv"


def close_to_rate_list(csv_path: Path) -> np.ndarray:
    """按日期排序收盘价，返回相邻交易日的普通收益率数组。"""
    with csv_path.open(encoding="utf-8-sig", newline="") as file:
        rows = sorted(csv.DictReader(file), key=lambda row: row["date"])

    close = np.array([float(row["close"]) for row in rows], dtype=float)
    if len(close) < 2 or np.any(~np.isfinite(close)) or np.any(close <= 0):
        raise ValueError("需要至少两个有效且大于 0 的收盘价")

    rate_list = (close[1:] - close[:-1]) / close[:-1]
    return rate_list


rate_list = close_to_rate_list(DATA_PATH)[-252:]


# 从历史日收益中有放回抽样；同一个 seed 会得到相同的路径。
def bootstrap(arr: np.ndarray, n_sample: int, sample_len: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    result = []
    for _ in range(n_sample):
        # 下标
        one_group_idx = rng.integers(low=0, high=len(arr), size=sample_len)
        # 根据下标抽样
        one_group = arr[one_group_idx]
        result.append(one_group)
    # 转成numpy二维数组
    return np.array(result)


def normal_sample(mean: float, std: float, n_sample: int, sample_len: int, seed: int) -> np.ndarray:
    """按历史样本估计的均值和标准差，生成正态日收益路径。"""
    rng = np.random.default_rng(seed)
    result = []
    for _ in range(n_sample):
        # 每次生成一条包含 sample_len 个交易日的路径。
        one_group = rng.normal(loc=mean, scale=std, size=sample_len)
        result.append(one_group)
    return np.array(result)


def loss_proportion(paths: np.ndarray) -> float:
    # 逐条路径计算复利收益，并统计期末低于起点的路径数。
    loss_count = 0
    for row in paths:
        prod = 1.0
        for r in row:
            prod = prod * (r + 1)
        if prod - 1 < 0:
            loss_count += 1
    return loss_count / len(paths)


if __name__ == "__main__":
    sample_mean = float(rate_list.mean())
    sample_std = float(rate_list.std(ddof=1))
    print(f"历史日收益：样本量={len(rate_list)}, 均值={sample_mean:.4%}, 样本标准差={sample_std:.4%}")

    for n_sample, seed in [(1_000, 50), (1_000, 51), (100_000, 50), (100_000, 51)]:
        paths = bootstrap(rate_list, n_sample, 20, seed)
        proportion = loss_proportion(paths)
        print(f"经验重抽样 路径数={n_sample:>6}, seed={seed}: 20日亏损比例={proportion:.2%}")

    # 只改变日收益生成规则，保持路径数和种子不变，方便比较。
    normal_paths = normal_sample(sample_mean, sample_std, 100_000, 20, 50)
    normal_proportion = loss_proportion(normal_paths)
    print(f"正态参数模拟 路径数=100000, seed=50: 20日亏损比例={normal_proportion:.2%}")
