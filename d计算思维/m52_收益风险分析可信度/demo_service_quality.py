"""教师示例：用合成的客服处理记录检查一份服务质量结论的口径。"""

# 每行是一个工作日的原始计数：(日期, 完成的工单数, 当天在时限内完成的工单数)。
rows = [
    ("周一", 10, 9),
    ("周二", 100, 80),
    ("周三", 10, 9),
    ("周四", 100, 85),
]

# 用切片按原有时间顺序取前半段与后半段；切片右端不包含在结果内。
early = rows[:2]
late = rows[2:]


# 定义一个接收原始记录的函数，计算整段的按工单加权达标率。
def service_rate(period_rows):
    # sum(iterable) 将各日完成数相加；生成式逐行取第二列。
    total = sum(row[1] for row in period_rows)
    # 同样相加第三列，得到整段按时完成的工单数。
    on_time = sum(row[2] for row in period_rows)
    # 分母必须是整段完成的工单总数，不能先算各日比率再直接平均。
    return on_time / total


# 用相同的函数和口径计算两个时期，避免比较时偷偷更换分母。
early_rate = service_rate(early)
late_rate = service_rate(late)

# 输出单位为百分比；这是对这四天记录的描述，不是未来服务水平保证。
print(f"前两天按工单达标率：{early_rate:.1%}")
print(f"后两天按工单达标率：{late_rate:.1%}")
