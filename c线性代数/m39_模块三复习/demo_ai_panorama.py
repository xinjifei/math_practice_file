# demo_ai_panorama.py
# 演示：把模块三的整条链，压缩成一个能跑起来的最小闭环。
#
#      logits ──softmax──▶ 概率分布 ──交叉熵──▶ 一个分数 ──梯度下降──▶ 新的 logits
#         ▲                                                                │
#         └──────────────────────── 转一圈 ───────────────────────────────┘
#
#   这一圈就是【输入 → 输出概率 → 打分器 → 改进器】的全部。
#   真实训练里前面还有一大段（文本 → Token → Embedding → Transformer 的矩阵乘法），
#   那些今天不跑 —— 它们是"原材料怎么来"，而这一圈是"拿到原材料之后怎么学"。
#
# ⚠️ 演示用 4 类、真实标签是第 3 类；你练习用 3 类、真实标签是第 1 类。数据完全不同。

import numpy as np
from function.plot import plot


# ---- 两个函数，都是你这几天自己写过的 ----
def softmax(z):
    """m35：把任意一串实数压成概率分布（每个都 > 0，加起来 = 1）。

    参数 z：一维数组，叫 logits —— 模型给每一类的"原始分数"，可正可负、可大可小。
    返回：同样长度的一维数组，就是概率。
    """
    z = np.asarray(z, dtype=float)   # 不管传进来是 list 还是 array，统一成 float 数组
    z = z - np.max(z)                # 每项都减掉最大值 —— 纯为了数值稳定（exp 太大要溢出），不改变结果
    e = np.exp(z)                    # 逐元素取 e 的幂，把实轴压到 (0, +∞)
    return e / np.sum(e)             # 除以总和 —— 这一步才让它们加起来正好等于 1


def cross_entropy(p, q):
    """m38：真实分布 p 和预测分布 q 的差距，越小越好。

    ⚠️ 这里用自然对数 ln，而 m37/m38 你用的是 log2。
       换底只差一个常数倍（m38 验收里划到"可外包"的那条），所以两者形状一模一样，
       只是单位不同（log2 是 bit）。用 ln 是因为下一段那个梯度公式只在 ln 下长这样。
    """
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    safe_q = np.where(q > 0, q, 1.0)  # log(0) = -inf，把 0 顶成 1.0 挡掉（q 全 > 0 时用不上）
    return -np.sum(p * np.log(safe_q))


# ---- 1. 前向：一串分数 → 概率 → 一个分数 ----
z = np.array([2.0, 1.0, 0.5, -1.0])   # 4 类，第 4 类分数最低 —— 模型最不看好它
y = np.array([0.0, 0.0, 1.0, 0.0])    # 真实标签：正确答案是第 3 类（one-hot，m38 学的）

q = softmax(z)                        # 分数 → 概率
print(f"logits        = {z}")
print(f"softmax → {np.round(q, 4)}   加起来 = {q.sum():.4f}")
print(f"交叉熵        = {cross_entropy(y, q):.4f}")
# 注意 q 里第 4 类还有 0.05 左右的概率 —— softmax 永远不会吐出正好 0（m35 的结论）。
# 这就是为什么真实框架里很少真撞上 log(0) 那个 +∞。


# ---- 2. 手动挪一步：只把"正确类"的分数往上抬一点，看分数怎么变 ----
# 这一段是在验证 m38 硬线2 的那句话：打分器对"微小的改进"是有反应的。
z_up = z + np.array([0.0, 0.0, 1.0, 0.0])   # 只给第 3 类（正确类）+1，别的都不动

print(f"\n把正确类的 logits 从 {z[2]} 抬到 {z_up[2]}：")
print(f"  正确类的概率  {q[2]:.4f} → {softmax(z_up)[2]:.4f}")
print(f"  交叉熵        {cross_entropy(y, q):.4f} → {cross_entropy(y, softmax(z_up)):.4f}")
# 概率动了，分数就跟着动了 —— 而且是在没有任何一类"被判错"的情况下动的。
# 换成准确率（判对=1 / 判错=0），这一步它纹丝不动：本来就已经判对了。
# 这就是 m36 那个"改进器"为什么必须有交叉熵当搭档。


# ---- 3. 自动挪：梯度下降 = "每一步都往对的方向挪" ----
# 梯度公式：dL/dz = softmax(z) - y
# 这个公式的推导在 m38 里划到"可外包"了，今天只当结论用。它说的是：
#     每个类的分数，按"我预测的概率 - 真实概率"来修。
#     q 比 y 大的类（猜多了）往下压，q 比 y 小的类（猜少了）往上抬。
# 代入 one-hot 的 y：正确类被往上抬，其余三类按各自概率大小被往下压。
losses = []                                # 每一轮的分数，等一下画曲线要用
z_cur = np.array([2.0, 1.0, 0.5, -1.0])    # 从同一组 logits 出发
lr = 0.5                                   # 学习率：每步挪多大。m36 学过的那个旋钮

for step in range(20):
    q_cur = softmax(z_cur)                 # 前向：算这一步的概率
    loss = cross_entropy(y, q_cur)         # 打分器：算这一步考了多少分
    losses.append([step, loss])            # 存成 [x, y] —— 画图要 (n, 2) 的形状
    z_cur = z_cur - lr * (q_cur - y)       # ← 整个模块的最后一行：改进器

print(f"\n20 步之后：交叉熵 {losses[0][1]:.4f} → {losses[-1][1]:.4f}")
print(f"此时的概率分布：{np.round(softmax(z_cur), 4)}")
# loss 一路降到很接近 0：正确类的概率被推到了接近 1。
# "训练 = 最小化交叉熵 = 把正确 token 的概率往上推" —— m38 硬线3 那句话，就是这 20 行。

# ---- 4. 画出来 ----
# 用统一的 plot()：point 层，data 必须是 (n, 2) 矩阵，每行一个 [x, y]。
# s = 点的大小 —— 这里只有 20 个点，调大一点才看得清。
plot(
    [{"type": "point",
      "data": np.array(losses),
      "color": "tab:red",
      "s": 40}],
    title="每一步都在把交叉熵往下压",
)
