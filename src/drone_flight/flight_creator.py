"""
! This file will create the flight pattern of the drones
"""
import osmnx as ox
import networkx as nx
from equipement import Drone

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
        raise ValueError("Usage error: the graph is not eulerian, will be fixed later")
    #Create our drone
    drone = Drone()
    #Create the flight path
    flight_path = find_eulerian_circuit(G)
    #Calculate the price
    price = calculate_price(G, flight_path, drone)
    return flight_path, price