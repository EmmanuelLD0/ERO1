import src.tools.dijikstra as dj
import networkx as nx
import pytest

def test_pytest():
    assert 1 == 1

def test_empty_graph():
    G = nx.Graph()
    assert dj.dijikstra(G, 1, 2) == []

def test_non_existing_nodes():
    G = nx.Graph()
    G.add_edge(1, 2, weight=4)
    assert dj.dijikstra(G, 1, 3) == []

def test_no_path():
    G = nx.Graph()
    G.add_node(1)
    G.add_node(3)
    assert dj.dijikstra(G, 1, 3) == []

def test_one_path():
    G = nx.Graph()
    G.add_edge(1, 2, weight=4)
    G.add_edge(2, 3, weight=1)
    assert dj.dijikstra(G, 1, 3) == [1, 2, 3]

def test_multiple_paths():
    G = nx.Graph()
    G.add_edge(1, 2, weight=4)
    G.add_edge(2, 3, weight=4)
    G.add_edge(1, 3, weight=4)
    assert dj.dijikstra(G, 1, 3) == [1, 3]

def test_weights_matter():
    G = nx.Graph()
    G.add_edge(1, 2, weight=2)
    G.add_edge(2, 3, weight=1)
    G.add_edge(1, 3, weight=4)
    assert dj.dijikstra(G, 1, 3) == [1, 2, 3]
