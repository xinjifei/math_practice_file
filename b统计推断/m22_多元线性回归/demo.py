"""最简示例：sklearn 多元线性回归的接口"""
import numpy as np
from sklearn.linear_model import LinearRegression

# ── 造数据：5 只股票，2 个因子 ──
# X: 5行 × 2列（每行一只股票，每列一个因子）
X = np.array([
    [0.5, -0.3],   # 股票A：大盘+0.5%，规模偏小
    [0.2,  0.1],   # 股票B
    [-0.4, 0.8],   # 股票C
    [0.1, -0.6],   # 股票D
    [-0.2, 0.3],   # 股票E
])

# y: 真实收益（你藏起来的"正确答案"）
y = np.array([0.3, 0.15, -0.25, 0.05, -0.1])

# ── 训练（拟合） ──
model = LinearRegression()
model.fit(X, y)

# ── 输出 ──
print("截距 a :", model.intercept_)
print("系数 b :", model.coef_)          # [b1, b2]，顺序跟 X 的列对应
print("R²    :", model.score(X, y))
print("预测值:", model.predict(X))      # 用刚才那组 X 算出的 Ŷ
