"""
! this file will show off a demo of our code
"""
import osmnx as ox # to load the graph from open street map
import matplotlib.pyplot as plt # for graph visualization

ox.config(use_cache=True, log_console=True)
G = ox.graph_from_place('Montreal, Quebec, Canada', network_type='drive')

print(G)

ox.plot_graph(G, figsize=(10, 10), node_size=10, edge_linewidth=2) # will remove when we'll do the actual implementation
plt.show()
