"""
! Dijikstra's Algorithm
"""
import osmnx as ox
import networkx as nx

def dijikstra(G : nx.Graph, start : int, end : int):
    """
    ! This function will find the shortest path between two nodes
    @param G: nx.Graph: the graph of the city
    @param start: int: the starting node
    @param end: int: the ending node
    @return: list: the shortest path between the two nodes
    """
    ans = []
    Q = []
    for node in G.nodes:
        G.nodes[node]['visited'] = False
        G.nodes[node]['distance'] = float('inf')
        Q.append((G.nodes[node]['distance'], node))
    G.nodes[start]['distance'] = 0

    while len(Q) > 0:
        Q.sort(key=lambda tup: tup[0])
        u = Q.pop(0)[1]
        if u == end:
            break
        for v in G.neighbors(u):
            alt = G.nodes[u]['distance'] + G[u][v][0]['length']
            if alt < G.nodes[v]['distance']:
                G.nodes[v]['distance'] = alt
                G.nodes[v]['previous'] = u
    
    u = end
    if G.nodes[u]['distance'] == float('inf') or G.nodes[u]['previous'] is None:
        raise ValueError("No path found between the two nodes " + str(start) + " and " + str(end))
    while u is not None:
        ans.insert(0, u)
        u = G.nodes[u]['previous']

    return ans
