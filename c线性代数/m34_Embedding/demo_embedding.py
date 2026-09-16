# demo_embedding.py
# 演示：怎么把一句话变成"语义坐标"，再用余弦相似度量两句话有多像。
#
# ⚠️ 演示数据用「机器学习 / 深度学习 / 红烧肉」，
#    你练习时换成「新能源汽车 / 动力电池 / 白酒消费」——思路一样，数据不同。

# ---- 1. 加载模型 ----
# SentenceTransformer：一个把"文字"翻译成"向量"的工具。
#   参数 model_name：用哪个预训练模型（不同模型向量维度、质量不同）。
#   第一次运行会联网下载模型，约百 MB。
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# ---- 2. 把句子变成向量 ----
# encode()：输入 = 一个句子列表，输出 = 一个矩阵，每一行是一个句子的向量。
#   一句话被压成一个几百维的数字数组——这个数组就是它的"语义坐标"。
sentences = ["机器学习", "深度学习", "红烧肉"]
vectors = model.encode(sentences)          # shape = (3, 384)

print("每个向量长度:", vectors.shape[1])    # 384 维的语义坐标

# ---- 3. 余弦相似度 = 两个向量夹角的余弦 ----
# 这就是 Day 27 学的点积：方向越一致，夹角越小，余弦越接近 1。
# 公式：cos = 点积 / (两个向量的长度相乘)
import numpy as np

def cos_sim(a, b):
    # np.dot(a, b)：点积（Day 27 的 v·w = v1w1 + v2w2 + ...）
    dot = np.dot(a, b)
    # np.linalg.norm(x)：向量的长度（模），默认算 L2 范数 = sqrt(平方和)
    length = np.linalg.norm(a) * np.linalg.norm(b)
    return dot / length

# ---- 4. 两两比较 ----
print("机器学习 vs 深度学习 :", round(cos_sim(vectors[0], vectors[1]), 3))   # 预期：高
print("机器学习 vs 红烧肉   :", round(cos_sim(vectors[0], vectors[2]), 3))   # 预期：低
