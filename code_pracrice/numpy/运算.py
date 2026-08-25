import numpy as np

x = np.array([1, 2])
y = np.array([3, 4])

基础相乘 = x * y
#print (基础相乘,type(基础相乘))
#output: [3 8] <class 'numpy.ndarray'>

点积 = np.dot(x, y)
#print(点积, type(点积))
#output: 11 <class 'numpy.int64'>

向量模长 = np.linalg.norm(x)
#print(向量模长, type(向量模长))
#output: 2.23606797749979 <class 'numpy.float64'>
