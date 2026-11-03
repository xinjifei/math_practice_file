"""最大回撤教师 demo：用一条净值曲线找到最深的峰谷落差。"""

# 导入 NumPy，用它处理数值数组和累计最大值。
import numpy as np


# 定义计算回撤的函数。
# 参数 values：按时间顺序排列的累计净值，例如 [100, 108, 104]。
# 返回值：滚动峰值、回撤序列、最大回撤的峰值位置和谷底位置。
def calculate_drawdown(values: np.ndarray):
    # maximum.accumulate 会在每个位置记录“到目前为止见过的最高净值”。
    running_peak = np.maximum.accumulate(values)
    # 当前净值减去历史峰值，再除以历史峰值；下跌时结果为负数。
    drawdown = (values - running_peak) / running_peak
    # argmin 返回回撤序列中最小值的位置，也就是最深谷底的位置。
    trough_index = int(np.argmin(drawdown))
    # 只在谷底及其之前寻找最高净值，保证峰值一定发生在谷底之前。
    peak_index = int(np.argmax(values[: trough_index + 1]))
    # 把计算结果交还给调用者。
    return running_peak, drawdown, peak_index, trough_index


# 这组净值是教师示例；学生练习会从另一组每日收益率生成净值。
net_values = np.array([100.0, 108.0, 104.0, 112.0, 107.0, 98.0, 103.0])
# 调用函数，接收四个结果。
peaks, drawdowns, peak_at, trough_at = calculate_drawdown(net_values)
# 最深回撤就是回撤序列中的最小值。
max_drawdown = drawdowns[trough_at]

# 打印原始净值，便于和后面的峰值、回撤逐点对照。
print("累计净值：", net_values)
# 打印每个时点之前出现过的最高净值。
print("滚动峰值：", peaks)
# 把回撤转换成百分比，只为让输出更容易阅读。
print("回撤序列：", np.round(drawdowns * 100, 2), "%")
# 打印最深回撤及其峰谷位置。
print(f"最大回撤：{max_drawdown:.2%}")
# 打印峰值时点和对应净值。
print(f"峰值位置：{peak_at}，峰值：{net_values[peak_at]:.2f}")
# 打印谷底时点和对应净值。
print(f"谷底位置：{trough_at}，谷底：{net_values[trough_at]:.2f}")
