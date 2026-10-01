"""
F = (x^2 + y^2)
nabla F = [
            [2x],
            [2y]
            ]
"""
import numpy as np

# 设置初始点
xy_0 = np.array([20,30])
# 求梯度函数

step = 100
lr = 0.1
xy_0 = np.array([20,30])

# 调试
def db(name_list):
    for name in name_list:
        i = globals()[name]
        print(f"{name} = {i} | type = {type(i)}")

# 对象函数
def F(xy:np.array):
    result = xy[0]**2 + xy[1]**2
    return result

# 单次下降
def gradient_descent(xy_0:np.array, lr:float):
    # 梯度函数
    def grad(xy:np.array):
        d_d = np.array([2,2])
        result = xy * d_d
        return result

    # 算值
    grad_ = grad(xy_0)
    xy = xy_0 - lr * grad_
    loss = F(xy)
    return xy, loss, grad_

def show(step, grad, new_xy, loss,):
    print(f"=====step = {step}")
    print(f"grad = {grad}")
    print(f"new xy = {new_xy}")
    print(f"loss = {loss}")

new_xy = None
# 循环下降
print(f"======gradient_descent======\nlearning rate = {lr}\nsteps = {step + 1}\n")

for i in range(step):
    # 下降
    if new_xy is None:
        new_xy, loss, grad = gradient_descent(xy_0, lr)
        show(i, grad, new_xy, loss)

    step = i + 1
    new_xy, loss, grad = gradient_descent(new_xy, lr)
    show(step, grad, new_xy, loss)