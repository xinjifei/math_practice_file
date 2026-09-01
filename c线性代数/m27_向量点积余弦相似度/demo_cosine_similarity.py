# -*- coding: utf-8 -*-
"""
demo_cosine_similarity.py —— 点积与余弦相似度的参考脚手架

注意：这里用的数据和练习不一样！
  练习：v1=[1,2], v2=[2,4], v3=[-2,1]
  本 demo：a=[3,1], b=[6,2], c=[-1,3]

目的：让你看懂「思路」，然后自己动手写练习的数据。
  思路 = 三步：
    1. 定义向量
    2. 写 cosine_sim()（用点积和长度）
    3. 验证：同方向 ≈ 1，垂直 ≈ 0
"""

import numpy as np  # numpy 用来做向量运算（点积、长度）

# ── 第 1 步：定义向量 ──────────────────────────────
# 用 np.array 把列表变成「向量」。numpy 的数组支持逐元素运算。
a = np.array([3, 1])   # a = (3, 1)
b = np.array([6, 2])   # b = (6, 2) = 2 × a，所以 b 和 a 方向完全一致
c = np.array([-1, 3])  # c = (-1, 3)，和 a 垂直（见下面验证）


# ── 第 2 步：写 cosine_sim() ───────────────────────
# 余弦相似度公式：cos_sim = (v · w) / (|v| × |w|)
#   分子 v·w  = 点积（逐元素相乘再求和）
#   分母 |v|  = 向量的长度（欧氏范数）
def cosine_sim(v, w):
    # np.dot(v, w)  —— 点积：v[0]*w[0] + v[1]*w[1]
    dot = np.dot(v, w)

    # np.linalg.norm(v) —— 向量长度：sqrt(v[0]² + v[1]²)
    #   linalg = linear algebra（线性代数）模块
    #   norm   = 范数，默认是 2 范数，即欧氏长度
    norm_v = np.linalg.norm(v)
    norm_w = np.linalg.norm(w)

    # 返回点积除以两个长度的乘积
    # 注意：分母相乘等价于「先各自归一化，再做点积」——结果落在 [-1, +1]
    return dot / (norm_v * norm_w)


# ── 第 3 步：验证三个关系 ─────────────────────────
print("cos(a, b) =", cosine_sim(a, b))   # b 和 a 同方向 → 期望 ≈ 1.0
print("cos(a, c) =", cosine_sim(a, c))   # c 和 a 垂直   → 期望 ≈ 0.0
print("cos(a, a) =", cosine_sim(a, a))   # 自己和自己   → 恒等于 1.0


# ── 额外：为什么 a 和 c 垂直？ ────────────────────
# 点积 a·c = 3*(-1) + 1*3 = -3 + 3 = 0
# 点积为 0 ⇔ 两个向量垂直（cos(90°) = 0）
print("a · c =", np.dot(a, c), "（0 就说明垂直）")
