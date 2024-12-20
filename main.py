import tkinter as tk
from tkinter import ttk
from variables import xroot, rightFrameBackground, graph, nodes, lines, graph, node_ids, H_Table,leftFrameBackground,labelscol,node_fill_color,line_color
from algorithms import BFS, DFS, UCS, a_star_search, greedy_search
from changeName_changeCost_drag import on_double_click, on_drag_start, on_drag_move, on_drag_stop, on_right_click
from classes import Node, Line


def add_root_node():
    root_node = Node(canvas, 'A', xroot, 100, start_node_combobox, end_node_combobox)  
    nodes.append(root_node)
    node_ids.append(root_node.node_id)
    start_node_combobox['values'] = node_ids
    end_node_combobox['values'] = node_ids

def reset():
    global nodes, lines
    canvas.delete("all")
    nodes.clear()
    lines.clear()
    graph.clear()
    H_Table.clear()
    animated_path_label['text'] = ""
    animated_closed_label['text'] = ""
    node_ids.clear()
    # Add the root node again
    add_root_node()
def reset_visulization():
    for node in nodes:
        canvas.itemconfig(node.circle, fill=node_fill_color)  
    # Reset edge colors to default
    for line in lines:
        canvas.itemconfig(line.line, fill=line_color, width=1)      
    animated_closed_label['text'] = ""
    animated_path_label['text'] = ""

def calculate_algorithm():
    selected = selected_algorithm.get()
    path = []
    print(f"Selected Algorithm: {selected}\nStart Node: {start_node.get()}\nEnd Node: {end_node.get()}")
    
    if selected == "Breadth First Search (BFS)":
        path = BFS(graph, start_node.get(), end_node.get(), canvas, root, update_animated_label)
    elif selected == "Depth First Search (DFS)":
        path = DFS(graph, start_node.get(), end_node.get(), canvas, root, update_animated_label)
    elif selected == "Uniform Cost Search (UCS)":
        path = UCS(graph, start_node.get(), end_node.get(), canvas, root, update_animated_label)
    elif selected == "A Star Search (A*)":
        path = a_star_search(graph, start_node.get(), end_node.get(), canvas, root, update_animated_label)
    elif selected == "Greedy Search":
        path = greedy_search(graph, start_node.get(), end_node.get(), canvas, root, update_animated_label)

    # Animate the final path (optional, if required for highlighting after traversal)
    if path:
        animate_path(path)

def update_animated_label(visited_nodes):
    animated_closed_label['text'] = "-".join(visited_nodes)

def animate_path(path):
    animated_path = tk.StringVar()
    animated_path_label.config(textvariable=animated_path)

    def update_path(animated_path, path, index):
        """Updates the animated path at each step."""
        if selected_algorithm.get()=="Breadth First Search (BFS)" or selected_algorithm.get()=="Depth First Search (DFS)":
            node_names=path
        else:
            node_names = [node for node, _ in path]
        animated_path.set(" -> ".join(node_names[:index + 1]))  # Include the current node

    # Call `update_path` iteratively for each step in the path
    for index in range(len(path)):
        update_path(animated_path, path, index)
        animated_path_label.update()  # Refresh the label
        animated_path_label.after(500)  # Pause for visibility

# Main Application
root = tk.Tk()
root.title("Search Algorithms Simulator")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Create a PanedWindow for the resizable frames
paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

########################## Left frame ##########################
left_frame = tk.Frame(paned_window, width=screen_width // 3, height=screen_height - 80, bg=leftFrameBackground)
paned_window.add(left_frame, weight=1)

# Add Start and End Node Select Boxes
start_node_label = tk.Label(left_frame, text="Select Start Node:", bg=labelscol, font=('Arial', 17))
start_node_label.pack(anchor=tk.W, padx=10, pady=10)

# Add a select box for "Start Node"
start_node = tk.StringVar()
start_node_combobox = ttk.Combobox(left_frame, textvariable=start_node, state="readonly", width=30, font=('Arial', 15))
start_node_combobox['values'] =  node_ids
start_node_combobox.pack(anchor=tk.W, padx=10, pady=5)

# Add a label for "End Node"
end_node_label = tk.Label(left_frame, text="Select End Node:", bg=labelscol, font=('Arial', 17))
end_node_label.pack(anchor=tk.W, padx=10, pady=10)

# Add a select box for "End Node"
end_node = tk.StringVar()
end_node_combobox = ttk.Combobox(left_frame, textvariable=end_node, state="readonly", width=30, font=('Arial', 15))
end_node_combobox['values'] =  node_ids
end_node_combobox.pack(anchor=tk.W, padx=10, pady=5)

# Add a label for "Select Search Algorithm"
algorithm_label = tk.Label(left_frame, text="Select Search Algorithm:", bg=labelscol, font=('Arial', 17))
algorithm_label.pack(anchor=tk.W, padx=10, pady=10)

# Add a select box for "Search Algorithm"
algorithms = ["Breadth First Search (BFS)", "Depth First Search (DFS)", "Uniform Cost Search (UCS)", "A Star Search (A*)", "Greedy Search"]
selected_algorithm = tk.StringVar()
algorithm_combobox = ttk.Combobox(left_frame, textvariable=selected_algorithm, state="readonly", width=30, font=('Arial', 15))
algorithm_combobox['values'] = algorithms
algorithm_combobox.pack(anchor=tk.W, padx=10, pady=5)

# Set default selection
algorithm_combobox.current(0)

# Add a Calculate button
CalcBtn = tk.Button(left_frame, text="Calculate", font=('Arial', 15), command=calculate_algorithm)
CalcBtn.pack(anchor=tk.W, padx=10, pady=5)

# Add a frame for the buttons
button_frame = tk.Frame(left_frame, bg=leftFrameBackground)
button_frame.pack(anchor=tk.W, padx=10, pady=15)

# Add reset button
reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 12), command=reset)
reset_button.grid(row=0, column=0, padx=5)

# Add reset visualization button
reset_visulization_button = tk.Button(button_frame, text="Reset Visualization", font=("Arial", 12), command=reset_visulization)
reset_visulization_button.grid(row=0, column=1, padx=5)
#closed 
closed_label = tk.Label(left_frame, text="Closed: ", bg=labelscol, font=('Arial', 17))
closed_label.pack(anchor=tk.W, padx=10, pady=10)
animated_closed_label = tk.Label(left_frame, text="", bg='lightgray', font=('Arial', 15), fg='blue')
animated_closed_label.pack(anchor=tk.W, padx=10, pady=20)
#path
path_label = tk.Label(left_frame, text="Path: ", bg=labelscol, font=('Arial', 17))
path_label.pack(anchor=tk.W, padx=10, pady=10)
animated_path_label = tk.Label(left_frame, text="", bg='lightgray', font=('Arial', 15), fg='blue')
animated_path_label.pack(anchor=tk.W, padx=10, pady=20)
########################## Right frame ##########################
right_frame = tk.Frame(paned_window, width=screen_width // 1.5, height=screen_height - 80)
paned_window.add(right_frame, weight=3)

# Create a canvas and add a scrollbar in the right frame
canvas = tk.Canvas(right_frame, bg=rightFrameBackground)
scrollbar = tk.Scrollbar(right_frame, orient=tk.VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(fill=tk.BOTH, expand=True)

# Add the root node initially
add_root_node()

# Bind events for dragging
canvas.bind("<ButtonPress-1>", lambda event: on_drag_start(event, canvas))
canvas.bind("<B1-Motion>", on_drag_move)
canvas.bind("<ButtonRelease-1>", on_drag_stop)
canvas.bind("<Button-3>", lambda event: on_right_click(event, canvas))

# Bind double-click to edit node ID
canvas.bind("<Double-1>", lambda event: on_double_click(event, canvas, start_node_combobox, end_node_combobox))

root.mainloop()
