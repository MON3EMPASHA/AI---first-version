from variables import graph, nodes, lines,H_Table,highlight_color

# Breadth-First Search (BFS)
def BFS(graph, start, goal, canvas, root, update_label):
    visited = []
    queue = [[start]]
    fringe = set()  

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node in visited:
            continue

        # Highlight the current node as visited
        visited.append(node)
        highlight_node(node, highlight_color, canvas, path)  # Highlight visited nodes
        canvas.update()
        root.after(500)

        # Update the animated label for visited nodes
        update_label(visited)

        if node == goal:
            print("Path found:", path)
            highlight_path(path, "green", canvas)  # Highlight the final path
            return path

        # Process neighbors
        for neighbor, cost in graph[node]:
            if neighbor not in visited and neighbor not in fringe:
                new_path = path.copy()
                new_path.append(neighbor)
                queue.append(new_path)
                
                # Highlight the node as a fringe node
                fringe.add(neighbor)
                highlight_node(neighbor, "red", canvas, path)  # Highlight fringe nodes
                canvas.update()
                root.after(500)

    print("No path found")
    return None

# Depth-First Search (DFS)
def DFS(graph, start, goal, canvas, root, update_label):
    visited = []
    stack = [[start]]
    fringe = set()  # Track fringe nodes

    while stack:
        path = stack.pop()
        node = path[-1]

        if node in visited:
            continue

        # Mark as visited
        visited.append(node)
        fringe.discard(node)  # Remove from fringe if it was there
        highlight_node(node, highlight_color, canvas, path)  # Highlight visited nodes
        canvas.update()
        root.after(500)

        # Update animated label for visited nodes
        update_label(visited)

        if node == goal:
            print("Path found:", path)
            highlight_path(path, "green", canvas)  # Highlight the final path
            return path

        # Explore neighbors
        for neighbor, cost in reversed(graph[node]):
            if neighbor not in visited and neighbor not in fringe:
                new_path = path + [neighbor]
                stack.append(new_path)

                # Highlight fringe nodes
                fringe.add(neighbor)
                highlight_node(neighbor, "red", canvas, path)  # Highlight fringe nodes
                canvas.update()
                root.after(500)

    print("No path found")
    return None

# Uniform Cost Search (UCS)
def path_cost(path):
    """Calculate the cost of a given path."""
    cost = 0
    for node in path:
        cost += node[1]
    return cost, path[-1][0]  # Return cost and the last node's ID

def UCS(graph, start, goal, canvas, root, update_label):
    visited = []
    queue = [[(start, 0)]]
    fringe = set()  # Track fringe nodes

    while queue:
        queue.sort(key=path_cost)  # Sort by path cost
        path = queue.pop(0)
        node = path[-1][0]

        if node in visited:
            continue

        # Mark as visited
        visited.append(node)
        fringe.discard(node)  # Remove from fringe if it was there
        highlight_node(node, highlight_color, canvas, path)  # Highlight visited nodes
        canvas.update()
        root.after(500)

        # Update animated label for visited nodes
        update_label(visited)

        if node == goal:
            print("Path found:", [(step[0], step[1]) for step in path])
            highlight_path([step[0] for step in path], "green", canvas)  # Highlight the final path
            return path

        # Explore neighbors
        for neighbor, cost in graph[node]:
            if neighbor not in visited and neighbor not in fringe:
                new_path = path.copy()
                new_path.append((neighbor, cost))
                queue.append(new_path)

                # Highlight fringe nodes
                fringe.add(neighbor)
                highlight_node(neighbor, "red", canvas, path)  # Highlight fringe nodes
                canvas.update()
                root.after(500)

    print("No path found")
    return None

def a_star_path_cost(path):
    """
    Calculate the f-cost of a given path (g + h).
    """
    g_cost = sum(cost for _, cost in path)  # Total actual cost
    last_node = path[-1][0]  # Last node in the path
    h_cost = H_Table.get(last_node, float('inf'))  # Heuristic cost
    return g_cost + h_cost
#kan s7 w hases en chatgpt bawzo mno lel llah
def a_star_search(graph, start, goal, canvas, root, update_label):
    queue = [[(start, 0)]]  # Priority queue containing paths
    visited = {}  # Tracks the lowest cost at which nodes were visited
    fringe = set()  # Tracks the nodes in the fringe

    while queue:
        # Sort by f-cost (g + h) before popping
        queue.sort(key=a_star_path_cost)
        path = queue.pop(0)
        current_node = path[-1][0]
        current_cost = sum(cost for _, cost in path)  # Total g-cost

        # Remove from fringe as it is now being visited
        fringe.discard(current_node)

        # Visualize the current node
        highlight_node(current_node, highlight_color, canvas, path)  # Highlight visited nodes
        canvas.update()
        root.after(500)

        # Update the animated label for visited nodes
        update_label([node for node, _ in path])

        # Check if goal is reached
        if current_node == goal:
            print("Path found:", [(node, cost) for node, cost in path])
            highlight_path([node for node, _ in path], "green", canvas)  # Highlight the final path
            return path

        # Update visited with the lowest cost for current_node
        if current_node not in visited or visited[current_node] > current_cost:
            visited[current_node] = current_cost

            # Explore neighbors
            for neighbor, cost in graph.get(current_node, []):
                # If not visited or part of the fringe, add to the queue
                if neighbor not in visited or visited[neighbor] > current_cost + cost:
                    new_path = path + [(neighbor, cost)]
                    queue.append(new_path)

                    # Highlight fringe nodes
                    if neighbor not in fringe:
                        fringe.add(neighbor)
                        highlight_node(neighbor, "red", canvas, path)  # Highlight fringe nodes in red
                        canvas.update()
                        root.after(500)

    print("No path found")
    return None

def greedy_path_cost(path):
    last_node = path[-1][0]  
    return H_Table.get(last_node, float('inf'))  # Heuristic cost


def greedy_search(graph, start, goal, canvas, root, update_label):
    visited = set()
    queue = [[(start, 0)]]
    fringe = set()  # Track fringe nodes

    while queue:
        # Sort the queue based on the heuristic (greedy_path_cost function)
        queue.sort(key=greedy_path_cost)
        path = queue.pop(0)
        current_node = path[-1][0]

        if current_node in visited:
            continue

        # Mark as visited
        visited.add(current_node)
        fringe.discard(current_node)  # Remove from fringe if it was there
        highlight_node(current_node, highlight_color, canvas, path)  # Highlight visited nodes
        canvas.update()
        root.after(500)

        # Update animated label for visited nodes
        update_label(list(visited))

        # Goal check
        if current_node == goal:
            print("Path found:", [(node, cost) for node, cost in path])
            highlight_path([node for node, _ in path], "green", canvas)  # Highlight final path
            return path

        # Explore neighbors
        for neighbor, cost in graph.get(current_node, []):
            if neighbor not in visited and neighbor not in fringe:
                new_path = path + [(neighbor, cost)]
                queue.append(new_path)

                # Highlight fringe nodes
                fringe.add(neighbor)
                highlight_node(neighbor, "red", canvas, path)  # Highlight fringe nodes in red
                canvas.update()
                root.after(500)

    print("No path found")
    return None


def highlight_node(node_id, color, canvas, path):
    """Highlight a node during the search."""
    if len(path) >= 2:
        # Check if path[-2] has the expected structure of (parent, parentCost)
        if isinstance(path[-2], tuple) and len(path[-2]) == 2:
            parent, parentCost = path[-2]
            print("Parent of node: ", node_id, "is ", parent)
            for node in nodes:
                if node.node_id == node_id and node.parent.node_id == parent:
                    canvas.itemconfig(node.circle, fill=color)
                    return
        else:
            print("Error: path[-2] does not contain the expected structure.")
            parent = path[-2]

            for node in nodes:
                if node.node_id == node_id and node.parent.node_id == parent:
                    canvas.itemconfig(node.circle, fill=color)
                    return
    for node in nodes:
        if node.node_id == node_id:
            canvas.itemconfig(node.circle, fill=color)
            break


def highlight_path(path, color, canvas):
    """Highlight the final path."""
    for i in range(len(path) - 1):
        start_node = path[i]
        end_node = path[i + 1]
        for line in lines:
            if (line.parent.node_id == start_node and line.child.node_id == end_node) or \
               (line.parent.node_id == end_node and line.child.node_id == start_node):  # For undirected graphs
                canvas.itemconfig(line.line, fill=color, width=3)
                break
