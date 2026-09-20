import numpy as np
from function.plot import plot


def loss(x):
    return (x + 2) ** 2

def grad(x):
    return 2 * (x + 2)

def gradient_descent_step(lr, x, steps):
    curve = []       # 记录每一步的 [迭代次数, 损失]，等一下画图要用
    for i in range(steps):
        # range(steps) 依次给出 0,1,2,3,4,5，i 只用来计数

        # 先记录"这一步开始时的状态"：站在哪、损失多少
        curve.append([i, loss(x)])
        print(f"第 {i} 步：x = {x:.5f}   loss = {loss(x):.5f}")

        # ↓↓↓ 整个梯度下降，就这一行 ↓↓↓
        x = x - lr * grad(x)
        # 为什么是"减"？因为 grad(x) 指向损失变大的方向，我们要损失变小 → 朝反方向走。
        # lr 的作用是"步长"：grad 只告诉你朝哪走，lr 说你这一步迈多远。

    # 循环结束后，记录最终落点
    curve.append([steps, loss(x)])
    print(f"第 {steps} 步：x = {x:.5f}   loss = {loss(x):.5f}")

    curve = np.array(curve)

    plot(
        [{"type": "point",
        "data": curve,
        "color": "tab:red",
        "s": 30}],
        title=f"梯度下降：loss 随迭代次数下降,lr={lr}",
    )

gradient_descent_step(1.2, 5.0, 6)
gradient_descent_step(0.1, 5.0, 6)
gradient_descent_step(0.01, 5.0, 6)
