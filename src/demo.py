from drone_flight.flight_creator import *
from tools.display import display
from copy import deepcopy
from removal_planning.planning import truck_paths
from data.path_merged_sectors import sector_path, sec_price
from data.anjou_data import anjou_path, anjou_price

"""
! this file will show off a demo of our code
"""

import osmnx as ox  # to load the graph from open street map
import matplotlib.pyplot as plt  # for graph visualization
import multiprocessing as mp  # for parallel processing
import tkinter as tk  # for the graphical interface
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy


def demo(
    screen: tk.Label,
    title_label: tk.Label,
    fixed_cost: float,
    cost_km: float,
    speed: float,
    graph_images: list,
    drones: bool = True,
):
    print("Initial Survey of Montreal with Drones...")
    print("Calculating the price for each sector...")

    ox.settings.log_console = False
    ox.settings.use_cache = True

    locations = [
        ('Verdun, Montreal, Quebec, Canada', 'Verdun'),
        ('Outremont, Montreal, Quebec, Canada', 'Outremont'),
        ('Anjou, Montreal, Quebec, Canada', 'Anjou'),
        ('Rivière-des-Prairies, Montreal, Quebec, Canada', 'Rivière-des-Prairies'),
        ('Le plateau-Mont-Royal, Montreal, Quebec, Canada', 'Le plateau-Mont-Royal'),
        ('Merged', 'Merged Sectors')
    ]

    def merged_sector() -> tuple[nx.Graph, list[list[tuple[int, int]]], float, str] :
        G = ox.load_graphml('./src/data/sectors_merged.graphml')
        G = ox.convert.to_undirected(G)
        name = 'Merged Sectors'
        return G, sector_path, sec_price, name

    def process_location(location) -> tuple[nx.Graph, list[list[tuple[int, int]]], float, str] :
        place, name = location
        graph = ox.graph_from_place(place, network_type='drive')
        if drones:
            graph = ox.convert.to_undirected(graph)
            copy = deepcopy(graph)
            name = name + ' Drone'
            if name == 'Anjou Drone':
                return copy, anjou_path, anjou_price, name

            path, price = create_flight_pattern(graph, name, fixed_cost, cost_km, speed)
            return copy, path, price, name
        else:
            if name == 'Anjou':
                path, price = truck_paths(graph, 15)
            elif name == 'Verdun':
                path, price = truck_paths(graph, 1)
            elif name == 'Outremont':
                path, price = truck_paths(graph, 1)
            elif name == 'Le plateau-Mont-Royal':
                path, price = truck_paths(graph, 1)
            elif name == 'Merged':
                path, price = sector_path, sec_price
            else:
                print(f"Error: {name}")
                path = []
                price = 0
            name = name + ' Snowplow'
            return graph, path, price, name
            

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_location, loc) if loc[0] != 'Merged' else executor.submit(merged_sector) for loc in locations}

        for future in as_completed(futures):
            graph, path, price, name = future.result()
            print(f"{name} : ${round(price)}")
            display(graph, path, screen, name, title_label)

    print('-----------------------------------')
