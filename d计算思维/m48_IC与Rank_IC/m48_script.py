# note里面讲过的例子

import numpy as np

def information_coefficent(f:list, r:list) -> float:
    f = np.array(f)
    r = np.array(r)
    # 之前学过相关系数所以这个计算部分不手写一遍了
    corr_mat = np.corrcoef(f, r)
    ic = corr_mat[0, 1]   # 取出f和r的相关系数
    print(f"========\nf = {f}\nr = {r}\ninformation coefficent = {ic:.4f}")


# 看三种情况

f_a = [8.2, 7.1, 6.5, 5.3, 4.8, 3.9, 3.2, 2.7, 1.5, 0.8]
r_a = [0.061, 0.048, 0.052, 0.030, 0.025, 0.011, 0.008, -0.005, -0.022, -0.031]

f_b = [8.2, 7.1, 6.5, 5.3, 4.8, 3.9, 3.2, 2.7, 1.5, 0.8]
r_b = [0.035, 0.012, 0.028, -0.005, 0.021, 0.009, -0.014, 0.006, -0.018, 0.002]

f_c = [8.2, 7.1, 6.5, 5.3, 4.8, 3.9, 3.2, 2.7, 1.5, 0.8]
r_c = [-0.012, 0.025, -0.008, 0.019, -0.022, 0.007, 0.014, -0.003, 0.020, -0.016]

information_coefficent(f_a,r_a)
information_coefficent(f_b,r_b)
information_coefficent(f_c,r_c)

    

    
    