# 国王和皇后在二维向量中的体现
import numpy as np
import matplotlib.pyplot as plt

# x = 男性化程度
# y = 高低位程度
king = np.array([1, 1])
queen = np.array([-1, 1])
man = np.array([1, 0])
woman = np.array([-1,0])
power = np.array([0, 1])
powerles = np.array([0, -1])

vectors = [king, queen, man, woman, power, powerles]
x = np.array([v[0] for v in vectors])
y = np.array([v[1] for v in vectors])
x_s = np.array([0, 0, 0, 0, 0, 0])
y_s = np.array([0, 0, 0, 0, 0, 0])

plt.quiver(x_s, y_s ,x, y, angles="xy", scale_units="xy",scale=1,
        color=["red", "orange", "yellow", "green", "blue", "purple"]
         )

plt.axhline(y=0, color="gray")
plt.axvline(x=0, color="gray")

plt.grid(True)

plt.ylim(-2, 2)
plt.xlim(-2, 2)

plt.show()