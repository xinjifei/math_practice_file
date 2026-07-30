import numpy as np
np.random.seed(42)
n = 20
x = np.linspace(0, 10, n)                    # 0~10 均匀取 20 个点
y = 2 * x + 1 + np.random.normal(0, 3, n)

# 展示plotly生成图表的全流程
# 1、导入库
import plotly.graph_objects as go
# 2、创建空图表
fig = go.Figure()
#3、创建图表元素
## 散点类型用于演示
points = go.Scatter(
    x = x, y = y, mode="markers", name="x", marker=dict(color="red", size=15)
)
"""
参数分别为
x = x轴参数(array)
y = y轴参数(array)
mode = 图案类型 markers是点 lines是线(str)
name = 图案的名字 会在网页中标注(str)
marker/line = 图案的配置 具体叫什么取决于图案的类型 需要转为字典 配置中包括(ditc)
    color = 颜色(str)
    size/dash = 图案的形态 size用在点类型 dash用在线类型 分别有
        点类型
            size = 大小 10 常用(int) 
        线类型
            dash = 线的类型 常用实心线 "solid"  虚线 "dash"(str) 
"""
#4、添加图表元素到新建的空图表
fig.add_traces([points])
"""
使用traces()+传入元素名列表可以一次性添加到元素里
"""
#5、显示网页
fig.show()