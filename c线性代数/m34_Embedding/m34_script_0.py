import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

from function.plot_3d import plot_3d

model_id = "paraphrase-multilingual-MiniLM-L12-v2"
model = SentenceTransformer(model_id)

text = company_desc = [
    "新能源电车",
    "动力电池",
    "白酒消费",
    "蓄势待发"
]
labels = [
    "新能源电车",
    "动力电池",
    "白酒消费",
    "蓄势待发"
]

embeddings = model.encode(text)
print(embeddings.shape)

sim = cosine_similarity(embeddings)
print(sim)
print("语义相似度矩阵（余弦相似度）")
print("embedding model = " ,model_id)

print("PCA降维开始")

pca = PCA(n_components=3)
pca_point = pca.fit_transform(embeddings)

print(pca_point.shape)

print("主成分方差解释率比例",pca.explained_variance_ratio_)
print("PCA result (componnenrs=3) = ", pca_point)

plot_3d([
    {"type":"point","data":pca_point,"labels":labels}
])


