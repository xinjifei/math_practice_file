import matplotlib.pyplot as plt
import math

def f_1(range_start, range_end):
    y_values = [2*x+1 for x in \
                range(range_start, range_end)
                ]
    return y_values

def f_2(range_start, range_end):
    y_values = [-(x*x) for x in \
                range(range_start, range_end)
                ]
    return y_values

def f_3(range_start, range_end):
    y_values = [math.sin(x) for x in \
                range(range_start, range_end)
                ]
    return y_values

def f_4(range_start, range_end):
    y_values = [math.cos(x) for x in \
                range(range_start, range_end)
                ]
    return y_values
    
def draw_line(x_values, y_values, title="折线图"):
    """画折线图"""
    plt.plot(x_values, y_values, marker='o')
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    x_config = [-20, 21]
    x_values = list(range(*x_config))
    
    y_values = f_1(x_config[0], x_config[1])

    print("x:", x_values)
    print("y:", y_values)
    print("type:", type(y_values))

    draw_line(x_values, y_values, "f(x) = 2x + 1")

    y_values = f_2(x_config[0], x_config[1])
    draw_line(x_values, y_values, "f(x) = x*x")

    y_values = f_3(x_config[0], x_config[1])
    draw_line(x_values, y_values, "f(x) = sin(x)")

    y_values = f_4(x_config[0], x_config[1])
    draw_line(x_values, y_values, "f(x) = cos(x)")

