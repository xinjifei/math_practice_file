"""
mat与plotly的区别
plotly形式
    1、新建空图表
    2、新建元素
    3、把元素添加至空图表（需要指定）
    4、显示图表
mat形式
    1、一上来直接开始添加元素，往哪里添加，不用管，
    自动新建所有的空图表，以及其所需的初始配置
    2、继续添加配置不用手动指向某一个图表，直接plt添加元素，
    自动引导添加到当前的图表
    3、要换一个图表写，直接plt.figure()，
    后续操作都在新建的这个图表里面进行
    4、显示图表
"""
import matplotlib.pyplot as plt
import numpy as np

#赋值
x = np.linspace(0, 10, 100)

#画图
plt.plot(x,np.sin(x), label="sin(x)")
plt.plot(x,np.cos(x),label="cos(x)")

#标注y=0的线
plt.axhline(y=0, color="gray", linestyle="--")

#生成图例
plt.legend()

#开启网格
plt.grid(True)

#显示
plt.show()