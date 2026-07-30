import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

# 造数据
np.random.seed(5)
n = 15
## x
x = np.linspace(0,10,n).reshape(-1,1)
## y
y_ = np.sin(x.ravel())
y = y_ + np.random.normal(0,0.3,n)

#训练
## 截数据
x_train, y_train = x[:10], y[:10]
x_test,  y_test  = x[10:], y[10:]
model = make_pipeline(
    PolynomialFeatures(degree=5),
    LinearRegression()
)
model.fit(x_train, y_train)

#打分+打印分数（r ** 2）
r2_train = model.score(x_train, y_train)
r2_test  = model.score(x_test, y_test)
print(f"训练R² = {r2_train:.4f}")
print(f"测试R² = {r2_test:.4f}")  

#画图
## 创建函数对比专用数据
x_curve = np.linspace(0, 10, 200)
y_pred  = model.predict(x_curve.reshape(-1,1))

## 创建空图表
fig = go.Figure()

## 创建图表元素
### 数据集（点状）
#### 训练数据
train_markers = go.Scatter(
    x = x_train.ravel(), y = y_train,
    mode="markers", name = "train_data", marker=dict(color="green", size=15) 
)
test_markers = go.Scatter(
    x = x_test, y = y_test,
    mode="markers", name="test_data", marker=dict(color="blue", size=15)
)
#### 拟合对比
sinX = go.Scatter(
    x = x_curve, y = np.sin(x_curve),
    mode="lines", name="sin(x)", line=dict(color="black", dash="dash")
)
modelX = go.Scatter(
    x = x_curve, y = y_pred,
    mode="lines", name="model(x)", line=dict(color="red", dash="solid")
)

## 填进图表
fig.add_traces([train_markers, test_markers, sinX, modelX])

## 显示图表
fig.show()