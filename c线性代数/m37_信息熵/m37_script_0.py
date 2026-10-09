import numpy as np

# 信息熵计算函数
def entropy(p_list:list) -> float:
    result = 0
    for i in p_list:
        # 如果概率为零直接跳
        if i > 0:
            x = i * np.log2(i)
            result += x

    return -(result)

_list = [
    [0.5,0.5],
    [0.7,0.3],
    [0.9,0.1],
    [1,0]
]

cun = 0
for i in _list:
    cun += 1
    ent = entropy(i)
    print(f"情况{cun}   entropy = {ent}")