# 导入 NetworkX：它提供创建和分析图结构的工具。
import networkx as nx
# 导入 Matplotlib：NetworkX 用它把图画出来。
import matplotlib.pyplot as plt

# 创建一个无向图：校园的双向步行路线没有方向。
campus = nx.Graph()

# 加入节点；每个字符串是一处地点。
campus.add_nodes_from(["图书馆", "教学楼", "食堂", "宿舍", "体育馆"])

# 加入带权重的边；weight 是两地之间的步行分钟数。
campus.add_weighted_edges_from([
    ("图书馆", "教学楼", 4),
    ("教学楼", "食堂", 3),
    ("教学楼", "宿舍", 6),
    ("食堂", "宿舍", 5),
    ("体育馆", "宿舍", 7),
])

# spring_layout 根据连接关系计算绘图位置，seed 让每次运行的布局一致。
positions = nx.spring_layout(campus, seed=7)

# 画节点；pos 指定位置，node_color 指定节点颜色，node_size 指定节点大小。
nx.draw_networkx_nodes(campus, pos=positions, node_color="#9ecae1", node_size=1800)
# 画无向边；pos 指定位置，width 指定线条粗细。
nx.draw_networkx_edges(campus, pos=positions, width=2)
# 把地点名称写在节点上；font_family 让中文字体由环境选择。
nx.draw_networkx_labels(campus, pos=positions, font_size=11, font_family="Arial Unicode MS")

# 取出每条边的权重，供下一行标到边上。
edge_labels = nx.get_edge_attributes(campus, "weight")
# 在边旁标出步行分钟数；pos 指定位置，edge_labels 提供“边→文字”的映射。
nx.draw_networkx_edge_labels(campus, pos=positions, edge_labels=edge_labels, font_size=10)

# 标题说明：这是无向、加权的关系网络。
plt.title("Campus walking network: undirected and weighted")
# 隐藏坐标轴，因为坐标值不是这个模型关心的内容。
plt.axis("off")
# 调整边距，避免标题或标签被裁掉。
plt.tight_layout()
# 显示这张图。
plt.show()

# degree 表示每个地点直接相连的地点数。
print("degree:", dict(campus.degree()))
# betweenness 表示一个地点出现在其他地点最短路径中的相对频繁程度。
print("betweenness:", nx.betweenness_centrality(campus))
