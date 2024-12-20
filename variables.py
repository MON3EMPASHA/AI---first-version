import tkinter as tk
from tkinter import ttk
# Configuration Variables (Dynamic Customization)
xroot = 500
node_radius = 15
leftFrameBackground="#1da7f8"
rightFrameBackground = "#f2f902"
labelscol="#f2f902"
node_fill_color = "white"
highlight_color = "#79c2ec"
node_outline_color = "black"
line_color = "gray"
font = ("Arial", 10, "bold")
leftFrame=700
rightFrame=700
# Global Lists
nodes = []  # List of all Nodes
lines = []  # List of all Lines

graph = {}
H_Table={}
node_ids=[]

# GUI elements
start_node_combobox = None
end_node_combobox = None
start_node = None
end_node = None