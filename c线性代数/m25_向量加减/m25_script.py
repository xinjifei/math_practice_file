"""
建向量
    四个向量，分别代表男人、女人、国王、皇后。两个维度，代表 皇室程度，男人程度

算向量 queen_hat

画图显示五个向量
"""

import numpy as np
import matplotlib.pyplot as plt

def practice_0():
    # 建向量
    man = np.array([0, 1])
    woman = np.array([0, -1])
    king = np.array([1, 1])
    queen = np.array([0.7, -1])

    # 算向量 queen_hat
    queen_hat = king - man + woman
    print(queen_hat)

    # 画图显示向量
    ## 重构数组
    quivers = [man, woman, king, queen, queen_hat]
    x = np.array([v[0] for v in quivers])
    y = np.array([v[1] for v in quivers])
    x_s = np.array([0 for _ in range(len(quivers))])
    y_s = np.array([0 for _ in range(len(quivers))])

    ## 画图
    plt.quiver(
        x_s, y_s, x, y,
        angles="xy", scale_units="xy", scale=1,
        color=["red","orange","yellow","green","blue",]
    )

    names = ["man", "woman", "king", "queen", "queen_hat"]
    for i in range(len(quivers)):
        plt.text(x[i], y[i], names[i])


    plt.xlim(-3, 3)
    plt.ylim(-3, 3)
    plt.axhline(y=0, color="gray", linestyle="--")
    plt.axvline(x=0, color="gray", linestyle="--")

    plt.xlabel("x=皇室程度")
    plt.ylabel("y=男人程度")
    plt.show()

"""
练习2
prince应该在那个位置
"""
def practice_1():
    # 定义向量
    boy = np.array([-0.5 ,0.3])
    king = np.array([1, 1])
    man = np.array([0, 1])

    # 计算prince
    prince_hat = king - man + boy

    # 画图
    quivers = [king, boy, prince_hat, man]
    x = np.array([v[0] for v in quivers])
    y = np.array([v[1] for v in quivers])
    x_s = np.array([0 for _ in range(len(quivers))])
    y_s = np.array([0 for _ in range(len(quivers))])
    plt.quiver(
            x_s, y_s, x, y,
            angles="xy", scale_units="xy", scale=1,
            color=["red","orange","yellow", "green"]
    )

    plt.xlim(-3, 3)
    plt.ylim(-3, 3)
    plt.axhline(y=0, color="gray", linestyle="--")
    plt.axvline(x=0, color="gray", linestyle="--")

    names = ["king", "boy", "prince_hat", "man"]
    for i in range(len(names)):
        plt.text(x[i], y[i], names[i])

    plt.xlabel("x=皇室程度")
    plt.ylabel("y=男人程度")
    plt.show()

if __name__ == "__main__":
    practice_0()
    practice_1()


