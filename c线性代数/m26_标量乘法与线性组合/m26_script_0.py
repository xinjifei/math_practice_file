from function.plot import plot_vectors

# 相关
figure_0 = [
    {"v_0":[3,6]},
    {"v_1":[-1.5,-3]},
]

# 无关
figure_1 = [
    {"v_0":[3,6]},
    {"v_1":[-2,3]},
]

plot_vectors(figure_0, "线性相关")
plot_vectors(figure_1, "线性无关")