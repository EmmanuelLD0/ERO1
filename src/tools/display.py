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
from matplotlib.patches import FancyArrowPatch


graph_images = []

def create_image(G: nx.Graph, path: list, edge_colors: dict, edge_labels: dict = {}):
    """
    This function will create an image of the graph
    @param G: nx.Graph: the graph of the city
    @return: Image: the image of the graph
    """
    #edge_colors = [data.get('color', 'k') for u, v, key, data in G.edges(keys=True, data=True)]
    #fig, ax = ox.plot_graph(G, edge_color=edge_colors, bgcolor='white', node_color='black', node_edgecolor='black', node_zorder=2, show=False)
    fig, ax = ox.plot_graph(G, bgcolor='white', node_color='black', node_edgecolor='black', node_zorder=2, show=False, close=True, node_size=1)


    for i, route in enumerate(path):
        for (u, v) in route:
            if edge_colors[(u, v)] is not None:
                x_start, y_start = G.nodes[u]['x'], G.nodes[u]['y']
                x_end, y_end = G.nodes[v]['x'], G.nodes[v]['y']
                arrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                                        color=edge_colors[(u, v)], arrowstyle='-|>', mutation_scale=10, lw=1)
                ax.add_patch(arrow)

    for (u, v), label in edge_labels.items():
        x_start, y_start = G.nodes[u]['x'], G.nodes[u]['y']
        x_end, y_end = G.nodes[v]['x'], G.nodes[v]['y']
        ax.text((x_start + x_end) / 2, (y_start + y_end) / 2, label, fontsize=8, fontweight='bold', color='black')

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
    color = ['r', 'g', 'b', 'y', 'm', 'c', 'k', 'w', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    edge_colors = {}
    edge_labels = {}
    for i in range(len(path)):
        for j in range(len(path[i])):
            u, v = path[i][j][0], path[i][j][1]
            edge_colors[(u, v)] = color[i % len(color)]
            if j == 0:
                edge_labels[(u, v)] = f'Start path {i}'
            if directionnal:
                edge_colors[(v, u)] = color[i % len(color)]

    img = create_image(G, path, edge_colors, edge_labels)
    graph_images.append((img, title))
    update_image(img, screen)
    graph_title.configure(text=title)
