import tkinter as tk
from variables import graph,font, nodes, graph, node_ids,lines,H_Table
######### change Name Logic + Change Cost Logic (ChatGpt) #########
def on_double_click(event, canvas, start_node_combobox, end_node_combobox):
    """Handle double-click to edit a node's ID, a line's cost, or the cost text itself."""
    global editing_node
    closest_item = canvas.find_closest(event.x, event.y)[0]
    tags = canvas.gettags(closest_item)

    # Check if the double-click is on a line or its cost text
    for tag in tags:
        if tag.startswith("line_") or tag.startswith("cost_"):  # Line or cost text tags
            # If it's the cost text, derive the line's parent and child from the cost tag
            if tag.startswith("cost_"):
                _, parent_id, child_id = tag.split("_")  # Extract IDs from "cost_parentID_childID"
            else:  # If it's the line itself
                _, parent_id, child_id = tag.split("_")  # Extract IDs from "line_parentID_childID"

            # Find the corresponding Line object
            editing_line = next(
                (line for line in lines if line.parent.node_id == parent_id and line.child.node_id == child_id),
                None
            )

            if editing_line:
                # Create an entry widget to allow editing the cost
                entry = tk.Entry(canvas.master, font=font, width=5)
                mid_x, mid_y = canvas.coords(editing_line.cost_text)  # Get current position of the cost text
                entry.place(x=mid_x - 15, y=mid_y - 15)  # Position the entry near the cost text
                entry.insert(0, str(editing_line.cost))  # Pre-fill with the current cost

                def save_cost(event):
                    """Save the new cost and update the canvas and graph."""
                    try:
                        # Get the new cost as an integer
                        new_cost = int(entry.get().strip())
                        editing_line.cost = new_cost

                        # Update the cost text on the canvas
                        canvas.itemconfig(editing_line.cost_text, text=str(new_cost))

                        # Update the graph with the new cost
                        connections = graph[editing_line.parent.node_id]
                        for i, (child, cost) in enumerate(connections):
                            if child == editing_line.child.node_id:
                                connections[i] = (child, new_cost)  # Update the cost for the matching child
                                break

                        print(f"Updated graph: {graph}")  # Debugging: print the updated graph

                    except ValueError:
                        pass  # Ignore invalid input
                    finally:
                        entry.destroy()  # Remove the entry widget after saving

                # Bind Enter key to save changes
                entry.bind("<Return>", save_cost)

                return  # Exit the function after handling the line or cost case

    # If the double-click is not on a line or cost, handle the node editing
    for tag in tags:
        if tag.startswith("node_") and "_" in tag:
            unique_tag = tag
            editing_node = next((node for node in nodes if node.unique_tag == unique_tag), None)
            if editing_node:
                # Temporarily hide the text
                canvas.itemconfig(editing_node.text, state="hidden")

                # Create an entry widget to allow editing
                entry = tk.Entry(canvas.master, font=font, width=5)
                entry.insert(0, editing_node.node_id)
                entry.place(x=editing_node.x - 15, y=editing_node.y - 15)

                def save_changes(event):
                    """Save the new node ID and update the canvas, graph, H_Table, and other references."""
                    new_id = entry.get().strip()
                    if new_id and new_id != editing_node.node_id:
                        old_id = editing_node.node_id

                        # Update all Line objects connected to this node
                        for line in lines:
                            if line.parent == editing_node:  # If this node is the parent
                                line.parent.node_id = new_id
                                # Update canvas line and cost tags
                                canvas.itemconfig(line.line, tags=f"line_{new_id}_{line.child.node_id}")
                                canvas.itemconfig(line.cost_text, tags=f"cost_{new_id}_{line.child.node_id}")
                            elif line.child == editing_node:  # If this node is the child
                                line.child.node_id = new_id
                                # Update canvas line and cost tags
                                canvas.itemconfig(line.line, tags=f"line_{line.parent.node_id}_{new_id}")
                                canvas.itemconfig(line.cost_text, tags=f"cost_{line.parent.node_id}_{new_id}")

                        # Update the Node object
                        editing_node.node_id = new_id

                        # Update the graph dictionary:
                        # 1. Rename the key for the current node
                        graph[new_id] = graph.pop(old_id, [])

                        # 2. Update all edges pointing to the old node ID
                        for parent, edges in graph.items():
                            graph[parent] = [
                                (new_id if child == old_id else child, cost) for child, cost in edges
                            ]

                        # Update H_Table with the new ID
                        if old_id in H_Table:
                            H_Table[new_id] = H_Table.pop(old_id)  # Move the heuristic value to the new ID
                            print(f"Updated H_Table: {H_Table}")  # Debugging output for H_Table

                        # Update the text and tags of the node on the canvas
                        canvas.itemconfig(editing_node.text, text=new_id, state="normal")
                        canvas.itemconfig(editing_node.circle, tags=(editing_node.unique_tag, f"node_{new_id}"))
                        canvas.itemconfig(editing_node.text, tags=(editing_node.unique_tag, f"node_{new_id}"))

                        # Update the node IDs list
                        node_ids.remove(old_id)
                        node_ids.append(new_id)

                        # Update combobox values
                        start_node_combobox['values'] = remove_duplicates( node_ids)
                        end_node_combobox['values'] = remove_duplicates( node_ids)

                        print(f"Graph updated: {graph}")  # Debugging output for the graph

                    # Destroy the entry widget after saving
                    entry.destroy()

                # Bind Enter key to save changes
                entry.bind("<Return>", save_changes)

                break
#Add Heuristic Logic (ChatGpt)
def on_right_click(event, canvas):
    """Handle right-click to add or edit a heuristic value for a node."""
    global H_Table  # Ensure we can modify the global H_Table
    closest_item = canvas.find_closest(event.x, event.y)[0]  # Find the closest item to the click
    tags = canvas.gettags(closest_item)  # Get the tags of the closest item

    # Check if the click is on a node
    for tag in tags:
        if tag.startswith("node_"):
            # Find the corresponding Node object
            node = next((node for node in nodes if node.unique_tag == tag), None)

            if node:
                # Create an entry widget to allow heuristic input
                entry = tk.Entry(canvas.master, font=font, width=5)
                entry.place(x=node.x - 20, y=node.y - 30)  # Position near the node
                entry.insert(0, str(node.heuristic or ""))  # Pre-fill with current heuristic, if any

                def save_heuristic(event):
                    """Save the heuristic value, update the node, and update H_Table."""
                    try:
                        for N in nodes:
                            if N.node_id==node.node_id:
                                # Get the new heuristic value as an integer
                                new_heuristic = int(entry.get().strip())
                                N.heuristic = new_heuristic

                                # Update the H_Table
                                H_Table[N.node_id] = new_heuristic

                                # Optionally display the heuristic on the canvas
                                if hasattr(N, 'heuristic_text'):
                                    canvas.itemconfig(N.heuristic_text, text=f"h: {new_heuristic}")
                                else:
                                    N.heuristic_text = canvas.create_text(
                                        N.x, N.y - 30,  # Display below the node
                                        text=f"h: {new_heuristic}", font=font, fill="blue",
                                        tags=(N.unique_tag, f"heuristic_{N.node_id}")
                                    )

                                # Print the updated H_Table for debugging
                                print("Updated H_Table:", H_Table)

                    except ValueError:
                        print("Invalid heuristic value entered!")  # Debugging: Notify of invalid input
                    finally:
                        entry.destroy()  # Remove the entry widget after saving

                # Bind the Enter key to save changes
                entry.bind("<Return>", save_heuristic)

                return  # Exit after handling the node


#Drag Logic
def on_drag_start(event,canvas):
    """Start dragging a node."""
    global dragged_node
    closest_item = canvas.find_closest(event.x, event.y)[0]
    tags = canvas.gettags(closest_item)

    # Identify the node uniquely using its `unique_tag`
    for tag in tags:
        if tag.startswith("node_") and "_" in tag:  # Ensure it is a node's unique tag
            unique_tag = tag
            dragged_node = next((node for node in nodes if node.unique_tag == unique_tag), None)
            if dragged_node:
                break
def on_drag_move(event):
    """Move the dragged node along with updating all connected lines."""
    if dragged_node is not None:
        dx = event.x - dragged_node.x
        dy = event.y - dragged_node.y
        dragged_node.move(dx, dy)
def on_drag_stop(event):
    """Stop dragging the node."""
    global dragged_node
    dragged_node = None
def remove_duplicates(input_list):
    # Use a set to track seen items and a list to store the unique ones
    seen = set()
    result = []
    for item in input_list:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result