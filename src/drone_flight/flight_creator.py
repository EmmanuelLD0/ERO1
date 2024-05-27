"""
! This file will create the flight pattern of the drones
"""
import osmnx as ox
import networkx as nx

def create_flight_pattern(G : nx.Graph):
    """
    ! This function will create the flight pattern of the drones
    @param G: nx.Graph: the graph of the city
    @return: pair: list: the flight pattern of the drones, float: the price of the path
    """
    print("Creating flight pattern")
    #Create our drone
    drone = Drone()
    #Create the flight path
    flight_path = []
    #Create the price of the path
    price = drone.fixed_cost