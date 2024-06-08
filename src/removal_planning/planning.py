"""
! This file will create the flight pattern of the drones
"""

import osmnx as ox
import networkx as nx
from equipement.drone import Drone
from tools.dijikstra import dijikstra
from itertools import combinations
from datetime import datetime, timedelta
from copy import copy


def truck_paths(G, n_trucks):
    """
    ! This function merges or splits the truck paths created to match the wanted number of paths.
    @param G: DiGraph of the city
    @param n_trucks: number of paths wanted in the result
    @return: list of list of pairs representing the different paths and a 0
    """
    temp = get_path(G)
    paths = []
    for i in range(len(temp)):
        path = []
        for j in range(len(temp[i]) - 1):
            path.append((temp[i][j], temp[i][j + 1]))
        paths.append(path)
    while len(paths) < n_trucks:
        m = -1
        v = -1
        for i in range(len(paths)):
            if len(paths[i]) > v:
                m = i
                v = len(paths[i])
        if m == -1:
            break
        t1 = paths[m][:len(paths[m])//2]
        t2 = paths[m][len(paths[m])//2:]
        paths[m] = t2
        paths.append(t1)
    return paths, 0


def get_path(G):
    """
    ! This function takes a Digraph and gives a way to split the graph into paths that span it
    @param G: DiGraph of the city
    @return: list of list of pairs representing the different paths
    """
    if nx.is_empty(G):
        return []
    dE = G.edges
    if dE == []:
        return []
    unG = nx.Graph()
    edges_left = nx.DiGraph()
    for edge in dE:
        unG.add_edge(edge[0],edge[1])
        edges_left.add_edge(edge[0],edge[1])
    try:
        unG = nx.eulerize(unG)
    except Exception as e:
        res = []
        components = [G.subgraph(c).copy() for c in nx.strongly_connected_components(G)]
        for g in components:
            res += (get_path(g))
        return res
    path = []
    path = list(nx.eulerian_path(unG))
    i = len(path) - 1
    while i >= 0:
        start = path[:-1]
        (a,b) = path[i]
        if (a,b) in start or (b,a) in start:
            path.pop(len(path) - 1)
        else:
            break
        i -= 1
    reg = 0
    rev = 0
    for (a,b) in path:
        if (a,b) not in dE:
            reg += 1
        if (b,a) not in dE:
            rev += 1
    if reg > rev:
        path.reverse()
        for i in range(len(path)):
            (a,b) = path[i]
            path[i] = (b,a)
    le = len(path) - 1
    res = []
    for (a, b) in path:
        res.append(a)
        path_ex = False
        if (a, b) in dE:
            try:
                edges_left.remove_edge(a,b)
            except:
                pass
            try:
                edges_left.remove_edge(b,a)
            except:
                pass
            continue
        try:
            sP = nx.shortest_path(G, a, b)
        except:
            return [res] + get_path(edges_left)
        for i in range(len(sP) - 1):
            try:
                edges_left.remove_edge(sP[i], sP[i + 1])
            except:
                pass
        res += sP[1:-1]
        if (b, a) in dE and (b,a) not in path:
            try:
                edges_left.remove_edge(a,b)
            except:
                pass
            try:
                edges_left.remove_edge(b,a)
            except:
                pass
            res.append(b)
            res += sP[:-1]
    res.append(path[le][1])
    return [res]
