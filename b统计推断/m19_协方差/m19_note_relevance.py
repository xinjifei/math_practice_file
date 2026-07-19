import sys
sys.path.insert(0, 'D:/math_practice_file/数据源获取/script')
from get_data import get_stock_data
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

#获取数据为dataframe
df_PingAn = get_stock_data(
    symbol="sz000001", 
    stock_name="平安银行",
    start_date="20250623",
    end_date="20260623"
    )
df_WuLiang = get_stock_data(
    symbol="sz000858", 
    stock_name="五粮液",
    start_date="20250623",
    end_date="20260623"
    )
df_NingDe = get_stock_data(
    symbol="sz300750", 
    stock_name="宁德时代",
    start_date="20250623",
    end_date="20260623"
    )

#列收益率列表
source_list = []
PingAn_list = df_PingAn["close"].pct_change().dropna().tolist()
source_list.append(PingAn_list)
WuLiang_list = df_WuLiang["close"].pct_change().dropna().tolist()
source_list.append(WuLiang_list)
NingDe_list = df_NingDe["close"].pct_change().dropna().tolist()
source_list.append(NingDe_list)
test = source_list


#开始算协方差
def convariance(source_list:list) -> list:
    ##差离值列表
    def deviation_func(source_list):
        average = sum(source_list) / len(source_list)
        deviation_list = []
        for i in source_list:
            deviation = i - average
            deviation_list.append(deviation)
        return deviation_list
    
    ##计算三个股票之间的积
    """
        A
        B
        C
         ABC
    """
    Ping_dev_list = deviation_func(source_list[0])
    Wu_dev_list = deviation_func(source_list[1])
    Ning_dev_list = deviation_func(source_list[2])

    pw = [Ping_dev_list[i] * Wu_dev_list[i] for i in range(len(Ping_dev_list))]
    pn = [Ping_dev_list[i] * Ning_dev_list[i] for i in range(len(Ping_dev_list))]
    wn = [Wu_dev_list[i] * Ning_dev_list[i] for i in range(len(Wu_dev_list))]

    #平均值
    pw_result = sum(pw) / (len(pw) - 1)
    pn_result = sum(pn) / (len(pn) - 1)
    wn_result = sum(wn) / (len(wn) - 1)

    return pw_result, pn_result, wn_result

#相关系数
## 标准差
def std(a:list) -> float:
    n = len(a)
    mean = sum(a) / n
    variance = sum((x - mean) ** 2 for x in a) / (n - 1)
    return variance ** 0.5

## 相关系数
def correlation(convariance:float, variance_x:float, variance_y:float) ->float:
    cor = convariance / (variance_x * variance_y)
    return cor

#开始计算
## 准备数据
pw_cov, pn_cov, wn_cov = convariance(source_list)
Ping_std = std(source_list[0])
Wu_std = std(source_list[1])
Ning_std = std(source_list[2])

pw_cor = correlation(pw_cov, Ping_std, Wu_std)
pn_cor = correlation(pn_cov, Ping_std, Ning_std)
wn_cor = correlation(wn_cov, Wu_std, Ning_std)

##显示
print("=" * 30)
print(pw_cor)
print(pn_cor)
print(wn_cor)
    

        
# ====== 热力图 + 折线图 ======
labels = ["平安银行", "五粮液", "宁德时代"]

# 1. 相关系数矩阵热力图
corr_matrix = [[1, pw_cor, pn_cor],
               [pw_cor, 1, wn_cor],
               [pn_cor, wn_cor, 1]]

fig1 = go.Figure(data=go.Heatmap(
    z=corr_matrix,
    x=labels,
    y=labels,
    colorscale="RdBu",
    zmin=-1, zmax=1,
    text=[[f"{v:.3f}" for v in row] for row in corr_matrix],
    texttemplate="%{text}",
))
fig1.update_layout(title="三只股票日收益率相关系数", width=500, height=450)
fig1.show()

# 2. 累计收益率折线图
df_returns = pd.DataFrame({
    "平安银行": PingAn_list,
    "五粮液": WuLiang_list,
    "宁德时代": NingDe_list,
})
cum_returns = (1 + df_returns).cumprod()

fig2 = px.line(cum_returns, y=labels, title="累计收益率（1 元起点）")
fig2.update_layout(xaxis_title="交易日", yaxis_title="累计净值", width=700, height=400)
fig2.show()
