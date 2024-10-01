# Define the graph based on extracted connections
graph = {"a": {"b": 2, "d": 5, "f": 6},
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

path_colors = {
    ("a", "b"): "red",
    ("a", "d"): "blue",
    ("a", "f"): "yellow",
    ("b", "c"): "blue",
    ("b", "e"): "red",
    ("c", "g"): "blue",
    ("c", "e"): "red",
    ("d", "e"): "red",
    ("d", "h"): "yellow",
    ("e", "g"): "blue",
    ("e", "h"): "yellow",
    ("f", "d"): "blue",
    ("f", "i"): "red",
    ("g", "j"): "red",
    ("h", "j"): "red",
    ("h", "k"): "blue",
    ("i", "h"): "yellow",
    ("i", "l"): "blue",
    ("j", "n"): "yellow",
    ("j", "k"): "blue",
    ("k", "i"): "red",
    ("k", "n"): "yellow",
    ("l", "m"): "red",
    ("m", "k"): "blue",
    ("n", "o"): "red",
}

# Implement Dijkstra's algorithm using the existing function
def dijkstra(graph, startnode, endnode):
    D = {node: float('inf') for node in graph}  # Distance dictionary
    D[startnode] = 0
    R = {node: [] for node in graph}  # Route dictionary
    MK = [startnode]

    while MK:
        # Find the node with the smallest distance in MK
        current_node = min(MK, key=lambda node: D[node])

        # Remove it from MK
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
    # Iterate through the path to get the colors for each segment
    for i in range(len(path) - 1):
        # Get the color for the segment (path[i], path[i+1])
        segment_color = path_colors.get((path[i], path[i + 1])) or path_colors.get((path[i + 1], path[i]))
        if segment_color:
            color_list.append(segment_color)
    return color_list

# Example usage with the Dijkstra path
start = "a"
end = "n"
path = dijkstra(graph, start, end)
print("Shortest path from {} to {}:".format(start, end), path)

# Get the color list for the path
color_list = get_path_colors(path, path_colors)
print("Color list for the path {}: {}".format(path, color_list))
