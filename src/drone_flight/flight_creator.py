"""
! This file will create the flight pattern of the drones
"""

import osmnx as ox
import networkx as nx
from equipement.drone import Drone
from tools.dijikstra import dijikstra
from itertools import combinations
from datetime import datetime, timedelta


def is_eulerian(G: nx.Graph):
    """
    ! This function will check if the graph is eulerian
    @param G: nx.Graph: the graph of the city
    @return: bool: if the graph is eulerian
    """
    for node in G.nodes:
        if G.degree[node] % 2 != 0:
            return False
    return True


def find_eulerian_path_rec(G: nx.Graph, actual: int):
    """
    ! This function will find the eulerian path of the graph recursively
    @param G: nx.Graph: the graph of the city
    @param actual: int: the actual node
    @return: list: the eulerian path of the graph
    """
    if len(G.edges) == 0:
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


def find_eulerian_circuit(G: nx.Graph):
    """
    ! This function will find the eulerian circuit of the graph
    @param G: nx.Graph: the graph of the city
    @return: list: the eulerian circuit of the graph
    """
    return find_eulerian_path_rec(G, list(G.nodes)[0])


def cpp(G: nx.Graph):
    """
    ! This function will create the flight pattern of the drones
    @param G: nx.Graph: the graph of the city
    @return: list: the flight pattern of the drones
    """
    if not nx.is_connected(G):
        raise ValueError("The graph is not connected.")

    odd_degree_nodes = [node for node, degree in G.degree() if degree % 2 == 1]
    odd_node_pairs = list(combinations(odd_degree_nodes, 2))
    odd_node_pairs_shortest_paths = [
        (pair, nx.shortest_path(G, pair[0], pair[1])) for pair in odd_node_pairs
    ]

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

def calculate_price(G: nx.Graph, path: list, drones: list, sector: str):
    """
    ! This function will calculate the price of the path
    @param G: nx.Graph: the graph of the city
    @param path: list: the path of the drones
    @param drones: list: listy of the drones
    @return: pair: (list: (pair: int int)) int the price of the path and the new path
    """
    times = [datetime.strptime("00:00:00", "%H:%M:%S") for i in range(len(drones))]
    price = drones[0].fixed_cost * len(drones)
    active_drone_index = 0
    new_path = []
    new_path.append([])
    for i in range(len(path)):
        if (
            not 0
            in G[path[i][0]][
                path[i][1]
            ]
        ):
            continue
        if timedelta(
            seconds=G[path[i][0]][
                path[i][1]
            ][0]["length"]
            / drones[active_drone_index].speed
        ) + times[active_drone_index] > datetime.strptime("23:59:59", "%H:%M:%S"):
            if active_drone_index == len(drones) - 1:
                return [], -1
            active_drone_index += 1
            new_path.append([])

        price += drones[active_drone_index].cost_km * (
            G[path[i][0]][
                path[i][1]
            ][0]["length"]
            / 1000
        )
        times[active_drone_index] += timedelta(
            seconds=G[path[i][0]][
                path[i][1]
            ][0]["length"]
            / drones[active_drone_index].speed
        )
        new_path[active_drone_index].append(path[i])
        # check that the time is still in the first day
        if times[active_drone_index] > datetime.strptime("23:59:59", "%H:%M:%S"):
            # went over time needs more drones
            return [], -1
    return new_path, price


def create_flight_pattern(G: nx.Graph, sector: str, fixed_cost: float, cost_km: float, speed: float):
    """
    ! This function will create the flight pattern of the drones
    @param G: nx.Graph: the graph of the city
    @return: pair: list: list: pair: int, int the flight pattern of all the drones, float: the price of the path
    """
    # check if the graph is eulerian
    if not is_eulerian(G):
        # Use cpp
        flight_path = cpp(G)
    else:
        # Use eulerian circuit
        flight_path = find_eulerian_circuit(G)
    # Create our dronfound between the two nodes 17052772 and 17052789e
    drone = Drone()
    drone.fixed_cost = fixed_cost
    drone.cost_km = cost_km
    drone.speed = speed
    drones = [drone]
    # Calculate the price
    new_path, price = calculate_price(G, flight_path, drones, sector)
    while price == -1:
        new_drone = Drone()
        new_drone.fixed_cost = fixed_cost
        new_drone.cost_km = cost_km
        new_drone.speed = speed
        drones.append(new_drone)
        new_path, price = calculate_price(G, flight_path, drones, sector)
    return new_path, price
