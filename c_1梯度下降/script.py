"""
F = 1 - e^-(x^2 + y^2)
nabla F = [
            [2x * e^-(x^2+y^2)],
            [2y * e^-(x^2+y^2)]
            ]
"""
import numpy as np

# 设置初始点
xy_0 = np.array([1.2, 1.2])

func = "F = 1 - e^-(x^2 + y^2)"
step = 7
lr = 0.8


# 调试
def db(name_list):
    for name in name_list:
        i = globals()[name]
        print(f"{name} = {i} | type = {type(i)}")

# 对象函数
def F(xy:np.array):
    result = 1 - np.exp(-(xy[0]**2 + xy[1]**2))
    return result

# 单次下降
def gradient_descent(xy_0:np.array, lr:float):
    # 梯度函数
    def grad(xy:np.array):
        x, y = xy
        e = np.exp(-(x**2 + y**2))
        return np.array([2*x*e, 2*y*e])

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
print(f"======gradient_descent======")
print(f"funcion = {func}")
print(f"xy_0 = {xy_0}")
print(f"learning rate = {lr}")
print(f"steps = {step + 1}\n")

for i in range(step):
    # 下降
    if new_xy is None:
        new_xy, loss, grad = gradient_descent(xy_0, lr)
        show(i, grad, new_xy, loss)

    step = i + 1
    new_xy, loss, grad = gradient_descent(new_xy, lr)
    show(step, grad, new_xy, loss)


# ============================================================
# 下降过程可视化（附加段，上面一行都不动）
# ------------------------------------------------------------
# 叠成一张图：先画候选3「真坑」曲面（照 tmp.py 的 plot_surface_3d 用法），
# 再把每一步当成一根向量叠到同一张画布上（给 plot_3d / plot_vectors_3d 传 fig=）。
# 对象函数直接复用上面的 F；起点、学习率、步数也全读上面的变量 —— 改上面这里就跟着变。
# ============================================================
from function.plot_3d import plot_vectors_3d, plot_surface_3d


# ---- 被下降的对象函数：直接用上面的 F（= tmp.py 候选 3「真坑」）----
# F 收的是向量 xy，plot_surface_3d 要的是 f(x, y)，这里只包一层转格式；F 一改自动跟着变。
def obj(x, y):
    return F(np.array([x, y]))


# ---- 1) 重跑一遍"标准一步一降"，收下每一步的位置 ----
path = [np.array(xy_0, dtype=float)]
for _ in range(int(step)):
    next_xy, _, _ = gradient_descent(path[-1], lr)
    path.append(next_xy)
path = np.array(path, dtype=float)
path_z = np.array([obj(p[0], p[1]) for p in path])


# ---- 2) 窗口：把"坑(0,0)"和"整条路径"一起框进来，不写死 ----
pts = np.vstack([path[:, :2], np.zeros((1, 2))])        # 路径所有点 + 碗底原点
lo, hi = pts.min(axis=0), pts.max(axis=0)
center = float(((lo + hi) / 2).mean())                  # x、y 共用同一窗口，取一个中心
radius = float((hi - lo).max()) / 2 * 1.25 or 1.0        # 半宽，再留 25% 边

grid = np.linspace(center - radius, center + radius, 60)
Xg, Yg = np.meshgrid(grid, grid)
Zg = obj(Xg, Yg)
z_bottom = float(np.nanmin(Zg))
z_height = float(np.nanmax(Zg) - z_bottom) * 1.05
z_lift = 0.02 * z_height                                 # 路径抬离曲面一点，免得被曲面盖住

# ---- 3) 一张图：曲面 + 每一步的向量 ----
fig = plot_surface_3d(
    obj,
    x_range=(center, radius),
    z_range=(z_bottom, z_height),
    n=140,
    title=f"下降过程 · 起点 {tuple(xy_0)} · lr={lr} · {int(step)} 步",
    show=False,
)

# 每一步一根向量：6 个数 = [起点 xyz, 终点 xyz]（z 抬高一点）
descent_vectors = [
    {f"{k}→{k + 1}": [path[k, 0], path[k, 1], path_z[k] + z_lift,
                      path[k + 1, 0], path[k + 1, 1], path_z[k + 1] + z_lift]}
    for k in range(len(path) - 1)
]
plot_vectors_3d(descent_vectors, fig=fig, s=6, show=True)   # s = 箭头尖端小球大小
