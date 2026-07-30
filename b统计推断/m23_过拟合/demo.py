import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

# ─── 第一步：造数据 ───
np.random.seed(42)
n = 15                              # 15个数据点，故意很少

X = np.linspace(0, 10, n).reshape(-1, 1)   # X：均匀排开的15个点
y_true = np.sin(X.ravel())                  # 真实规律：正弦曲线
y = y_true + np.random.normal(0, 0.3, n)    # Y：正弦 + 噪音

# ─── 第二步：训练（用前10个点）────
X_train, y_train = X[:10], y[:10]           # 前10个点给模型"学"
X_test,  y_test  = X[10:], y[10:]           # 后5个点藏起来当"考题"

# 5次多项式回归 = 本质还是你m22的 y = a + Σ(b_i * x^i)
model = make_pipeline(
    PolynomialFeatures(degree=5),   # 把 x 变成 [1, x, x², x³, x⁴, x⁵]
    LinearRegression()              # 就是 m22 的 SIGMA —— 算6个系数
)
model.fit(X_train, y_train)

# ─── 第三步：打分 ───
r2_train = model.score(X_train, y_train)    # 训练集 R²
r2_test  = model.score(X_test,  y_test)     # 测试集 R²
print(f"训练集 R² = {r2_train:.3f}")         # 预期：接近 1.0
print(f"测试集 R² = {r2_test:.3f}")          # 预期：低很多，甚至负数

# ─── 第四步：画图 ───
x_curve = np.linspace(0, 10, 200)
y_pred  = model.predict(x_curve.reshape(-1,1))

fig = go.Figure()

train_scatter = go.Scatter(
    x = X_train.ravel(), y = y_train, 
    mode="markers", name="train_data(10points)", marker=dict(color="green",size=10)
    )
test_scatter = go.Scatter(
    x = X_test.ravel(), y = y_test,
    mode="markers", name="test_data(5points)", marker=dict(color="blue",size=10)
    )
sinX_scatter = go.Scatter(
    x = x_curve, y = np.sin(x_curve),
    mode="lines", name="sin(x)", line=dict(color="black",dash="dash")
    )
modelX_scatter = go.Scatter(
    x = x_curve, y = y_pred,
    mode="lines", name="model(x)", line=dict(color="red",dash="solid")
    )

fig.add_traces([train_scatter, test_scatter, sinX_scatter, modelX_scatter])

fig.show()