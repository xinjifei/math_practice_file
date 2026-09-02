import numpy as np

# 数据
mtr_a = np.array([
    [1, 0],
    [0, -1]
])

mtr_b = np.array([
    [2, 0],
    [1, 2]
])

v = np.array([3,4])

# 验证结合律适用于矩阵乘法
result_a = (mtr_a @ mtr_b) @ v
result_b = mtr_a @ (mtr_b @ v)

if np.allclose(result_a, result_b):
    print("证明:结合律适用于矩阵乘法")
    print("result_a=",result_a)
    print("result_b=",result_b)
else:
    print("证伪:结合律适用于矩阵乘法")
    print("result_a=",result_a)
    print("result_b=",result_b)

# 验证交换律不适用于矩阵乘法
ab = mtr_a @ mtr_b
ba = mtr_b @ mtr_a

if np.allclose(ab, ba):
    print("证伪:交换律不适用于矩阵乘法")
    print("ab=",ab)
    print("ba",ba)

else:
    print("证明:交换律不适用于矩阵乘法")
    print("ab=",ab)
    print("ba",ba)