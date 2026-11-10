"""教师演示：用 Bootstrap 估计客服工单处理时长中位数的不确定性。

示例使用工单处理时长，而不是学生练习中的交易收益与 Sharpe。
运行后会在本目录写入 demo_bootstrap_distribution.png。
"""

# 导入 NumPy，用于保存样本、随机重抽样和计算分位数。
import numpy as np
# 导入 Matplotlib 的无交互绘图接口，用于保存经验分布图。
import matplotlib.pyplot as plt
# 导入字体属性类，用来指定 macOS 中可被 Matplotlib 加载的中文字体。
from matplotlib.font_manager import FontProperties


# 默认 DejaVu Sans 没有中文字形；这里明确选择系统的 Hiragino Sans GB。
CJK_FONT = FontProperties(fname="/System/Library/Fonts/Hiragino Sans GB.ttc")


def bootstrap_statistics(values, repetitions, statistic, generator):
    """对一个样本反复有放回重抽样，并计算指定统计量。

    参数：
        values: 原始一维样本数组，例如每张工单的处理时长。
        repetitions: 重抽样次数；次数越多，经验分布越平滑。
        statistic: 接受一个一维数组、返回一个数值的函数，例如 np.median。
        generator: NumPy 随机数生成器，传入它可使结果复现。
    返回：
        长度为 repetitions 的数组，其中每个元素是一次重抽样的统计量。
    """
    # 样本量必须保持不变：每次都从原始的 n 个观测里抽 n 个。
    sample_size = len(values)
    # 创建结果数组，预留每一次统计量的位置。
    results = np.empty(repetitions)
    # 重复进行“抽样 → 统计”这一完整过程。
    for index in range(repetitions):
        # replace=True 表示有放回；同一个观测可以在一次重抽样中出现多次。
        resample = generator.choice(values, size=sample_size, replace=True)
        # 对本次重抽样计算同一种统计量，并记录下来。
        results[index] = statistic(resample)
    # 所有结果合起来就是统计量的经验分布。
    return results


# 18 张假想客服工单的处理时长，单位为分钟；其中包含几张明显较慢的工单。
ticket_minutes = np.array([11, 9, 14, 12, 10, 16, 13, 8, 15, 12, 11, 18, 10, 14, 9, 25, 13, 17])
# 固定随机种子，使教师演示每次得到同样的结果。
rng = np.random.default_rng(seed=20261110)
# 先计算原始样本的单次中位数；它只是一个点估计。
observed_median = np.median(ticket_minutes)
# 有放回地重抽 5,000 次，每次都重新计算中位数。
median_distribution = bootstrap_statistics(ticket_minutes, repetitions=5_000, statistic=np.median, generator=rng)
# 取中间 90% 的范围，描述本样本下中位数可能的波动区间。
lower, upper = np.percentile(median_distribution, [5, 95])
# 输出点估计、重抽样后的中心和区间，比较“一个数”与“一个分布”。
print(f"原始样本中位数: {observed_median:.1f} 分钟")
print(f"Bootstrap 中位数: {median_distribution.mean():.2f} 分钟")
print(f"90% 经验区间: [{lower:.1f}, {upper:.1f}] 分钟")

# 建立一张图，展示 5,000 个中位数组成的经验分布。
figure, axis = plt.subplots(figsize=(7, 4))
# 直方图的每根柱子统计一个中位数区间内出现了多少次。
axis.hist(median_distribution, bins=16, color="#4C78A8", edgecolor="white")
# 画出原始样本中位数的位置，方便与分布比较。
axis.axvline(observed_median, color="#E45756", linewidth=2, label="原始样本中位数")
# 为图提供能独立阅读的标题和坐标轴含义，并为中文指定字体。
axis.set_title("Bootstrap：工单处理时长中位数的经验分布", fontproperties=CJK_FONT)
axis.set_xlabel("每次重抽样得到的中位数（分钟）", fontproperties=CJK_FONT)
axis.set_ylabel("出现次数", fontproperties=CJK_FONT)
# 展示图例，指出红线代表什么。
axis.legend(prop=CJK_FONT)
# 调整留白，避免中文标签被裁切。
figure.tight_layout()
# 保存教师演示图到本文件所在目录，不弹出交互窗口。
figure.savefig("demo_bootstrap_distribution.png", dpi=150)
