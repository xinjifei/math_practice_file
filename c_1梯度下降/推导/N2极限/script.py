"""
f(x) = x³`，起点 `x₀ = 2`。列一张表，`Δx` 依次取
 `1`、`0.5`、`0.1`、`0.01`、`0.001`，
每一行算出 `Δy / Δx`。这五个数在往哪走？
"""

def f(x_0,delta_x):
  #  result = 12 + (6*delta_x) + (delta_x) ** 2
    result = ((x_0+delta_x)**3 - (x_0)**3)/(delta_x)
    print(delta_x,"-----",result)

print("Δx-----(x)^3")
del_list = [1,0.5,0.1,0.01,0.001]

for delta_x in del_list:
    f(1,delta_x)

print("Δx-----(x)^3")
for delta_x in del_list:
    f(2,delta_x)

del_list = [0]
print("Δx-----(x)^3")
for delta_x in del_list:
    f(2,delta_x)