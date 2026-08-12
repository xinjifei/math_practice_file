# 随机性入门
## 概念：
- 确定性 = 输入确定-->确定输出；例如：
```python
x = input_
y = x * 2
#这里的y就等于输出

```
- 随机性 = 输入确定-->输出随机；例如
```python
import random
x = input_
y = x * random.randint(0, 1)
#这里的y就等于输出
```
- 随机不等于没有规律，大量重复后规律会逐渐趋于稳定，这就是概率
