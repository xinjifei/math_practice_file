import numpy as np
from sklearn.decomposition import PCA
from function.plot import plot
# 生成数据
rng = np.random.default_rng(7)
n = 40
x = rng.uniform(-3,3,n)
noise = rng.normal(0, 2, n)
y = 1.5*x + noise
X = np.column_stack([x, y])

x = rng.normal(0, 2, n)
noise = rng.normal(0, 2, n)
y = rng.normal(0, 2, n)
X = np.column_stack([x, y])

# 拟合两个主成分
pca = PCA(n_components=2)
pca.fit(X)
pca_vec = pca.components_

# 打印
print("主成分分析")
print("拟合主成分（2维），单位向量 = ",pca_vec )
print("各维度解释方差比例 = ", pca.explained_variance_ratio_)

# 拟合一个主成分看丢失了多少信息
pca1 = PCA(n_components=1)
pca1.fit(X)
print("降到1维后保留的方差 = ", pca1.explained_variance_ratio_.sum())

# 画图
plot(
    [
        {
            "type":"point",
            "data":X
        },
        {
            "type":"vector",
            "data":[
                {"主成分1":pca_vec[0]*1},
                {"主成分2":pca_vec[1]*1}
                ]
        }
    ],
    title="数据点&主成分单位向量"
)

