"""
二维向量
"""
import matplotlib.pyplot as plt

# 一个向量
## 添加向量
plt.quiver(0,0,3,3,angles="xy",scale_units="xy",scale=1,color="green")
"""
0,0,3,3 前两个是向量的起始位置，后两个是结束位置，后者为头，前者为尾
angles,scale_units,scale 缩放设置
color 颜色
"""
## 添加坐标参考轴
plt.axhline(y=0,color="gray",linestyle="--")
plt.axvline(x=0,color="gray",linestyle="--")

## 显示网格
plt.grid(True)

## 设置显示窗口大小
plt.xlim(-10,10)
plt.ylim(-10,10)

## 显示
plt.show()

# 多个向量
plt.quiver(
    [0,0,0],[0,0,0],[0,2,4],[4,2,0],
    angles="xy",scale_units="xy",scale=1,
    color=["red", "green", "purple"]
           )

plt.xlim(-5,5)
plt.ylim(-5,5)
plt.axhline(y=0,color="gray",linestyle="--")
plt.axvline(x=0,color="gray",linestyle="--")
plt.grid(True)

plt.show()