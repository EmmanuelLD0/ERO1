from drone_flight.flight_creator import *
"""
! this file will show off a demo of our code
"""

import osmnx as ox # to load the graph from open street map
import matplotlib.pyplot as plt # for graph visualization

ox.settings.log_console = False
ox.settings.use_cache = True

G = ox.graph_from_place('Montreal, Quebec, Canada', network_type='drive')
G = ox.convert.to_undirected(G)

# l, price = create_flight_pattern(G)

# print(l)
# print(price)

ox.plot_graph(G, figsize=(10, 10), node_size=10, edge_linewidth=2) # will remove when we'll do the actual implementation
plt.show()
