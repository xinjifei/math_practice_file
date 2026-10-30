# 用 A（年化 30%、σ=25%）和 B（年化 18%、σ=10%），rf = 2%，算两者 Sharpe

def sharpe(R:float, sigma:float, r_f:float=0.02)->float:
    result = (R - r_f) / sigma
    return result

sharpe_1 = sharpe(0.3,0.25)
sharpe_2 = sharpe(0.18,0.10)
print(f"sharpe_1 = {sharpe_1}, sharpe_2 = {sharpe_2}")