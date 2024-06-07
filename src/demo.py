from drone_flight.flight_creator import *
from tools.display import display
from copy import deepcopy

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
):
    print("Initial Survey of Montreal with Drones...")
    print("Calculating the price for each sector...")

    ox.settings.log_console = False
    ox.settings.use_cache = True

    locations = [
        ('Verdun, Montreal, Quebec, Canada', 'verdun'),
        ('Outremont, Montreal, Quebec, Canada', 'outremont'),
        ('Anjou, Montreal, Quebec, Canada', 'Anjou'),
        ('Rivière-des-Prairies, Montreal, Quebec, Canada', 'Rivière-des-Prairies'),
        ('Le plateau-Mont-Royal, Montreal, Quebec, Canada', 'Le plateau-Mont-Royal')
    ]

    def process_location(location):
        place, name = location
        graph = ox.graph_from_place(place, network_type='drive')
        graph = ox.convert.to_undirected(graph)
        copy = deepcopy(graph)
        print(f"Number of edges in {name}: {graph.number_of_edges()}")
        path, price = create_flight_pattern(graph, name, fixed_cost, cost_km, speed)
        return copy, path, price, name

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_location, loc): loc for loc in locations}

        for future in as_completed(futures):
            graph, path, price, name = future.result()
            print(f"{name} : ${round(price)}")
            display(graph, path, screen, name, title_label)

    print('-----------------------------------')

    print('Plowing the Snow...')
