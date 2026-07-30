import numpy as np

# 随机数种子，用于生成随机数==
x = 5 #种子号
np.random.seed(x)

# 均匀排列；比如要均匀排列5个值到10==
result = np.linspace(0,10,5)#被分割数据的起始,被分割数据的结尾,排列个数

#正太随机数
result = np.random.normal(0, 0.3, 5)   # 均值0，标准差0.3，生成5个
print(result)