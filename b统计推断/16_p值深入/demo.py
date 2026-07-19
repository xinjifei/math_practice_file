"""Day 16：p 值直方图 —— 没用策略的 p 值服从均匀分布"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy.stats import ttest_1samp

# ====== 中文字体 ======
for font_name in ["Microsoft YaHei", "SimHei", "KaiTi"]:
    if font_name in {f.name for f in fm.fontManager.ttflist}:
        plt.rcParams["font.sans-serif"] = [font_name, "DejaVu Sans"]
        break
plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 模拟 100 个完全没用的策略，看 p 值的分布
# ============================================================
np.random.seed(42)
n_strategies = 100
p_values = []

for _ in range(n_strategies):
    trades = np.random.normal(0, 1, 50)       # 每笔期望 = 0，完全没用
    _, p = ttest_1samp(trades, popmean=0)      # 检验
    p_values.append(p)

# ============================================================
# 画直方图
# ============================================================
plt.hist(p_values, bins=20, edgecolor='white', color='steelblue')
plt.axvline(0.05, color='red', linestyle='--', linewidth=2, label='0.05 阈值')
plt.xlabel('p 值')
plt.ylabel('频次')
plt.title(f'{n_strategies} 个完全没用的策略，它们的 p 值分布')
plt.legend()
plt.tight_layout()
plt.show()

# ============================================================
# 关键观察
# ============================================================
print(f"p<0.05 的有 {sum(1 for p in p_values if p < 0.05)} 个")
print(f"p<0.10 的有 {sum(1 for p in p_values if p < 0.10)} 个")
print(f"p 值范围: [{min(p_values):.4f}, {max(p_values):.4f}]")
print()
print("如果 p 值在 0~1 之间大致均匀分布——")
print("那 0~0.05 区间自然就有约 5% 的 p 值落在里面。")
print("跟策略有没有用，一毛钱关系都没有。")
