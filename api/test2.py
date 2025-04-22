import networkx as nx
import igraph as ig
import matplotlib.pyplot as plt

# 1. Create NetworkX DiGraph
graph_nx = nx.DiGraph()
graph_nx.add_edges_from([
    ("A", "B"),
    ("A", "C"),
    ("B", "D"),
    ("B", "E"),
    ("C", "F"),
])

# 2. Convert NetworkX to iGraph
g_ig = ig.Graph.from_networkx(graph_nx, vertex_attr_hashable="name")

# 3. Compute Reingold–Tilford layout
root_label = "A"
root_idx = g_ig.vs.find(name=root_label).index
layout_ig = g_ig.layout_reingold_tilford(root=[root_idx])

# 4. Convert back to NetworkX
G_back = g_ig.to_networkx(create_using=nx.DiGraph, vertex_attr_hashable="name")

# 5. Extract positions
pos = {v['name']: layout_ig.coords[v.index] for v in g_ig.vs}

# 6. Rotate layout for left-to-right growth
pos = {node: (y, x) for node, (x, y) in pos.items()}

# 7. Map y-coordinate to [0, 1000.0]
ys = [coord[1] for coord in pos.values()]
min_y, max_y = min(ys), max(ys)
if max_y - min_y != 0:
    pos = {
        node: (
            coord[0],
            (coord[1] - min_y) / (max_y - min_y) * 1000.0
        )
        for node, coord in pos.items()
    }
else:
    # 모든 y 값이 동일한 경우 중간값으로 설정
    pos = {node: (coord[0], 500.0) for node, coord in pos.items()}

# 8. Visualize with NetworkX
plt.figure(figsize=(8, 6))
nx.draw(
    G_back,
    pos=pos,
    with_labels=True,
    arrows=True,
    node_size=800,
    node_color='lightblue',
    font_size=10
)
plt.title("Tree Layout: Left-to-Right with Y-mapped [0,1000]")
plt.axis('off')
plt.show()
