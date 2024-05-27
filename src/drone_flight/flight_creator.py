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
    #get the odd nodes
    odd_nodes = [v for v in G.nodes if G.degree[v] % 2 != 0]
    #pair the odd nodes
    odd_pairs = list(combinations(odd_nodes, 2))
    #calculate the shortest path between the odd nodes
    shortest_path = dict()
    for pair in odd_pairs:
        shortest_path[pair] = dijikstra(G, pair[0], pair[1])
    #find the minimum weight matching
    min_pairs = []
    min_distance = float('inf')
    
    for pair_set in combinations(odd_pairs, len(odd_nodes) // 2):
        covered = set(sum(pair_set, ()))
        if len(covered) == len(odd_nodes):
            distance = sum(shortest_path[u][v] for u, v in pair_set)
            if distance < min_distance:
                min_distance = distance
                min_pairs = pair_set
    
    #add the shortest paths to the graph
    for u, v in min_pairs:
        path = dijikstra(G, u, v)
        for i in range(len(path) - 1):
            G.add_edge(path[i], path[i + 1])
        
    #Find eulerian circuit
    flight_path = find_eulerian_circuit(G)
    return flight_path

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
        price += drone.cost_km * G[path[i]][path[i + 1]]['length']
    return price

def create_flight_pattern(G : nx.Graph):
    """
    ! This function will create the flight pattern of the drones
    @param G: nx.Graph: the graph of the city
    @return: pair: list: the flight pattern of the drones, float: the price of the path
    """
    print("Creating flight pattern")
    #check if the graph is eulerian
    if not is_eulerian(G):
        #Use cpp
        flight_path = cpp(G)
    else:
        #Use eulerian circuit
        flight_path = find_eulerian_circuit(G)
    #Create our drone
    drone = Drone()
    #Calculate the price
    price = calculate_price(G, flight_path, drone)
    return flight_path, price
