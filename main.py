import tkinter as tk
from tkinter import ttk
from math import cos, sin, radians, sqrt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import string
from motif import draw_hexagon_grid

# Global variables to store user input
global_motif_size = None
global_frequency = None

# Function to display a popup for data input
def show_popup():
    popup = tk.Toplevel()
    popup.title("Formulaire")
    popup.geometry("400x400")
    popup.configure(bg='#f0f0f0')
    
    # Adding a frame with rounded corners
    content_frame = tk.Frame(popup, bg='#f0f0f0', bd=2, relief="groove", padx=20, pady=20)
    content_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Adding input fields and labels with padding
    ttk.Label(content_frame, text="Taille d'un motif:", font=('Arial', 12), background='#f0f0f0').grid(row=0, column=0, pady=10, sticky='w')
    motif_size_entry = ttk.Entry(content_frame, font=('Arial', 12))
    motif_size_entry.grid(row=0, column=1, pady=10, padx=10)
    
    ttk.Label(content_frame, text="Rayon d'une cellule:", font=('Arial', 12), background='#f0f0f0').grid(row=1, column=0, pady=10, sticky='w')
    cell_radius_entry = ttk.Entry(content_frame, font=('Arial', 12))
    cell_radius_entry.grid(row=1, column=1, pady=10, padx=10)
    
    ttk.Label(content_frame, text="Nombre de fréquences:", font=('Arial', 12), background='#f0f0f0').grid(row=2, column=0, pady=10, sticky='w')
    frequency_entry = ttk.Entry(content_frame, font=('Arial', 12))
    frequency_entry.grid(row=2, column=1, pady=10, padx=10)

    ttk.Label(content_frame, text="Nombre de répétitions:", font=('Arial', 12), background='#f0f0f0').grid(row=3, column=0, pady=10, sticky='w')
    repetitions_entry = ttk.Entry(content_frame, font=('Arial', 12))
    repetitions_entry.grid(row=3, column=1, pady=10, padx=10)
    
    # Submit button
    submit_button = ttk.Button(content_frame, text="Soumettre", command=lambda: submit_form(popup, motif_size_entry, cell_radius_entry, frequency_entry,repetitions_entry), style='TButton')
    submit_button.grid(row=4, column=0, columnspan=2, pady=20)

# Function to process submitted data
def submit_form(popup, motif_size_entry, cell_radius_entry, frequency_entry,repetitions_entry):
    global global_motif_size, global_frequency
    global_motif_size = int(motif_size_entry.get())
    cell_radius = int(cell_radius_entry.get())
    global_frequency = int(frequency_entry.get())
    global_repetitions = int(repetitions_entry.get())
    print(f"Taille d'un motif: {global_motif_size}")
    print(f"Rayon d'une cellule: {cell_radius}")
    print(f"Nombre de fréquences: {global_frequency}")
    print(f"Nombre de répétitions: {global_repetitions}")
    popup.destroy()
    draw_hexagon_grid(global_motif_size, cell_radius,global_frequency)

# Function to generate the frequency allocation report
def generate_frequency_report():
    global global_motif_size, global_frequency
    filename = "rapport_repartition_frequences.pdf"
    frequency = global_frequency
    motif_size = global_motif_size
    frequencies_per_motif = frequency // motif_size
    extra_frequencies = frequency % motif_size
    alphabet = string.ascii_uppercase
    num_combinations = motif_size if motif_size <= 26 else 26
    combinations = [alphabet[i] for i in range(num_combinations)]
    frequency_combinations = {}
    for i, comb in enumerate(combinations):
        frequency_combinations[comb] = [f"F{i * frequencies_per_motif + j + 1}" for j in range(frequencies_per_motif)]
    for i in range(extra_frequencies):
        frequency_combinations[combinations[i]].append(f"F{num_combinations * frequencies_per_motif + i + 1}")
    allocation = []
    for i in range(motif_size):
        allocation.append(combinations[i % len(combinations)])
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    title = Paragraph("Rapport de Répartition des Fréquences dans les Réseaux Mobiles", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    introduction = Paragraph("Ce rapport présente le processus appliqué pour répartir les fréquences dans les réseaux mobiles.", styles['Normal'])
    elements.append(introduction)
    elements.append(Spacer(1, 12))
    input_data = Paragraph(f"""
        <b>Données d'entrée :</b><br/>
        Nombre de fréquences : {frequency}<br/>
        Taille du motif (N) : {motif_size}<br/>
        Nombre de fréquences par motif : {frequencies_per_motif}<br/>
        Fréquences supplémentaires : {extra_frequencies}<br/>
    """, styles['Normal'])
    elements.append(input_data)
    elements.append(Spacer(1, 12))
    comb_title = Paragraph("<b>Combinaisons de fréquences :</b>", styles['Normal'])
    elements.append(comb_title)
    comb_data = [["Combinaison", "Fréquences"]]
    for comb, freqs in frequency_combinations.items():
        comb_data.append([comb, ", ".join(freqs)])
    comb_table = Table(comb_data)
    comb_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(comb_table)
    elements.append(Spacer(1, 12))
    allocation_title = Paragraph("<b>Répartition des combinaisons dans le motif :</b>", styles['Normal'])
    elements.append(allocation_title)
    allocation_data = [["Cellule", "Combinaison"]]
    for i, alloc in enumerate(allocation):
        allocation_data.append([f"Cellule {i+1}", alloc])
    allocation_table = Table(allocation_data)
    allocation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(allocation_table)
    elements.append(Spacer(1, 12))
    conclusion = Paragraph("La répartition des fréquences a été réalisée avec succès en utilisant les combinaisons et la disposition décrites ci-dessus.", styles['Normal'])
    elements.append(conclusion)
    doc.build(elements)

# Function to create a rounded rectangle
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Function to create a rounded button
def create_rounded_button(canvas, x, y, width, height, text, command):
    radius = 20
    button = create_rounded_rectangle(canvas, x, y, x + width, y + height, radius, fill="#4CAF50", outline="")
    label = canvas.create_text(x + width / 2, y + height / 2, text=text, fill="white", font=("Arial", 12, "bold"))
    canvas.tag_bind(button, "<Button-1>", lambda e: command())
    canvas.tag_bind(label, "<Button-1>", lambda e: command())
    return button, label

# Function to create the main window with a side navigation
def create_main_window():
    root = tk.Tk()
    root.title("Hexagon Grid Application")
    root.geometry("1200x800")
    
    # Main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill='both', expand=True)
    
    # Side navigation frame
    sidenav_frame = tk.Frame(main_frame, width=200, bg='#333')
    sidenav_frame.pack(side='left', fill='y')
    
    # Content frame
    content_frame = tk.Frame(main_frame, bg='#f0f0f0')
    content_frame.pack(side='right', fill='both', expand=True)
    
    # Side navigation buttons
    canvas = tk.Canvas(sidenav_frame, width=200, height=800, bg='#333', highlightthickness=0)
    canvas.pack(fill='both', expand=True)
    
    # Button for data input popup
    button1, label1 = create_rounded_button(canvas, 10, 20, 180, 50, "Saisie des données", show_popup)
    
    # Button for generating report
    button2, label2 = create_rounded_button(canvas, 10, 90, 180, 50, "Générer le rapport", generate_frequency_report)
    
    # Button for reuse function
    button3, label3 = create_rounded_button(canvas, 10, 160, 180, 50, "Réutilisation", reuse_function)
    
    # Drawing canvas
    draw_canvas = tk.Canvas(content_frame, bg='white')
    draw_canvas.pack(fill='both', expand=True)
    root.draw_canvas = draw_canvas
    
    root.mainloop()

# Function to handle the "Réutilisation" button click
def reuse_function():
    # Replace with your desired functionality
    print("Action du bouton Réutilisation")
    # Add your code here for handling the reuse functionality

# Main function to run the application
if __name__ == "__main__":
    create_main_window()
