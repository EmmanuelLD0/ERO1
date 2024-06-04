"""
! This file will display the graph of the city with the flight of the drone on it
"""

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt 

def display(G: nx.Graph, path: list):
    """
    This function will display the graph of the city with the flight of the drone on it
    @param G: nx.Graph: the graph of the city
    @param path: list: list: the flight pattern of the drones
    """
    color = ['r', 'g', 'b', 'y', 'm', 'c', 'k']
    
    for i in range(len(path)):
        for j in range(len(path[i])):
            u, v = path[i][j][0], path[i][j][1]
            if G.has_edge(u, v):
                G[u][v][0].update({'color': color[i % 7]})
            else:
                G.add_edge(u, v, color=color[i % 7])

    edge_colors = []
    for u, v, key, data in G.edges(keys=True, data=True):
        edge_colors.append(data.get('color', 'k'))

    fig, ax = ox.plot_graph(G, edge_color=edge_colors, bgcolor='white', node_color='black', node_edgecolor='black', node_zorder=2)
    plt.show() 