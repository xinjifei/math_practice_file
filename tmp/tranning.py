import numpy as np
from function.plot_3d import plot_3d
from sklearn.decomposition import PCA
rng = np.random.default_rng(1)
n = 30

# group1
x = rng.normal(0, 2, n) + 9
y = rng.normal(0, 2, n) + 9
z = rng.normal(0, 3, n)
data_0 = np.column_stack([x,y,z])

# group1
x = rng.normal(0, 2, n) + 9
y = rng.normal(0, 2, n) - 9
z = rng.normal(0, 3, n)
data_1 = np.column_stack([x,y,z])

# group1
x = rng.normal(0, 2, n)
y = rng.normal(0, 2, n)
z = rng.normal(0, 3, n)
data_2 = np.column_stack([x,y,z])

"""plot_3d([
    {"type":"point", "data":data_0},
    {"type":"point", "data":data_1},
    {"type":"point", "data":data_2},
])"""

n = 40

x = rng.uniform(-10, 10, n)
noise = rng.normal(-2, 1, 2)

data = np.column_stack([x])


plot_3d([
    {"type":"point", "data":data},
    
])


