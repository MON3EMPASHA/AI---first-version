import tkinter as tk

from variables import  graph,node_radius, node_fill_color, node_outline_color, line_color, font, nodes, lines, graph, node_ids

class Node:
    """Class representing a tree node."""
    def __init__(self, canvas, node_id, x, y, start_node_combobox, end_node_combobox, parent=None,heuristic=None):
        self.canvas = canvas
        self.node_id = node_id  # Display name (e.g., "A", "B", etc.)
        self.x = x
        self.y = y
        self.parent = parent
        self.children = []
        self.heuristic = heuristic

        # Unique internal ID for tracking multiple nodes with the same letter
        self.unique_id = id(self)

        # Create a unique tag for this node
        self.unique_tag = f"node_{self.unique_id}"

        # Draw the node
        self.circle = self.canvas.create_oval(
            x - node_radius,
            y - node_radius,
            x + node_radius,
            y + node_radius,
            fill=node_fill_color,
            outline=node_outline_color,
            tags=(self.unique_tag, f"node_{node_id}")
        )

        # Draw the node text
        self.text = self.canvas.create_text(
            x, y, text=self.node_id, font=font,
            tags=(self.unique_tag, f"node_{node_id}")
        )

        # Add a '+' button for expanding the node
        button = tk.Button(self.canvas.master, text="+", command=lambda: self.expand_node(start_node_combobox, end_node_combobox))
        self.button_window = self.canvas.create_window(
            x + node_radius + 20, y, window=button, tags=f"button_{node_id}"
        )

        # Initialize this node in the graph
        if node_id not in graph:
            graph[node_id] = []

    def add_child(self, child, cost=0):
        """Add a child node with a specified cost."""
        self.children.append(child)
        # Update the graph with (child, cost) instead of just the child
        graph[self.node_id].append((child.node_id, cost))
        if child.node_id not in graph:
            graph[child.node_id] = []

    def expand_node(self, start_node_combobox, end_node_combobox):
        """Add a new child to this node."""
        global nodes
        child_x = self.x - 80 + 160 * len(self.children)  # Spread children evenly
        child_y = self.y + 100  # Next row
        new_node_id = generate_node_id(len(nodes))  # Generate letter-based ID
        new_node = Node(self.canvas, new_node_id, child_x, child_y, start_node_combobox, end_node_combobox, self)
        nodes.append(new_node)
        
        # Default cost for new lines is 0
        self.add_child(new_node, cost=0)

        # Create a line with a default cost
        Line(self.canvas, self, new_node, cost=0)

        node_ids.append(new_node.node_id)  # Add the new node ID to the list
        start_node_combobox['values'] =  node_ids
        end_node_combobox['values'] =  node_ids

        print(graph)  # Debugging: print the updated graph structure
    def move(self, dx, dy):
        """Move the node and its button."""
        self.x += dx
        self.y += dy

        # Use the unique tag to move the node's circle and text separately
        self.canvas.move(self.unique_tag, dx, dy)

        # Update the position of the button
        self.canvas.coords(self.button_window, self.x + node_radius + 20, self.y)

        # Update the coordinates of connected lines
        for line in lines:
            if line.parent == self or line.child == self:
                line.update_coords()  # Update connected lines

class Line:
    """Class representing a line connecting nodes."""
    def __init__(self, canvas, parent, child, cost=0,):
        self.canvas = canvas
        self.parent = parent
        self.child = child
        self.cost = cost

        # Create the line
        self.line = self.canvas.create_line(
            parent.x,
            parent.y + node_radius,
            child.x,
            child.y - node_radius,
            fill=line_color,
            arrow=tk.LAST,
            tags=f"line_{parent.node_id}_{child.node_id}"
        )

        # Determine the position of the cost text
        self.update_cost_text_position()

        # Add this line to the global lines list
        lines.append(self)

        # Update the graph with the cost
        self.update_graph_with_cost()

    def update_coords(self):
        """Update the line and cost text coordinates based on parent and child positions."""
        # Update line coordinates
        self.canvas.coords(
            self.line,
            self.parent.x,
            self.parent.y + node_radius // 2,
            self.child.x,
            self.child.y - node_radius // 2
        )

        # Update the cost text position
        self.update_cost_text_position()

    def update_cost_text_position(self):
        """Position the cost text dynamically based on the direction of the line."""
        mid_x = (self.parent.x + self.child.x) / 2
        mid_y = (self.parent.y + self.child.y) / 2

        # Shift the cost label to the left or right based on the direction of the line
        if self.child.x > self.parent.x:  # Line goes to the right
            mid_x += 20  # Shift to the right
        else:  # Line goes to the left
            mid_x -= 20  # Shift to the left

        # Create or update the cost text
        if hasattr(self, 'cost_text'):
            self.canvas.coords(self.cost_text, mid_x, mid_y)
            self.canvas.itemconfig(self.cost_text, text=str(self.cost))
        else:
            self.cost_text = self.canvas.create_text(
                mid_x, mid_y, text=str(self.cost), font=font, fill="black",
                tags=f"cost_{self.parent.node_id}_{self.child.node_id}"
            )

    def update_graph_with_cost(self):
        """Update the graph with the line cost."""
        # Find the parent node's connections in the graph
        connections = graph[self.parent.node_id]

        # Remove any existing connection to the child and add the updated one
        connections = [(child, c) for child, c in connections if child != self.child.node_id]
        connections.append((self.child.node_id, self.cost))

        # Update the graph
        graph[self.parent.node_id] = connections
# A function to generate node IDs as letters (A, B, C, ...)
def generate_node_id(index):
    return chr(65 + index)  # 'A' starts at 65 in ASCII
