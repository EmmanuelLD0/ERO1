"""
! this file will show off a demo of our code
"""

import osmnx as ox  # to load the graph from open street map
import matplotlib.pyplot as plt  # for graph visualization
import networkx as nx  # for merging graphs

print("Initial Survey of Montreal with Drones...")
print("Calculating the price for each sector...")

ox.settings.log_console = False
ox.settings.use_cache = True

locations = [
    ('Verdun, Montreal, Quebec, Canada', 'Verdun'),
    ('Outremont, Montreal, Quebec, Canada', 'Outremont'),
    ('Anjou, Montreal, Quebec, Canada', 'Anjou'),
    ('Rivière-des-Prairies, Montreal, Quebec, Canada', 'Rivière-des-Prairies'),
    ('Le plateau-Mont-Royal, Montreal, Quebec, Canada', 'Le plateau-Mont-Royal')
]

# Load the Montreal graph to connect the locations
montreal_graph = ox.graph_from_place('Montreal, Quebec, Canada', network_type='drive')
montreal_graph = ox.convert.to_undirected(montreal_graph)

# Function to calculate the centroid of a graph
def calculate_graph_centroid(graph):
    x, y = zip(*[(data['x'], data['y']) for node, data in graph.nodes(data=True)])
    centroid_x, centroid_y = sum(x) / len(x), sum(y) / len(y)
    return ox.distance.nearest_nodes(graph, centroid_x, centroid_y), centroid_x, centroid_y

# Initialize the merged graph with the first location's graph
place, name = locations[0]
merged_graph = ox.graph_from_place(place, network_type='drive')
merged_graph = ox.convert.to_undirected(merged_graph)

# Store the centroid nodes of each location graph
centroid_nodes = []

# Load and merge the rest of the location graphs
for location in locations:
    place, name = location
    graph = ox.graph_from_place(place, network_type='drive')
    graph = ox.convert.to_undirected(graph)
    merged_graph = nx.compose(merged_graph, graph)
    
    # Calculate the centroid of the graph
    centroid_node, centroid_x, centroid_y = calculate_graph_centroid(graph)
    centroid_nodes.append((centroid_node, centroid_x, centroid_y))

# Add synthetic edges between centroids using the Montreal graph
for i in range(len(centroid_nodes)):
    node_i, x_i, y_i = centroid_nodes[i]
    for j in range(i + 1, len(centroid_nodes)):
        node_j, x_j, y_j = centroid_nodes[j]
        
        # Find the nearest nodes in the Montreal graph
        nearest_node_i = ox.distance.nearest_nodes(montreal_graph, x_i, y_i)
        nearest_node_j = ox.distance.nearest_nodes(montreal_graph, x_j, y_j)
        
        # Calculate the shortest path length between the nearest nodes in the Montreal graph
        try:
            distance = nx.shortest_path_length(montreal_graph, source=nearest_node_i, target=nearest_node_j, weight='length')
            # Add synthetic edge between the centroids of the graphs
            merged_graph.add_edge(node_i, node_j, weight=distance, length=distance)
        except nx.NetworkXNoPath:
            print(f"No path found between {nearest_node_i} and {nearest_node_j} in the Montreal graph.")

filepath = "../data/sectors_merged.graphml"
ox.save_graphml(merged_graph, filepath)
