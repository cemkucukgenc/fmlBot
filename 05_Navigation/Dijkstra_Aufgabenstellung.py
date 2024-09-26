def dijkstra(startnode):
    # 0 Initialisierung

    # NB contains the adjacency list for the graph
    NB = {"a": {"k": 3, "d": 4},
          "b": {"k": 4, "c": 4.5, "l": 9},
          "c": {"k": 3, "b": 4.5, "l": 8, "e": 4.5, "g": 3, "j": 4},
          "d": {"a": 4, "k": 5, "j": 2.5, "h": 6},
          "e": {"c": 4.5, "g": 3.5, "i": 3.5},
          "f": {"j": 4, "o": 3, "p": 2},
          "g": {"j": 5, "c": 3, "e": 3.5, "i": 3},
          "h": {"d": 6, "j": 4, "o": 3},
          "i": {"g": 3, "e": 3.5, "q": 4, "n": 4, "p": 3.5},
          "j": {"d": 2.5, "c": 4, "g": 5, "f": 4, "h": 4},
          "k": {"a": 3, "d": 5, "c": 3, "b": 4},
          "l": {"b": 9, "c": 8, "q": 3},
          "m": {"o": 4, "p": 2.5, "n": 3},
          "n": {"m": 3, "i": 4, "q": 3.5},
          "o": {"h": 3, "f": 3, "p": 3, "m": 4},
          "p": {"o": 3, "f": 2, "m": 2.5, "i": 3.5},
          "q": {"n": 3.5, "i": 4, "l": 3}
          }

    # MK is the set of nodes to be processed
    MK = list(NB.keys())

    # D will store the shortest distance from the start node to each node
    D = {node: float('inf') for node in NB}
    D[startnode] = 0  # The distance to the start node is 0

    # R will store the shortest path for each node
    R = {node: [] for node in NB}

    # Iterationen
    while len(MK) != 0:

        # 1. Select the node h from MK with D[h] = min {D[i] | i ∈ MK}
        dis_start = float('inf')
        for node in MK:
            dis_start_node = D[node]
            if dis_start_node < dis_start:
                new_node = node
                dis_start = dis_start_node
        current_node = new_node

        # 2. For each neighbor j of the current node, update the distance if needed
        for neighbor in NB[current_node]:
            if D[neighbor] > D[current_node] + NB[current_node][neighbor]:
                D[neighbor] = D[current_node] + NB[current_node][neighbor]
                R[neighbor] = R[current_node] + [current_node]

        # 3. Remove the current node from MK
        MK.remove(current_node)

    # Add the startnode to its own path
    R[startnode] = [startnode]
    return R, D


# Running the algorithm starting from node 'a'
paths, distances = dijkstra("a")

print("Shortest paths from a:")
for node, path in paths.items():
    print(f"Node {node}: Path = {path}, Distance = {distances[node]}")
