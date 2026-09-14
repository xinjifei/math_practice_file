# m33_stock_pca.py —— 用 PCA 给 43 只股票"自动分组"（真实应用，不是练习本身）
#
# 一句话：把"每只股票 = 一段 ~240 天的收益曲线"看成高维空间里的一个点，
#          PCA 把 240 维压成 3 维，再在 3 维里聚类，看哪些股票"走势是同类"。
#
# 运行前：
#   1) 确认装好依赖：`uv add akshare scikit-learn pandas matplotlib`（缺哪个补哪个）
#   2) 会联网拉 43 只股票近一年日线，约 1~2 分钟，等它跑完
#   3) 运行：`uv run m33_stock_pca.py`（在 m33_PCA降维 目录下）

import time
import numpy as np
import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from function.plot import plot

# ---------- 0. 股票池：覆盖多个行业，这样"同类聚一起"才看得出 ----------
# 每项 (symbol, 名字)。symbol 格式：交易所前缀 + 6 位代码（sz=深, sh=沪）
STOCKS = [
    ("sh600519", "贵州茅台"), ("sz000858", "五粮液"), ("sz000568", "泸州老窖"), ("sh600809", "山西汾酒"),
    ("sz000001", "平安银行"), ("sh600036", "招商银行"), ("sh601398", "工商银行"), ("sh601288", "农业银行"),
    ("sz300750", "宁德时代"), ("sz002594", "比亚迪"), ("sh601012", "隆基绿能"), ("sz300014", "亿纬锂能"),
    ("sh688981", "中芯国际"), ("sz002371", "北方华创"), ("sh603986", "兆易创新"), ("sz002415", "海康威视"),
    ("sh600276", "恒瑞医药"), ("sz300760", "迈瑞医疗"), ("sz000538", "云南白药"), ("sh603259", "药明康德"),
    ("sh600030", "中信证券"), ("sz300059", "东方财富"), ("sh601688", "华泰证券"),
    ("sz000002", "万科A"), ("sh600048", "保利发展"),
    ("sz000333", "美的集团"), ("sh600690", "海尔智家"), ("sz000651", "格力电器"),
    ("sh601318", "中国平安"), ("sh601601", "中国太保"),
    ("sh600111", "北方稀土"), ("sz002460", "赣锋锂业"), ("sh601899", "紫金矿业"),
    ("sh601088", "中国神华"), ("sh601857", "中国石油"),
    ("sh600893", "航发动力"), ("sz000768", "中航西飞"),
    ("sh600887", "伊利股份"), ("sh603288", "海天味业"),
    ("sz000063", "中兴通讯"), ("sh600941", "中国移动"),
    ("sh600900", "长江电力"), ("sh601985", "中国核电"),
]

START, END = "20250901", "20260914"   # 近一年，约 240 个交易日


# ---------- 1. 拉数据：每只股票返回 (日期, 收盘价) ----------
def _find_col(df, keywords):
    """在 df 里找列名含某个关键词的列，找不到返回 None（容错 akshare 中英文列名差异）。"""
    for c in df.columns:
        if any(k in str(c).lower() for k in keywords):
            return c
    return None


def fetch_close(symbol, name, start, end):
    """拉一只股票的日线，返回 (dates, close) 两个序列。"""
    df = ak.stock_zh_a_daily(symbol=symbol, start_date=start, end_date=end, adjust="")
    date_col = _find_col(df, ("date", "日期"))
    close_col = _find_col(df, ("close", "收盘"))
    if date_col is None or close_col is None:
        df = df.reset_index()          # 某些版本日期放在索引里，重置成列再找一次
        date_col = _find_col(df, ("date", "日期"))
        close_col = _find_col(df, ("close", "收盘"))
    if date_col is None or close_col is None:
        raise KeyError(f"{name} 列名识别失败，现有列：{list(df.columns)}")
    dates = pd.to_datetime(df[date_col])
    close = pd.to_numeric(df[close_col], errors="coerce")
    return dates, close


# ---------- 2. 收集所有收盘价，拼成一张表 ----------
close_series = {}                    # {股票名: Series(index=日期, value=收盘价)}
for symbol, name in STOCKS:
    try:
        dates, close = fetch_close(symbol, name, START, END)
        close_series[name] = pd.Series(close.values, index=dates, name=name)
        print(f"已拉取 {name}")
    except Exception as e:
        print(f"[跳过] {name}：{e}")
    time.sleep(0.3)                  # 稍作停顿，别把数据源打太狠

price = pd.DataFrame(close_series)   # index=日期, columns=股票名；缺的日期自动变 NaN

# ---------- 3. 算日收益率，转成 (股票 × 日期) 矩阵 ----------
# pct_change：每只股票"今天的收盘价 / 昨天的 - 1"，得到日收益率
#   fill_method=None：别用旧的前向填充逻辑（新版已弃用），第一行本来就是 NaN，稍后统一 drop
returns = price.pct_change(fill_method=None)
returns = returns.dropna(how="all")  # 去掉第一行（全是 NaN，因为没有前一天）
returns = returns.T                  # 转置 → 每行一只股票，每列一个交易日

# 停牌太多的股票直接剔除（缺失 > 20%），剩余缺失填 0（停牌日视为收益 0）
valid = returns.notna().sum(axis=1)               # 每只股票的非 NaN 天数
returns = returns[valid >= int(returns.shape[1] * 0.8)]
returns = returns.fillna(0.0)

names = list(returns.index)          # 活下来的股票名（顺序和下面矩阵的行一致）
R = returns.values                    # (n_stocks, n_days) 的数值矩阵
n_stocks, n_days = R.shape
print(f"\n数据矩阵：{n_stocks} 只股票 × {n_days} 个交易日")


# ---------- 4. 标准化：让每只股票"贡献相同大小的方差" ----------
# 不标准化会怎样？波动大的股票（如中芯国际）方差大，会主导主成分方向，
# 把"波动大"错当成"信息多"。标准化后比较的是"涨跌的相关结构"，不是幅度。
R_std = (R - R.mean(axis=1, keepdims=True)) / R.std(axis=1, keepdims=True)


# ---------- 5. PCA：把 n_days 维压成 3 维 ----------
# 每个"维度"是一个交易日；PCA 在"股票分布得最开的方向"上找主成分。
# 第一主成分 ≈ 所有股票一起涨跌的方向（大盘），所以解释方差通常最高。
pca = PCA(n_components=3)
scores = pca.fit_transform(R_std)    # (n_stocks, 3)：每只股票在 3 个主成分上的坐标

print("每个主成分解释的方差比例:", np.round(pca.explained_variance_ratio_, 4))
print("前 3 个主成分累计解释:", round(pca.explained_variance_ratio_.sum(), 4))
print("（这就是你说的『前 3 个解释 85%』，看它实际是多少）")


# ---------- 6. 聚类：在 3 维主成分空间里把股票分组 ----------
# KMeans：把 n_stocks 个点分成 k 簇，每个点归到离它最近的中心。
#   n_clusters=5  分几类（可调）
#   random_state  固定随机种子，结果可复现
#   n_init=10     多跑几次取最优，避免初始点选的不好
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
labels = kmeans.fit_predict(scores)  # 每只股票的簇标签 (0~4)

print("\n聚类结果（同类里走势相近的股票）：")
groups = {}
for name, lab in zip(names, labels):
    groups.setdefault(lab, []).append(name)
for lab in sorted(groups):
    print(f"  簇 {lab}：{'、'.join(groups[lab])}")


# ---------- 7. 画图 ----------
# 图 1：方差解释比例（柱状 + 累计线）—— 用 matplotlib，因为 plot() 没有 bar 类型
ratio = pca.explained_variance_ratio_
cum = np.cumsum(ratio)
x = np.arange(1, 4)
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(x, ratio, color="tab:blue", alpha=0.7, label="单个主成分")
ax.plot(x, cum, marker="o", color="tab:red", label="累计解释比例")
for i in range(3):
    ax.text(x[i], ratio[i] + 0.01, f"{ratio[i]:.1%}", ha="center")
    ax.text(x[i], cum[i] + 0.02, f"{cum[i]:.1%}", ha="center", color="tab:red")
ax.set_xticks(x)
ax.set_xticklabels(["主成分1", "主成分2", "主成分3"])
ax.set_ylim(0, 1.05)
ax.set_ylabel("解释方差比例")
ax.set_title("前 3 个主成分解释了绝大部分方差")
ax.legend()
plt.tight_layout()
plt.show()

# 图 2：股票在前两个主成分上的投影，颜色=聚类（用统一的 plot()，point 层）
#   "data" 用 scores 的前两列（每只股票一个 (x, y) 点）
#   "c"    是每只股票的簇标签，透传给 scatter 让它按簇上色
plot([
    {"type": "point", "data": scores[:, :2], "c": labels, "s": 60, "cmap": "tab10"},
], title="43 只股票在前两个主成分上的投影（颜色 = 聚类）")
