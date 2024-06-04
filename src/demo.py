from drone_flight.flight_creator import *
"""
! this file will show off a demo of our code
"""

import osmnx as ox # to load the graph from open street map
import matplotlib.pyplot as plt # for graph visualization
import multiprocessing as mp # for parallel processing

print('Initial Survey of Montreal with Drones...')
print('Calculating the price for each sector...')

ox.settings.log_console = False
ox.settings.use_cache = True

verdun = ox.graph_from_place('Verdun, Montreal, Quebec, Canada', network_type='drive')
verdun = ox.convert.to_undirected(verdun)
# l, price = create_flight_pattern(verdun)
# print(f"Verdun : ${round(price)}")

outremont = ox.graph_from_place('Outremont, Montreal, Quebec, Canada', network_type='drive')
outremont = ox.convert.to_undirected(outremont )
# l, price = create_flight_pattern(outremont )
# print(f"Outrmont : ${round(price)}")

anjou = ox.graph_from_place('Anjou, Montreal, Quebec, Canada', network_type='drive')
anjou = ox.convert.to_undirected(anjou)
# l, price = create_flight_pattern(anjou)
# print(f"Anjou : ${round(price)}")

Rivière_des_Prairies = ox.graph_from_place('Rivière-des-Prairies, Montreal, Quebec, Canada', network_type='drive')
Rivière_des_Prairies = ox.convert.to_undirected(Rivière_des_Prairies)
# l, price = create_flight_pattern(Rivière_des_Prairies)
# print(f"Rivière_des_Prairies : ${round(price)}")

LPMR = ox.graph_from_place('Le plateau-Mont-Royal, Montreal, Quebec, Canada', network_type='drive')
LPMR = ox.convert.to_undirected(LPMR)
# l, price = create_flight_pattern(LPMR)
# print(f"Le plateau-Mont-Royal : ${round(price)}")

list = [(verdun, "Verdun"), (outremont, "Outremont") , (anjou, "Anjou"), \
        (Rivière_des_Prairies, "Rivière des Prairies"), (LPMR, "Le plateau-Mont-Royal")]

with mp.Pool(5) as p:
    results = p.starmap(create_flight_pattern, list)

i = 0
for result in results:
    print(f"{list[i][1]} : ${round(result[1])}")
    i+=1

print('-----------------------------------')

print('Plowing the Snow...')
