import tkinter as tk
from math import cos, sin, radians, sqrt

# Global variable to store drawn hexagons
drawn_hexagons = []

# Function to draw a hexagon grid based on user input
def draw_hexagon_grid(motif_size, cell_radius, global_frequency):
    global drawn_hexagons
    canvas = tk._default_root.draw_canvas
    # Calculate canvas dimensions
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    hex_height = sqrt(3) * cell_radius
    hex_width = 2 * cell_radius
    
    # Calculate the starting point to center the hexagons
    start_x = width / 2 - (motif_size / 2 * hex_width * 0.75)
    start_y = height / 2 - (motif_size / 2 * hex_height)

    # Draw hexagons centered in the canvas
    for row in range(motif_size):
        for col in range(motif_size):
            if len(drawn_hexagons) < motif_size:  # Ensure only the number of cells equal to motif_size are drawn
                x_offset = start_x + col * hex_width * 0.75
                y_offset = start_y + row * hex_height + (col % 2) * (hex_height / 2)
                hexagon = create_hexagon(canvas, x_offset, y_offset, cell_radius)
                drawn_hexagons.append(hexagon)
                # Place frequency labels
                place_frequency_labels(canvas, x_offset, y_offset, global_frequency, motif_size, len(drawn_hexagons) - 1)
    highlight_hexagons(canvas, drawn_hexagons)

# Function to create a single hexagon
def create_hexagon(canvas, x_center, y_center, radius):
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = radians(angle_deg)
        x = x_center + radius * cos(angle_rad)
        y = y_center + radius * sin(angle_rad)
        points.append((x, y))
    hexagon = canvas.create_polygon(points, outline='black', fill='white', width=2)
    return hexagon

# Function to highlight hexagons (can be customized further)
def highlight_hexagons(canvas, hexagons):
    for hexagon in hexagons:
        canvas.itemconfig(hexagon, outline='blue', width=3)

# Function to place multiple frequency labels inside a hexagon
def place_frequency_labels(canvas, x_center, y_center, total_frequencies, motif_size, index):
    frequencies_per_cell = total_frequencies // motif_size
    extra_frequencies = total_frequencies % motif_size
    frequencies = [f"F{index * frequencies_per_cell + i + 1}" for i in range(frequencies_per_cell)]
    
    # Add extra frequencies if applicable
    if index < extra_frequencies:
        frequencies.append(f"F{motif_size * frequencies_per_cell + index + 1}")
    
    # Display the frequencies inside the hexagon as a comma-separated list
    frequencies_str = ",".join(frequencies)
    canvas.create_text(x_center, y_center, text=frequencies_str, fill="black", font=("Arial", 12, "bold"))

# Function to reuse the existing hexagon grid representation
def reuse_function(motifs):
    global drawn_hexagons
    canvas = tk._default_root.draw_canvas
    # Calculate canvas dimensions
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    hex_height = sqrt(3) * 50  # Assuming cell_radius is 50 for consistency
    hex_width = 2 * 50
    
    # Calculate the starting point to center the hexagons
    start_x = width / 2 - (motifs / 2 * hex_width * 0.75)
    start_y = height / 2 - (motifs / 2 * hex_height)
    
    # Draw additional hexagons if motifs > 1
    if motifs > 1:
        for _ in range(motifs - 1):
            for hexagon in drawn_hexagons:
                x, y = canvas.coords(hexagon)[0], canvas.coords(hexagon)[1]
                hexagon = create_hexagon(canvas, x, y, 50)
                # Place frequency labels
                place_frequency_labels(canvas, x, y, 8, motifs, len(drawn_hexagons) - 1)
    highlight_hexagons(canvas, drawn_hexagons)
