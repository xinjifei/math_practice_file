from function.plot_vectors import plot_vectors
import numpy as np

def calc(v, M, title):
    v = np.array(v)

    M = np.array(M)

    w = M @ v

    print("v=", v)
    print("w=", w)
    print("M=", M)

    plot_vectors(
        [
            {"v": list(v)},
            {"w": list(w)}
        ],
        title=title,
    )
#######################################
calc(
    [3, 2],
    [
        [0,1],
        [1,-3]
    ],
    ""
)

# 猜 [[0,1],[1,0]] 对 [3,2] 做了什么：什么都没做
calc(
    [3, 2],
    [
        [0,1],
        [1,0]
    ],
    ""
)
# 正确答案：w维度值互换了

# 把向量沿 x 轴方向压缩到一半（y 坐标不变）

calc(
    [3, 2],
    [
        [0.5,0],
        [0,1]
    ],
    "x轴压缩一半"
)

# 扁平矩阵
calc(
    [3, 2],
    [
        [0,0],
        [0,1]
    ],
    "扁平x轴"
)

