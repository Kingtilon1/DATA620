# Import necessary libraries
import networkx as nx
import matplotlib.pyplot as plt
import random
G = nx.read_edgelist("email.txt",create_using=nx.DiGraph(), nodetype = int)

if not nx.is_weakly_connected(G):
    # Find the largest weakly connected component
    wcc = max(nx.weakly_connected_components(G), key=len)
    G = G.subgraph(wcc).copy()

# Calculate the diameter
diameter = nx.diameter(G.to_undirected())
print(f"Diameter of the largest weakly connected component: {diameter}")

avg_clustering_coefficient = nx.average_clustering(G.to_undirected())

## Going to get a sample of the edges for the graph 
sampled = random.sample(list(G.edges()), 100)
sampled_graph = nx.Graph(sampled)
print(f"Average clustering coefficient: {avg_clustering_coefficient}")
plt.figure(figsize=(10, 6))
nx.draw(sampled_graph, with_labels=True, node_color='skyblue', node_size=200, edge_color='gray')
plt.title('Email Communication Network')
plt.show()