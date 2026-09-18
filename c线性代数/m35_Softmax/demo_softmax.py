# demo_softmax.py
# 演示：怎么把一组"任意分数"变成"概率分布"，以及 temperature 怎么改变这个分布。
#
# ⚠️ 演示数据用 [2.0, 1.0, 0.5, -1.0]，温度用 0.5 / 1.0 / 4.0。
#    你练习时换成 [1.5, 2.8, 0.3, 2.0] 和 0.1 / 1.0 / 5.0——思路一样，数据不同。

import numpy as np
from function.plot import plot

# ---- 1. 先看"最朴素的想法"为什么不行 ----
# 想要概率分布，最直觉的做法：每个数除以总和 → 和就变成 1 了。
# 但试试带负数的分数：
scores = np.array([2.0, 1.0, 0.5, -1.0])
naive = scores / scores.sum()
print("朴素做法 x / x.sum() :", naive)
# → 负数除以正数还是负数。-1.0 那个位置会得到"负的概率"。
# 概率的定义要求每项都在 0~1 之间，这个做法直接违反定义。
# 而且总和也不是 1（正负抵消了），两头都不满足。

# ---- 2. 换成指数：先把所有数"变成正的"，再归一化 ----
# np.exp(x)：自然指数 eˣ，逐元素作用在数组上。
#   参数只有一个 x，返回同形状的数组：每个元素都算一遍 e 的该次方。
#   为什么它正好合适？三个理由：
#     a) eˣ 恒为正 —— 不管输入多负，输出永远 > 0，负概率的问题直接消失
#     b) eˣ 单调递增 —— 大的输入还是大，不会打乱排名
#     c) eˣ 放大差距 —— 差 1.0 的两个分数，指数后差 e 倍，差距被拉开
e = np.exp(scores)
print("exp 之后           :", e)
print("exp 之后求和        :", e.sum())   # np.ndarray.sum() 无参数 = 全部加起来

# ---- 3. 归一化：除以总和，和 = 1 ----
probs = e / e.sum()
print("softmax (T=1)      :", probs)
print("验证：总和 =", probs.sum())        # 一定是 1（浮点数误差下可能是 0.9999...）


# ---- 4. 写成函数，加上 temperature ----
def softmax(scores, T=1.0):
    """把任意实数分数变成概率分布。

    参数:
        scores : 一组分数，list 或 np.ndarray 都行（内部会转成数组）
        T      : temperature，默认 1.0。
                 注意 T 是"除数"——先 scores / T，再走 exp 和归一化。
                 T 小 → 分数差距被放大 → 分布更尖（确定）
                 T 大 → 分数差距被压平 → 分布更平（随机）
    """
    # np.asarray(..., dtype=float)：把输入统一转成浮点数组。
    #   为什么要转？如果传进来的是 Python list，不能直接做数组运算；
    #   而且整数数组做除法会截断，必须显式转成 float。
    x = np.asarray(scores, dtype=float) / T
    e = np.exp(x)
    return e / e.sum()


# ---- 5. 三种温度对比 ----
print("\n--- 温度对比 ---")
for T in [0.5, 1.0, 4.0]:
    p = softmax(scores, T)
    # round(p, 3)：把每个概率四舍五入到 3 位小数，纯粹为了打印好看
    print(f"T={T:<4} -> {np.round(p, 3)}")
# 预期看到的规律：
#   T=0.5 —— 差距被放大，最大那个（2.0）拿到压倒性的概率
#   T=1.0 —— 原始分布
#   T=4.0 —— 差距被压平，四个数越来越接近 0.25（均匀）

# ---- 6. 画图：把"分布形状"变成看得见的东西 ----
# 用统一的 plot()，不写裸 matplotlib。
# 思路：把"第几个候选"当 x，"概率"当 y，温度不同的三组分别画一层散点。
#   layers 里每层靠 type 区分："point" 层的 data 必须是 (n, 2) 矩阵，每行一个 [x, y]。
#   只写 type/data/labels 之外的键会透传给 scatter（这里用 color 区分温度）。
idx = np.arange(len(scores))          # np.arange(4) -> [0, 1, 2, 3]，当 x 坐标

ax = plot(
    [
        # enumerate: 每层一个温度，zip 起来一次生成三层
        {"type": "point",
         "data": np.column_stack([idx, softmax(scores, T)]),  # 拼成 (4, 2) 矩阵
         "color": color, "s": 20, "label": f"T={T}"}
        for T, color in [(0.5, "tab:red"), (1.0, "tab:blue"), (4.0, "tab:green")]
    ],
    title="同一组分数在不同 temperature 下的概率分布",
)
# plot() 返回 matplotlib 的 ax，所以还能在它上面继续加东西——这里补个图例。
ax.legend()

# ---- 附：真实代码里还会多一行 ----
# 你在任何框架里翻 softmax 的实现，几乎都会看到：
#     x = x - np.max(x)      # np.max(x, axis=...) 默认求全局最大值
#     e = np.exp(x)
#     ...
# 这不是在改结果，而是在防溢出：e¹⁰⁰⁰ 会直接算成 inf。
# 减掉最大值后，最大的那一项变成 e⁰ = 1，其余都 ≤ 1，就不会炸。
# 为什么结果不变？因为 softmax 对"整体平移"免疫——分子分母同时乘 e⁻ᵐᵃˣ，比值一样。
# 软线内容，看懂就行，不用自己推。
