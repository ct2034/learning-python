import mdptoolbox, mdptoolbox.example
import networkx as nx
import matplotlib.pyplot as plt

P, R = mdptoolbox.example.forest()
print(f"{P=}")
print(f"{R=}")

# Visualize the MDP
# Extract the adjacency matrix for the first action (P[0])
adj_matrix = P[0]
# rewards as edge annotations
edge_labels = {}
for i in range(len(adj_matrix)):
    for j in range(len(adj_matrix)):
        if adj_matrix[i][j] > 0:
            edge_labels[(i, j)] = f"{R[i][0]:.1f}"  # Assuming reward is same for all actions

g = nx.DiGraph(adj_matrix)
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(g)
nx.draw(g, pos, with_labels=True, node_size=700, node_color='lightblue', arrowsize=20)
nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
plt.show()

fh = mdptoolbox.mdp.FiniteHorizon(P, R, 0.9, 3)
fh.run()
print(f"{fh.V=}")
print(f"{fh.policy=}")
