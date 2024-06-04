"""
! This file will create the flight pattern of the drones
"""
import osmnx as ox
import networkx as nx
from equipement.drone import Drone
from tools.dijikstra import dijikstra
from itertools import combinations
from datetime import datetime, timedelta

def cpp(G : nx.Graph):
    """
    ! This function will create the flight pattern of the drones
    @param G: nx.Graph: the graph of the city
    @return: list: the flight pattern of the drones
    """
    if not nx.is_connected(G):
        raise ValueError("The graph is not connected.")

    odd_degree_nodes = [node for node, degree in G.degree() if degree % 2 == 1]
    odd_node_pairs = list(combinations(odd_degree_nodes, 2))
    odd_node_pairs_shortest_paths = [(pair, nx.shortest_path(G, pair[0], pair[1])) for pair in odd_node_pairs]

    odd_node_graph = nx.Graph()
    for pair, path in odd_node_pairs_shortest_paths:
        odd_node_graph.add_edge(pair[0], pair[1], weight=len(path) - 1)

    min_weight_matching = nx.algorithms.max_weight_matching(odd_node_graph, True)

    for node1, node2 in min_weight_matching:
        path = nx.shortest_path(G, node1, node2)
        path_edges = list(zip(path[:-1], path[1:]))
        G.add_edges_from(path_edges)

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
    time = datetime.strftime('00:00:00', '%H:%M:%S')
    price = drone.fixed_cost
    for i in range(len(path) - 1):
        if not 0 in G[path[i][0]][path[i][1]]:
            continue
        price += drone.cost_km * (G[path[i][0]][path[i][1]][0]['length'] / 1000)
        time += timedelta(seconds=G[path[i][0]][path[i][1]][0]['length'] / drone.speed)
        #check that the time is still in the first day
        if time > datetime.strftime('23:59:59', '%H:%M:%S'):
            print("The time is over the first day")
            price += drone.fixed_cost
            time = datetime.strftime('00:00:00', '%H:%M:%S')
    print("The drone took " + str(time) + " to complete the path.")
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
