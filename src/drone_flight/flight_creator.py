"""
! This file will create the flight pattern of the drones
"""
import osmnx as ox
import networkx as nx
from equipement.drone import Drone
from tools.dijikstra import dijikstra
from itertools import combinations

def is_eulerian(G : nx.Graph):
    """
    ! This function will check if the graph is eulerian
    @param G: nx.Graph: the graph of the city
    @return: bool: if the graph is eulerian
    """
    for node in G.nodes:
        if G.degree[node] % 2 != 0:
            return False
    return True

def find_eulerian_path_rec(G : nx.Graph, actual : int):
    """
    ! This function will find the eulerian path of the graph recursively
    @param G: nx.Graph: the graph of the city
    @param actual: int: the actual node
    @return: list: the eulerian path of the graph
    """
    if (len(G.edges) == 0):
        return []
    for edge in G.edges(actual):
        next_node = edge[1]
        G.remove_edge(actual, next_node)
        path = find_eulerian_path_rec(G, next_node)
        if path is None:
            G.add_edge(actual, next_node)
            continue
        return [actual] + path
    return None

def find_eulerian_circuit(G : nx.Graph):
    """
    ! This function will find the eulerian circuit of the graph
    @param G: nx.Graph: the graph of the city
    @return: list: the eulerian circuit of the graph
    """
    return find_eulerian_path_rec(G, list(G.nodes)[0])

def cpp(G : nx.Graph):
    """
    ! This function will create the flight pattern of the drones
    @param G: nx.Graph: the graph of the city
    @return: list: the flight pattern of the drones
    """
    if not nx.is_connected(G):
        raise ValueError("The graph is not connected.")

    # Find all nodes with odd degree
    odd_degree_nodes = [node for node, degree in G.degree() if degree % 2 == 1]

    # Compute all pairs of odd degree nodes. In each pair, compute the shortest
    # path between the nodes. Add the paths to a list.
    odd_node_pairs = list(combinations(odd_degree_nodes, 2))
    odd_node_pairs_shortest_paths = [(pair, nx.shortest_path(G, pair[0], pair[1])) for pair in odd_node_pairs]

    # Create a complete graph between all odd nodes. Each edge in this graph
    # represents a possible pairing of two odd nodes. The weight of each edge is
    # the length of the shortest path between these nodes in the original graph.
    odd_node_graph = nx.Graph()
    for pair, path in odd_node_pairs_shortest_paths:
        odd_node_graph.add_edge(pair[0], pair[1], weight=len(path) - 1)

    # Compute the minimum weight matching of the odd node graph. This gives us the
    # pairs of odd nodes that should be connected in the original graph.
    min_weight_matching = nx.algorithms.max_weight_matching(odd_node_graph, True)

    # For each pair of nodes in the minimum weight matching, connect the nodes in
    # the original graph by the shortest path between them.
    for node1, node2 in min_weight_matching:
        path = nx.shortest_path(G, node1, node2)
        path_edges = list(zip(path[:-1], path[1:]))
        G.add_edges_from(path_edges)

    # Compute the Eulerian circuit of the modified graph.
    euler_circuit = list(nx.eulerian_circuit(G))

    return euler_circuit


def calculate_price(G : nx.Graph, path : list, drone : Drone):
    """
    ! This function will calculate the price of the path
    @param G: nx.Graph: the graph of the city
    @param path: list: the path of the drones
    @param drone: Drone: the drone object
    @return: float: the price of the path
    """
    price = drone.fixed_cost
    for i in range(len(path) - 1):
        if not 0 in G[path[i][0]][path[i][1]]:
            continue
        price += drone.cost_km * (G[path[i][0]][path[i][1]][0]['length'] / 1000)
    return price

def create_flight_pattern(G : nx.Graph):
    """
    ! This function will create the flight pattern of the drones
    @param G: nx.Graph: the graph of the city
    @return: pair: list: the flight pattern of the drones, float: the price of the path
    """
    #check if the graph is eulerian
    if not is_eulerian(G):
        #Use cpp
        flight_path = cpp(G)
    else:
        #Use eulerian circuit
        flight_path = find_eulerian_circuit(G)
    #Create our dronfound between the two nodes 17052772 and 17052789e
    drone = Drone()
    #Calculate the price
    price = calculate_price(G, flight_path, drone)
    return flight_path, price
