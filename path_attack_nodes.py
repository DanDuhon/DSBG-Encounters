from itertools import product
from collections import deque

# Define nodes
nodes = [
    (0,0),(0,2),(0,4),
    (1,1),(1,3),
    (2,0),(2,2),(2,4),
    (3,1),(3,3),
    (4,0),(4,2),(4,4)
]

# Define adjacency based on previous calculation
adjacency = {
    (0,0): {(1,1),(0,2),(2,0)},
    (0,2): {(1,1),(1,3),(0,0),(0,4),(2,2)},
    (0,4): {(1,3),(0,2),(2,4)},
    (1,1): {(0,0),(0,2),(2,0),(2,2),(1,3)},
    (1,3): {(0,2),(0,4),(2,2),(2,4),(1,1)},
    (2,0): {(1,1),(3,1),(0,0),(4,0),(2,2)},
    (2,2): {(1,1),(1,3),(3,1),(3,3),(0,2),(2,0),(2,4),(4,2)},
    (2,4): {(1,3),(3,3),(0,4),(2,2),(4,4)},
    (3,1): {(2,0),(2,2),(4,0),(4,2),(3,3)},
    (3,3): {(2,2),(2,4),(4,2),(4,4),(3,1)},
    (4,0): {(3,1),(2,0),(4,2)},
    (4,2): {(3,1),(3,3),(2,2),(4,0),(4,4)},
    (4,4): {(3,3),(2,4),(4,2)}
}

allNodeCombos = 13

# Revised approach: account for branching when multiple nodes are valid shortest-path steps
# We compute the set of all nodes visited along any shortest path from start to end

def nodes_visited_branching(start, end):
    visited_nodes = set()
    # BFS keeping track of all nodes visited along shortest paths
    queue = deque([[start]])
    min_length = None
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        path_length = len(path) - 1  # steps taken so far
        
        if min_length is not None and path_length > min_length:
            continue
        if node == end:
            visited_nodes.update(path[1:])  # exclude start, include end
            min_length = path_length
            continue
        # Find neighbors that move along a shortest path
        for neighbor in adjacency[node]:
            # Only proceed if neighbor is on a path that does not exceed current min_length
            if neighbor not in path:  # avoid cycles in current path
                queue.append(path + [neighbor])
    return visited_nodes

# Function to compute average nodes visited for given path length considering branching
def average_nodes_visited_branching(target_length):
    total_nodes = 0
    count_paths = 0
    for start in nodes:
        for end in nodes:
            # if start == end:
            #     continue
            # Compute all shortest paths length
            # BFS to determine shortest distance
            queue = deque([(start, 0)])
            distances = {start: 0}
            while queue:
                node, dist = queue.popleft()
                for neighbor in adjacency[node]:
                    if neighbor not in distances or dist+1 < distances[neighbor]:
                        distances[neighbor] = dist+1
                        queue.append((neighbor, dist+1))
            if distances.get(end, None) == target_length:
                visited = nodes_visited_branching(start, end)
                total_nodes += len(visited)
                count_paths += 1
    if count_paths == 0:
        return 0
    print(str(target_length) + ": " + str(count_paths))
    return total_nodes / count_paths

# Compute averages for path lengths 2, 3, 4 considering branching
avg_visited_branching = {l: average_nodes_visited_branching(l) for l in [1,2,3,4]}
print(avg_visited_branching)
