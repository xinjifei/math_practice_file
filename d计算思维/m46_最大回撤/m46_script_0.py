# 最大回撤计算示例

def mdd_cal(V_list):
    peak = V_list[0]
    mdd = 0.0
    peak_low = {"peak": peak, "low": peak}
    for v in V_list:
        # 先计算历史的最高峰(滚动峰值)
        peak = max(peak, v)
        # 再计算今天的净值，相比此前达到过的最高点，跌了百分之多少
        drawdown = (v - peak) / peak
        # 更新峰谷值、mdd
        if drawdown < mdd:
            mdd = drawdown
            peak_low = {"peak": peak, "low": v}

    return mdd, peak_low

if __name__ == "__main__":
    V_list = [100,120,110,150,90,130]

    mdd, peak_low = mdd_cal(V_list)
    peak, low = peak_low["peak"], peak_low["low"]
    print(f"\nV_list = {V_list}\nMDD(V_list) = {mdd}\npeak = {peak} | low = {low}")