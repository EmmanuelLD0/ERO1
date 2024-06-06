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

    verdun = ox.graph_from_place('Verdun, Montreal, Quebec, Canada', network_type='drive')
    verdun = ox.convert.to_undirected(verdun)
    l, price = create_flight_pattern(verdun, "verdun", fixed_cost, cost_km, speed)
    print(f"Verdun : ${round(price)}")

    display(verdun, l, screen, "Verdun")

    outremont = ox.graph_from_place('Outremont, Montreal, Quebec, Canada', network_type='drive')
    outremont = ox.convert.to_undirected(outremont )
    l, price = create_flight_pattern(outremont, "outremont", fixed_cost, cost_km, speed)
    print(f"Outrmont : ${round(price)}")

    display(outremont, l, screen, "Outremont")

    anjou = ox.graph_from_place('Anjou, Montreal, Quebec, Canada', network_type='drive')
    anjou = ox.convert.to_undirected(anjou)
    l, price = create_flight_pattern(anjou, "Anjou", fixed_cost, cost_km, speed)
    print(f"Anjou : ${round(price)}")

    display(anjou, l, screen, "Anjou")

    Rivière_des_Prairies = ox.graph_from_place('Rivière-des-Prairies, Montreal, Quebec, Canada', network_type='drive')
    Rivière_des_Prairies = ox.convert.to_undirected(Rivière_des_Prairies)
    l, price = create_flight_pattern(Rivière_des_Prairies, "Rivere-des-Prairies", fixed_cost, cost_km, speed)
    print(f"Rivière_des_Prairies : ${round(price)}")

    display(Rivière_des_Prairies, l, screen, "Rivere-des-Prairies")

    LPMR = ox.graph_from_place('Le plateau-Mont-Royal, Montreal, Quebec, Canada', network_type='drive')
    LPMR = ox.convert.to_undirected(LPMR)
    l, price = create_flight_pattern(LPMR, "Le plateau-Mont-Royal", fixed_cost, cost_km, speed)
    print(f"Le plateau-Mont-Royal : ${round(price)}")

    display(LPMR, l, screen, "Le plateau-Mont-Royal")

    print('-----------------------------------')

    print('Plowing the Snow...')

    # verdun = ox.graph_from_place(
    #     "Verdun, Montreal, Quebec, Canada", network_type="drive"
    # )
    # verdun = ox.convert.to_undirected(verdun)
    # # l, price = create_flight_pattern(verdun)
    # # print(f"Verdun : ${round(price)}")
    #
    # outremont = ox.graph_from_place(
    #     "Outremont, Montreal, Quebec, Canada", network_type="drive"
    # )
    # outremont = ox.convert.to_undirected(outremont)
    # # l, price = create_flight_pattern(outremont )
    # # print(f"Outrmont : ${round(price)}")
    #
    # anjou = ox.graph_from_place("Anjou, Montreal, Quebec, Canada", network_type="drive")
    # anjou = ox.convert.to_undirected(anjou)
    # # l, price = create_flight_pattern(anjou)
    # # print(f"Anjou : ${round(price)}")
    #
    # Rivière_des_Prairies = ox.graph_from_place(
    #     "Rivière-des-Prairies, Montreal, Quebec, Canada", network_type="drive"
    # )
    # Rivière_des_Prairies = ox.convert.to_undirected(Rivière_des_Prairies)
    # # l, price = create_flight_pattern(Rivière_des_Prairies)
    # # print(f"Rivière_des_Prairies : ${round(price)}")
    #
    # LPMR = ox.graph_from_place(
    #     "Le plateau-Mont-Royal, Montreal, Quebec, Canada", network_type="drive"
    # )
    # LPMR = ox.convert.to_undirected(LPMR)
    # # l, price = create_flight_pattern(LPMR)
    # # print(f"Le plateau-Mont-Royal : ${round(price)}")
    #
    # list = [
    #     (verdun, "Verdun", fixed_cost, cost_km, speed),
    #     (outremont, "Outremont", fixed_cost, cost_km, speed),
    #     (anjou, "Anjou", fixed_cost, cost_km, speed),
    #     (Rivière_des_Prairies, "Rivière des Prairies", fixed_cost, cost_km, speed),
    #     (LPMR, "Le plateau-Mont-Royal", fixed_cost, cost_km, speed),
    # ]
    #
    # with mp.Pool(5) as p:
    #     results = p.starmap(create_flight_pattern, list)
    #
    # i = 1
    # for result in results:
    #     print(f"{list[i-1][1]} : ${round(result[1])}")
    #     display(list[i - 1][0], result[0], screen, list[i-1][1])
    #     i += 1

    # show the first graph
    # if graph_images:
    #     display.update_image(graph_images[0][0], screen)
    #     title_label.config(text=graph_images[0][1])

        # print(f"{list[i-1][1]} : ${round(result[1])}")
