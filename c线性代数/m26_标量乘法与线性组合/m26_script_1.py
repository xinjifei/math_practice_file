from function.plot_vectors import plot_vectors

plot_vectors(
    [
        {"v_1":[2,3]},
        {"v_2":[-3,4]},
        {"c_1*v_1":[-3, -4.5]},
        {"c_2*v_2":[3, -4]},
        {"c_1*v_1+c_2*v_2":[0, -8.5]},
    ],
    "线性组合示例"
)