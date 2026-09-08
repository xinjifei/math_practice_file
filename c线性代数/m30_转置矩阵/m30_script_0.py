"""
创建 Q(2x3)、K(2x3)，算 Q@K.T
验证
"""
import numpy as np

x = np.array(
    [
# 两个行对应两个token，单个token维度为3（列数=3）
        [1, 2, 3],
        [4, 5 ,6]
    ]
)
# 这里假设两者值相同（真实attention场景中并不会这样）
Q = x
K = x

# 计算Q×Kᵀ
result = Q @ K.T
print("result=",result)

#验证result中的单个值等于i行和j列的点积
# 取一行一列的点积
dot = Q[0] @ K[0]

if dot == result[0][0]:
    print("证明")
else:
    print("证伪")





