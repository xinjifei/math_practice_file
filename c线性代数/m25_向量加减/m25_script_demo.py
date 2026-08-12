import matplotlib.pyplot as plt
import numpy as np

# 新建向量
king = np.array([0, 0, 1, 1])
man =  np.array([1, 1, 0, -1])
woman = np.array([1, 0, -0.2, -1])
queen = np.array([0, 0, 0.9, -1])

def dr_quiver(quiver:np.array, color:str, name:str): # quiver = np.array([x_s, y_s, x, y])

    x_s = quiver[0]
    y_s = quiver[1]
    x = quiver[2]
    y = quiver[3]

    text_x = quiver[0] + quiver[2]
    text_y = quiver[1] + quiver[3]

    plt.text(text_x, text_y, name)

    plt.quiver(
        x_s, y_s, x, y,
    angles="xy", scale_units="xy", scale=1,
    color=color
    )

    print(f"向量{name},加载成功")

def plt_config(x_label:str, y_label:str):
    plt.axhline(y=0,color="gray",linestyle="--")
    plt.axvline(x=0,color="gray",linestyle="--")

    ## 显示网格
    plt.grid(True)

    ## 设置显示窗口大小
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)

    ## 维度标注
    plt.xlabel(x_label)
    plt.ylabel(y_label)

dr_quiver(king, "red", "king")
dr_quiver(man, "orange", "- man")
dr_quiver(woman, "yellow", "+ woman")
dr_quiver(queen, "green", "queen")
plt_config(x_label="x=皇室程度", y_label="y=男人程度")

plt.show()
