""" Σ(x * P(x))"""

value_list = [-1, 1] #这里的两个数字分别代表输和赢所代表金额


result_list = []
print(value_list)
for x in value_list:
    if x == -1:
        sigma = x * 0.4
    
    if x == 1:
        sigma = x * 0.6

    result_list.append(sigma)
print(result_list)

final = 0
for result in result_list:
    final += result

print(final)


    

