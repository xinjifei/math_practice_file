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

    rate_arr = np.array((close[1:] - close[:-1]) / close[:-1])
    return rate_arr

rate_arr = close_to_rate_list(DATA_PATH)[-252:]

# 一阶自相关系数
def corr(rate_arr):
    yesterday = rate_arr[:-1]
    today = rate_arr[1:]
    matrix = np.corrcoef(yesterday, today)
    corr_value = matrix[0][1]
    return corr_value


if __name__ == "__main__":
    DATA_PATH = Path.home() / "stu/py_practice_file/practice_data_source/index_daily/000300.csv"
    rng = np.random.default_rng(51)

    # 取最近315个日收益率
    rate_arr = close_to_rate_list(DATA_PATH)[-315:]

    # 严格按照时间分割
    train = rate_arr[:252]
    test = rate_arr[252:]

    # 一阶自相关对照
    train_disorder = rng.permutation(train)

    print("分析段一阶相关:", corr(train))
    print("打乱后的一阶相关:", corr(train_disorder))
    print("留出段一阶相关:", corr(test))

    # 均值和标准差
    print(f"\n分析段均值:", np.mean(train))
    print("留出段均值:", np.mean(test))

    print(f"\n分析段标准差:", np.std(train, ddof=1))
    print("留出段标准差:", np.std(test, ddof=1))