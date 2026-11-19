"""教师示例：用模拟客服来电量观察顺序怎样改变相邻关系。"""

# statistics 提供均值与两组数之间的 Pearson 相关系数。
import statistics


def lag_one_correlation(values):
    """计算一阶样本相关；values 是按日期先后排列的数值列表。"""
    # 去掉最后一天，构造每一对中较早的一天。
    earlier = values[:-1]
    # 去掉第一天，构造同一对中较晚的一天。
    later = values[1:]
    # correlation 的第一个参数是较早值列表，第二个是较晚值列表。
    return statistics.correlation(earlier, later)


# 模拟的 12 天客服来电量；它们不是任何企业的真实记录。
calls_in_order = [80, 82, 84, 86, 88, 90, 110, 112, 114, 116, 118, 120]
# 只为演示顺序效应，重新排列相同的 12 个观测值。
calls_reordered = [80, 120, 82, 118, 84, 116, 86, 114, 88, 112, 90, 110]
# 头六天代表较早时期；这个切分保留了当时能看到的信息。
earlier_period = calls_in_order[:6]
# 后六天代表较晚时期，不混入早期估计。
later_period = calls_in_order[6:]
# 打印两种排列的一阶相关，观察相邻配对变化后的结果。
print(f"原顺序一阶相关：{lag_one_correlation(calls_in_order):.3f}")
# 相同观测值、不同顺序，相关结果可能不同。
print(f"重排后一阶相关：{lag_one_correlation(calls_reordered):.3f}")
# mean 的参数是较早时期列表，返回这六天的平均来电量。
print(f"较早六天均值：{statistics.mean(earlier_period):.1f}")
# mean 的参数是较晚时期列表，用它观察时期变化。
print(f"较晚六天均值：{statistics.mean(later_period):.1f}")
