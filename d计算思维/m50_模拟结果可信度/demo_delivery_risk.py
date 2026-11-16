"""教师示例：从历史配送记录估计十单班次触发赔付的机会。"""

# NumPy 提供随机数生成器与数组运算。
import numpy as np


def estimate_compensation_rate(on_time_probability, orders_per_shift, shifts, seed):
    """估计一个班次至少有两单延迟而触发赔付的比例。

    on_time_probability: 每单准时的模型概率，取值在 0 到 1 之间。
    orders_per_shift: 一个班次内的订单数量。
    shifts: 要模拟的班次数量；班次越多，模拟抽样波动通常越小。
    seed: 随机种子；传入同一个整数可复现抽样结果。
    """
    # 创建独立的随机数生成器。
    generator = np.random.default_rng(seed)
    # 每行代表一个班次，每列代表其中一单；小于准时概率表示准时。
    on_time = generator.random((shifts, orders_per_shift)) < on_time_probability
    # 对每行计算延迟的订单数。
    late_count = (~on_time).sum(axis=1)
    # 统计延迟至少两单的班次占全部模拟班次的比例。
    return np.mean(late_count >= 2)


# 十二笔历史配送的示例观测；1 表示准时，0 表示延迟。
observed_on_time = np.array([1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1])
# 从观测列表估计准时概率，而不是直接把未来概率当成已知事实。
base_probability = observed_on_time.mean()
# 少量班次模拟用于观察抽样波动。
small_run = estimate_compensation_rate(base_probability, 10, 1_000, 50)
# 相同假设下增加模拟班次，观察估计是否更稳定。
large_run = estimate_compensation_rate(base_probability, 10, 100_000, 51)
# 设定一个更保守的准时概率，比较模型假设改变后的输出。
changed_rule = estimate_compensation_rate(base_probability - 0.10, 10, 100_000, 52)
# 打印三组结果，分别对照模拟次数和生成规则的变化。
print(f"历史准时比例：{base_probability:.1%}（仅 {len(observed_on_time)} 笔示例记录）")
print(f"按该比例，1,000 班次：赔付比例约 {small_run:.1%}")
print(f"按该比例，100,000 班次：赔付比例约 {large_run:.1%}")
print(f"准时概率降低 10 个百分点，100,000 班次：赔付比例约 {changed_rule:.1%}")
