# Define the graph based on extracted connections
graph = {
    "a": {"b": 2, "d": 5, "f": 6},
    "b": {"c": 3, "e": 2},
    "c": {"g": 8, "e": 1},
    "d": {"e": 1, "h": 10},
    "e": {"g": 10, "h": 10},
    "f": {"d": 2, "i": 4},
    "g": {"j": 8},
    "h": {"j": 6, "k": 6},
    "i": {"h": 7, "l": 4},
    "j": {"n": 5, "k": 7},
    "k": {"i": 7, "n": 9},
    "l": {"m": 9},
    "m": {"k": 1},
    "n": {"o": 1},
    "o": {},
}

# Define the colors for the paths
path_colors = {
    ("a", "b"): "Red",
    ("a", "d"): "Blue",
    ("a", "f"): "Yellow",
    ("b", "c"): "Blue",
    ("b", "e"): "Red",
    ("c", "g"): "Blue",
    ("c", "e"): "Red",
    ("d", "e"): "Red",
    ("d", "h"): "Yellow",
    ("e", "g"): "Blue",
    ("e", "h"): "Yellow",
    ("f", "d"): "Blue",
    ("f", "i"): "Red",
    ("g", "j"): "Red",
    ("h", "j"): "Red",
    ("h", "k"): "Blue",
    ("i", "h"): "Yellow",
    ("i", "l"): "Blue",
    ("j", "n"): "Yellow",
    ("j", "k"): "Blue",
    ("k", "i"): "Red",
    ("k", "n"): "Yellow",
    ("l", "m"): "Red",
    ("m", "k"): "Blue",
    ("n", "o"): "Red",
}

# Function to perform Dijkstra's algorithm
def dijkstra(graph, startnode, endnode):
    D = {node: float('inf') for node in graph}  # Distance dictionary
    D[startnode] = 0
    R = {node: [] for node in graph}  # Route dictionary
    MK = [startnode]

    while MK:
        # Find the node with the smallest distance in MK
        current_node = min(MK, key=lambda node: D[node])
        MK.remove(current_node)

        # Check neighbors
        for neighbor, weight in graph[current_node].items():
            distance = D[current_node] + weight
            if distance < D[neighbor]:
                D[neighbor] = distance
                R[neighbor] = R[current_node] + [current_node]
                if neighbor not in MK:
                    MK.append(neighbor)

    # Return the shortest path from startnode to endnode
    return R[endnode] + [endnode]

# Function to get the color list for a given path
def get_path_colors(path, path_colors):
    color_list = []
    for i in range(len(path) - 1):
        # Get the color for the segment (path[i], path[i+1]) or (path[i+1], path[i])
        segment_color = path_colors.get((path[i], path[i + 1])) or path_colors.get((path[i + 1], path[i]))
        if segment_color:
            color_list.append(segment_color)
    return color_list

# Modular function to get the path as a color list
def get_path_color_list(start, end, graph, path_colors):
    # Get the shortest path using Dijkstra's algorithm
    path = dijkstra(graph, start, end)
    # Get the color list for the path
    return get_path_colors(path, path_colors)

# # Example usage of the modular function
# start_point = "a"
# end_point = "n"
# color_list = get_path_color_list(start_point, end_point, graph, path_colors)
# print(color_list)
