# 交叉熵函数
import numpy as np

def cross_entropy(q:np.array, p:np.array) ->float :

    cun = 0
    etr = 0.0
    for q_i, p_i in zip(q, p):
        cun += 1

        etr_i = p_i * np.log2(q_i)
        etr_i = -(etr_i)
        etr += etr_i

        print(f"etr_{cun} = {etr_i}")

    return etr

import numpy as np

# p_list：存放5个样本的真实分布数组
p_list = [
    np.array([1, 0, 0]),   # 样本1，真实token：猫
    np.array([0, 1, 0]),   # 样本2，真实token：狗
    np.array([0, 0, 1]),   # 样本3，真实token：鸟
    np.array([1, 0, 0]),   # 样本4，真实token：猫
    np.array([0, 1, 0])    # 样本5，真实token：狗
]

# q_list：存放5个样本模型预测概率分布数组，无0，总和=1
q_list = [
    np.array([0.1, 0.6, 0.3]),    # 样本1模型输出
    np.array([0.2, 0.6, 0.2]),    # 样本2模型输出
    np.array([0.35, 0.4, 0.25]),  # 样本3模型输出
    np.array([0.8, 0.1, 0.1]),    # 样本4模型输出
    np.array([0.2, 0.5, 0.3])     # 样本5模型输出
]

cun = 0
for q, p in zip(q_list, p_list):
    cun += 1
    print(f"样本{cun}============")
    result = cross_entropy(q, p)
    print(f"样本{cun} cross_entropy = {result}\n")


    
        
