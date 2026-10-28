# -*- coding: utf-8 -*-
# demo_bigo_growth.py
# 演示：同一个"找东西"的任务，两种写法，输入 n 变大时耗时怎么走。
#
#   按位置扫（list）：从头一个一个比 → n 翻 10 倍，要走 10 倍的路   → 增长趋势 O(n)
#   按 key 取（dict）：直接算出该去第几格 → n 翻多少倍，都只有那一步 → 增长趋势 O(1)
#
# Big O 说的就是这个"增长趋势"，不是秒数。所以下面画的是：
#   X = 输入规模 n（对数轴），Y = 单次操作耗时（微秒）
# 要看的是线的"形状"：一条往上冲的斜线，一条贴地的水平线。
#
# ⚠️ demo 对比的是 list 逐个比对(O(n)) 和 dict 直接取(O(1))，
#    练习要你实现的是 linear_search(O(n)) vs binary_search(O(log n)) ——
#    规模和场景都不同，别把 demo 的数字当成练习的答案。

import time

import matplotlib.pyplot as plt
import numpy as np

from function.plot import plot

# ---- 参数（全集中在开头，改这里就够） ----
SIZES = [10_000, 100_000, 1_000_000]   # 三档输入规模 n
REPEAT = 5                             # 每档测 5 轮，取最快一轮
LOOKUPS = 200_000                      # dict 单次取值太快测不准，攒一批再除回单次


def scan_for(data, target):
    """按位置扫：从头一个一个比，比到就停。n 越大，平均要走越多格 → O(n)。"""
    for x in data:            # 走一遍列表，代价和列表长度成正比
        if x == target:       # 运气好第 1 个就中，运气差（最坏情况）要走到最后一个
            return True
    return False


def lookup_batch(index, key, times):
    """按 key 取：字典直接算出该去第几格，和里面装了多少个无关 → O(1)。"""
    value = None
    for _ in range(times):    # 下划线 _ = "这个变量我不用"，只是用来重复 times 次
        value = index[key]    # 一步到位，不管字典里是 1 万个还是 100 万个
    return value


def best_of(func, repeat=REPEAT):
    """跑 repeat 轮，返回最快的一轮耗时（秒）。

    参数:
        func  : 一个"不带参数、调用就执行"的东西（下面用 lambda 包了一层）
        repeat: 测几轮

    为什么不取平均：操作系统调度、内存回收只会让某一次变慢，不会让它变快，
    所以"最快的那次"最接近纯算法本身的耗时。这是性能测试的常见做法。
    """
    best = float("inf")              # 先设成无穷大，第一轮一定被替换
    for _ in range(repeat):          # 测 repeat 轮
        start = time.perf_counter()  # 高精度秒表，单位秒（比 time.time() 更稳）
        func()                       # 执行要测的那个动作
        elapsed = time.perf_counter() - start
        best = min(best, elapsed)    # 只保留最小值
    return best


scan_us = []      # 每档 n 下，"扫描一次"的耗时（微秒）
lookup_us = []    # 每档 n 下，"取一次 key"的耗时（微秒）

for n in SIZES:
    data = list(range(n))                 # 一列 0..n-1
    index = {key: key for key in data}    # 同样的内容装进字典（key → value）

    target = n - 1                        # 查最后一个 —— 扫描的最坏情况：要走到末尾

    # lambda：临时写一个没名字的小函数。冒号前是参数（这里是空的），后面是函数体。
    # best_of 要一个"调用就干活"的东西，所以把带参数的调用包进 lambda 里。
    scan_sec = best_of(lambda: scan_for(data, target))
    lookup_sec = best_of(lambda: lookup_batch(index, target, LOOKUPS))

    scan_us.append(scan_sec * 1e6)                  # 秒 → 微秒
    lookup_us.append(lookup_sec * 1e6 / LOOKUPS)    # 一批 ÷ 次数 = 单次

# ---- 数字表：曲线看形状，表看倍数 ----
print(f"{'n':>10} {'扫描 O(n)':>14} {'取key O(1)':>14}   （微秒/次）")
for n, a, b in zip(SIZES, scan_us, lookup_us):
    print(f"{n:>10,} {a:>14.1f} {b:>14.3f}")

for i in range(1, len(SIZES)):
    n_ratio = SIZES[i] / SIZES[i - 1]
    print(
        f"n 放大 {n_ratio:.0f} 倍 → 扫描放大 {scan_us[i] / scan_us[i - 1]:.1f} 倍，"
        f"取key 放大 {lookup_us[i] / lookup_us[i - 1]:.1f} 倍"
    )

# ---- 画图：X = n，Y = 单次耗时 ----
ax = plot(
    [
        {"type": "line",
         "data": np.array([[n, t] for n, t in zip(SIZES, scan_us)]),
         "color": "tab:red", "linestyle": "-", "linewidth": 2},
        {"type": "line",
         "data": np.array([[n, t] for n, t in zip(SIZES, lookup_us)]),
         "color": "tab:green", "linestyle": "-", "linewidth": 2},
    ],
    title="输入规模 n vs 单次耗时：一条往上冲，一条贴地",
    show=False,   # 先不显示，下面还要改坐标轴
)

# 横轴换成对数轴：n 是 1 万 / 10 万 / 100 万，跨了三个数量级，
# 线性轴上前两个点会一起挤在最左边看不清。
# 参数 set_xscale("log")：横轴刻度改成"每格 ×10"（默认是 "linear" 等距）。
ax.set_xscale("log")

plt.show()   # 全部改完，再一次性显示
