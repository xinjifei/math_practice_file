"""教师演示：在多个“资产截面”上比较 Pearson IC 与 Rank IC。

示例故意使用 12 个假想地区的消费信号和下一季度需求增速；
这不是学生练习中“月度股票因子 + 下月收益”的数据。
"""

# 导入 NumPy，用来创建和处理一维数值数组。
import numpy as np


def pearson_correlation(left, right):
    """计算两组同长度数据的 Pearson 相关系数。

    参数：
        left: 第一组一维数值数组。
        right: 第二组一维数值数组，顺序必须与 left 对齐。
    返回：
        一个介于 -1 和 1 之间的 float。
    """
    # corrcoef 生成 2×2 相关矩阵，非对角线元素就是两组数据之间的相关系数。
    return float(np.corrcoef(left, right)[0, 1])


def average_ranks(values):
    """把数值转成从 1 开始的排名；相同数值取并列名次的平均值。

    参数：
        values: 一维数值数组。
    返回：
        与 values 等长的浮点排名数组。
    """
    # argsort 给出从小到大的原始位置顺序。
    order = np.argsort(values, kind="stable")
    # 创建保存每个原始位置排名的数组。
    ranks = np.empty(len(values), dtype=float)
    # 从第一个已排序元素开始寻找并列组。
    start = 0
    # 逐组处理相同的数值。
    while start < len(values):
        # 先假定当前并列组只有一个元素。
        end = start + 1
        # 向后扩展，直到遇到不同的数值或数组末尾。
        while end < len(values) and values[order[end]] == values[order[start]]:
            end += 1
        # Python 下标从 0 开始，排名从 1 开始；并列组取首末名次的平均。
        mean_rank = (start + 1 + end) / 2
        # 把同一个平均排名写回这些元素原来的位置。
        ranks[order[start:end]] = mean_rank
        # 下一次从尚未处理的元素开始。
        start = end
    # 返回排名数组。
    return ranks


def calculate_ics(signal, future_result):
    """计算一个截面的两种 IC。

    参数：
        signal: 当前时点的信号数组，每个元素对应一个对象。
        future_result: 同一批对象下一期的结果数组，顺序必须与 signal 对齐。
    返回：
        (pearson_ic, rank_ic)，均为 float。
    """
    # 对原始数值直接计算 Pearson IC，衡量线性关系。
    pearson_value = pearson_correlation(signal, future_result)
    # 两组数分别转成排名，再计算 Pearson 相关，就是 Spearman Rank IC。
    rank_ic = pearson_correlation(average_ranks(signal), average_ranks(future_result))
    # 把两个指标一起交给调用者。
    return pearson_value, rank_ic


def make_cross_section(generator, size, period):
    """生成一个教学用截面。

    参数：
        generator: NumPy 的随机数生成器，使随机过程可复现。
        size: 截面中对象的数量。
        period: 当前期编号，用来让不同期的信号强度略有差异。
    返回：
        (signal, future_result) 两个同长度 NumPy 数组。
    """
    # 为 12 个地区生成当前消费强度信号。
    signal = generator.normal(loc=0.0, scale=1.0, size=size)
    # 让信号对下一季需求增速有一个温和的正向贡献。
    signal_strength = 0.25 if period != 2 else 0.05
    # 加入独立噪音，避免结果变成完美相关。
    noise = generator.normal(loc=0.0, scale=0.8, size=size)
    # 未来结果由“信号贡献 + 噪音”构成。
    future_result = signal_strength * signal + noise
    # 返回同一截面的当前信号和下一期结果。
    return signal, future_result


# 固定随机种子，保证每次运行都得到同一组教学数据。
rng = np.random.default_rng(seed=20261108)
# 创建两个列表，收集每期 IC，形成一段 IC 序列。
pearson_series = []
rank_series = []

# 模拟 4 个季度；每个季度都在一个新的截面上评估预测力。
for quarter in range(4):
    # 生成本季度的 12 个地区及其下一季度结果。
    signal, future_result = make_cross_section(rng, size=12, period=quarter)
    # 在同一截面上计算两种 IC。
    pearson_ic, rank_ic = calculate_ics(signal, future_result)
    # 把本期数值保存进序列，之后才能评估稳定性。
    pearson_series.append(pearson_ic)
    rank_series.append(rank_ic)
    # 输出每期结果，便于观察预测力是否持续存在。
    print(f"Q{quarter + 1}: Pearson IC={pearson_ic:+.3f}, Rank IC={rank_ic:+.3f}")

# 将 Python 列表转为数组，以便计算均值和标准差。
pearson_series = np.array(pearson_series)
rank_series = np.array(rank_series)
# 汇总多期表现：均值代表平均方向与强度，标准差提示稳定性。
print(f"平均 Pearson IC: {pearson_series.mean():+.3f}，标准差: {pearson_series.std():.3f}")
print(f"平均 Rank IC:    {rank_series.mean():+.3f}，标准差: {rank_series.std():.3f}")

# 取最后一期作对照，并人为制造一个异常大的未来结果。
outlier_result = future_result.copy()
# 仅改变一个对象，模拟极端观察值可能扭曲线性相关的情况。
outlier_result[0] = 12.0
# 重新计算后，比较两种指标受极端值的影响。
outlier_pearson, outlier_rank = calculate_ics(signal, outlier_result)
print(f"加入极端值后: Pearson IC={outlier_pearson:+.3f}, Rank IC={outlier_rank:+.3f}")
