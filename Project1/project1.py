import pandas as pd
import networkx as nx
import scipy.stats as stats

# Load Facebook data
file_path = r'C:\Users\bobbt\Downloads\archive\cyberbullying_tweets.csv'
facebook_data = pd.read_excel(file_path, index_col=0)

# Create a directed graph
G = nx.DiGraph()

# Add nodes
for user in facebook_data.columns:
    G.add_node(user, type='real')  # You can adjust the type as needed

# Add edges
for follower in facebook_data.index:
    for followee in facebook_data.columns:
        if facebook_data.at[follower, followee] == 1:
            G.add_edge(follower, followee)

# Calculate centrality measures
degree_centrality = nx.degree_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G)

# Dummy assignment of node types (adjust this according to actual data if available)
for node in G.nodes():
    G.nodes[node]['type'] = 'real' if ' ' in node else 'fake'

# Group by type
real_users = [node for node in G.nodes() if G.nodes[node]['type'] == 'real']
fake_users = [node for node in G.nodes() if G.nodes[node]['type'] == 'fake']

degree_real = [degree_centrality[node] for node in real_users]
degree_fake = [degree_centrality[node] for node in fake_users]
eigen_real = [eigenvector_centrality[node] for node in real_users]
eigen_fake = [eigenvector_centrality[node] for node in fake_users]

# Perform t-test
t_stat_degree, p_value_degree = stats.ttest_ind(degree_real, degree_fake)
t_stat_eigen, p_value_eigen = stats.ttest_ind(eigen_real, eigen_fake)

print(f"Degree Centrality t-test: t={t_stat_degree}, p={p_value_degree}")
print(f"Eigenvector Centrality t-test: t={t_stat_eigen}, p={p_value_eigen}")
