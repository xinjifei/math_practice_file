"""
通过代码证明 余弦值 同向≈1、v3垂直≈0、反向≈-1
"""
import numpy as np
from function.plot_vectors import plot_vectors

#造数据
v_0 = np.array([0, 3])
v_1_1 = np.array([0, 6])
v_2_0 = np.array([3, 0])
v_3_neg1 = np.array([0, -3])

# 计算验证

def cosine_sim(v:np.array, w:np.array) -> float:

    print("="*10)
    print(f"vector value:\n   v = {v}\n   w = {w}")

    # 点积
    dot = np.dot(v, w)
    print(f"dot = {dot}")

    # 向量模长
    v_len = np.linalg.norm(v)
    w_len = np.linalg.norm(w)
    print(f"v_len = {v_len}, w_len = {w_len}")

    # 余弦值
    cos_theta = dot / (v_len*w_len)
    print(f"cos_theta = {cos_theta}")

    print("="*10)
    return cos_theta


cosine_sim(v_0, v_1_1)
cosine_sim(v_0, v_2_0)
cosine_sim(v_0, v_3_neg1)

plot_vectors(
    [
        {"v_0":list(v_0)},
        {"v_1_1":list(v_1_1)},
        {"v_2_0":list(v_2_0)},
        {"v_3_neg1":list(v_3_neg1)}
    ],
    title="余弦值可视化"
)

