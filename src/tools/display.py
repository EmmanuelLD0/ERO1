"""
! This file will display the graph of the city with the flight of the drone on it
"""

import tkinter as tk
from tkinter import Label
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
from PIL import Image, ImageTk
import osmnx as ox
import networkx as nx

graph_images = []

def create_image(G: nx.Graph):
    """
    This function will create an image of the graph
    @param G: nx.Graph: the graph of the city
    @return: Image: the image of the graph
    """
    edge_colors = [data.get('color', 'k') for u, v, key, data in G.edges(keys=True, data=True)]
    fig, ax = ox.plot_graph(G, edge_color=edge_colors, bgcolor='white', node_color='black', node_edgecolor='black', node_zorder=2, show=False)
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()
    img = Image.frombuffer('RGBA', canvas.get_width_height(), buf, 'raw', 'RGBA', 0, 1)
    return img

def update_image(img: Image, screen: Label):
    """
    This function will update the image on the screen
    @param img: Image: the image of the graph
    @param screen: tk.Canvas: the screen
    """
    img_tk = ImageTk.PhotoImage(img)
    screen.configure(image=img_tk)
    screen.image = img_tk  # Keep a reference to avoid garbage collection

def display(G: nx.Graph, path: list, screen: tk.Canvas, title: str, graph_title: Label, directionnal: bool = False):
    """
    This function will display the graph of the city with the flight of the drone on it
    @param G: nx.Graph: the graph of the city
    @param path: list: list: the flight pattern of the drones
    """
    color = ['r', 'g', 'b', 'y', 'm', 'c', 'k']
    nb_moves = 0 
    for i in range(len(path)):
        for j in range(len(path[i])):
            u, v = path[i][j][0], path[i][j][1]
            nb_moves += 1
            if G.has_edge(u, v):
                G[u][v][0].update({'color': color[i % 7]})
            if directionnal and G.has_edge(v, u):
                G[v][u][0].update({'color': color[i % 7]})

    print(f"Number of moves in {title}: {nb_moves}")
    img = create_image(G)
    graph_images.append((img, title))
    update_image(img, screen)
    graph_title.configure(text=title)
