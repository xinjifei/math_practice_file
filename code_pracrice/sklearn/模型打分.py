# 用skLearn里面的函数自动打分（方差）
from sklearn.linear_model import LinearRegression
import numpy as np

# 造数据：y = 2x + 1，加一点点噪音
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([3, 5, 7, 9, 11])

#重点=====
model = LinearRegression()
model.fit(X, y)                      # 训练
score = model.score(X, y) 
"""
model里面内涵算出来的结果，(X, y)则是答案。就相当于有了作业和标准答案，可以开始打分了
"""
print(score)             