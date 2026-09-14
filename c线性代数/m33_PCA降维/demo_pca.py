# demo_pca.py —— PCA 降维的核心直觉（演示用，不是练习本身）
# 目标：看明白三件事
#   1) PCA 找到的"方差最大的方向"是什么
#   2) explained_variance_ratio_ 每个数字代表什么、加起来等于几
#   3) 降到低维后"丢了多少信息"怎么读
#
# 运行前：如果 sklearn 没装，先 `uv add scikit-learn`

import numpy as np
from sklearn.decomposition import PCA
from function.plot import plot

# ---- 造一组"几乎落在一条斜线上"的二维数据 ----
# 真实数据里很多特征高度相关（身高/体重、开盘价/收盘价），
# 这种"相关"意味着：数据其实基本躺在一个低维方向上，PCA 就是要抓这个方向。
rng = np.random.default_rng(7)   # 固定随机种子，让每次结果一样（可复现）
n = 200                          # 200 个样本点
x = rng.uniform(-3, 3, n)        # x 坐标：在 -3 到 3 之间均匀随机取值
noise = rng.normal(0, 0.4, n)    # 噪声：让点不严格在线上，模拟真实数据的抖动
y = 1.5 * x + noise              # y ≈ 1.5x：数据主要沿"斜率 1.5"的方向延伸
X = np.column_stack([x, y])      # 把两列拼成 (200, 2) 矩阵：每行是一个样本点

# ---- 拟合 PCA（先保留全部 2 维，好观察每个主成分占多少方差）----
# PCA(n_components=2)：n_components 参数 = 要保留的主成分个数，这里先留满 2 维。
pca = PCA(n_components=2)
pca.fit(X)                       # fit：让 PCA 从数据里"找方向"，不改变数据本身

print("每个主成分解释的方差比例 explained_variance_ratio_:")
print(pca.explained_variance_ratio_)
# explained_variance_ratio_ 是一个数组，第 i 个元素 = 第 i 个主成分"解释了多大比例的方差"。
# 所有元素加起来 = 1（100% 的方差被全部主成分瓜分）。
print("加起来 =", pca.explained_variance_ratio_.sum())
print()
print("主成分方向 components_（每行是一个主成分的单位向量）:")
print(pca.components_)
print()

# ---- 降到 1 维，看丢了多少信息 ----
# 不用重新 fit：保留 1 维时，"保留的方差比例"就是第一个主成分的比例，
# 因为不管保留几个主成分，第一主成分都是同一个。
print("降到 1 维后，保留的方差比例 =", pca.explained_variance_ratio_[0])
print("也就是丢了", round(1 - pca.explained_variance_ratio_[0], 4), "的信息")

# 要拿到降维后的坐标：用 transform 把数据投射到主成分上（不用再 fit 一次）。
X_1d = pca.transform(X)[:, :1]   # transform 得到 (200,2)，[:, :1] 取第一主成分那一列，保持 (200,1)
print("降维后的数据形状:", X_1d.shape, "（从 (200,2) 变成 (200,1)）")
print()

# ---- 画图：看原始点和第一主成分方向（用统一的 plot()，不写裸 matplotlib）----
v = pca.components_[0]           # 第一主成分的单位向量（长度=1 的方向）
# plot(layers, title) 接受一个图层列表：point 层画散点、vector 层画带名字的向量，可叠加。
#   point  层：data 是 (n,2) 矩阵，每行一个 [x, y]；s / alpha 会透传给 scatter
#   vector 层：data 是 [{"名字": 坐标}]，坐标给 2 个数表示终点（默认起点 (0,0)）
plot([
    {"type": "point", "data": X, "s": 10, "alpha": 0.5},                  # 原始 200 个点
    {"type": "vector", "data": [{"第一主成分": [v[0] * 4, v[1] * 4]}]},    # 方向向量，放大 4 倍便于看清
], title="数据主要沿一个方向延伸 → 第一主成分抓住了绝大部分方差")
