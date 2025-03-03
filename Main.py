import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Grafo_Dijkstra import grafo_de_rutas, dijkstra, posicion
from Algoritmo_A import a_estrella

G = nx.Graph()
for nodo, vecinos in grafo_de_rutas.items():
    for vecino, peso in vecinos:
        G.add_edge(nodo, vecino, weight=peso)

# Función para colorear y actualizar el grafo
def grafo_coloreado(camino, color, fig, canvas):
    fig.clf() 
    ax = fig.add_subplot(111)
    colores_nodos = [color if nodo in camino else 'skyblue' for nodo in G.nodes]
    edges = [(camino[i], camino[i + 1]) for i in range(len(camino) - 1)]
    edge_colors = [color if edge in edges or (edge[1], edge[0]) in edges else 'gray' for edge in G.edges]

    nx.draw(G, posicion, ax=ax, with_labels=True, node_size=240, node_color=colores_nodos,
            font_size=7.5, font_weight='bold', edge_color=edge_colors, width=2)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, posicion, edge_labels=labels, font_size=6, ax=ax)

    canvas.draw()

# Función para mostrar el resultado y actualizar el grafo
def mostrar_resultado():
    inicio = entrada_inicio.get().strip()
    objetivo = entrada_objetivo.get().strip()
    algoritmo = opciones_algoritmo.get()

    if inicio not in grafo_de_rutas or objetivo not in grafo_de_rutas:
        messagebox.showerror("Error", "Introduce nodos válidos")
        return

    try:
        if algoritmo == "Dijkstra":
            distancia, camino = dijkstra(grafo_de_rutas, inicio, objetivo)
            color = 'red'
        elif algoritmo == "A*":
            distancia, camino = a_estrella(grafo_de_rutas, inicio, objetivo)
            color = 'orange'

        if camino is None:
            resultado = f"No se encontró un camino desde {inicio} hasta {objetivo}"
        else:
            resultado = f"La distancia más corta desde {inicio} hasta {objetivo} es {distancia}\n"
            resultado += f"El camino más corto es: {' -> '.join(camino)}"
            actualizar_grafo(camino, color)

        text_resultado.config(state=tk.NORMAL)
        text_resultado.delete('1.0', tk.END)
        text_resultado.insert(tk.END, resultado)
        text_resultado.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Función para actualizar el grafo en la ventana separada
def actualizar_grafo(camino, color):
    global fig, canvas
    if 'grafo_ventana' not in globals() or not grafo_ventana.winfo_exists():
        crear_ventana_grafo()
    grafo_coloreado(camino, color, fig, canvas)

# Función para crear la ventana del grafo
def crear_ventana_grafo():
    global grafo_ventana, fig, canvas
    grafo_ventana = tk.Toplevel(ventana)
    grafo_ventana.title("Grafo")

    frame_grafo = ttk.Frame(grafo_ventana)
    frame_grafo.pack(fill=tk.BOTH, expand=True)

    fig, ax = plt.subplots(figsize=(14, 10))
    canvas = FigureCanvasTkAgg(fig, master=frame_grafo)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    grafo_coloreado([], 'skyblue', fig, canvas)

# Ventana principal
ventana = tk.Tk()
ventana.title("Encuentra la ruta más corta")

# Tamaño de la ventana principal
ventana.geometry("400x400")

frame = ttk.Frame(ventana, padding="20 20 20 20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Inicio", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
entrada_inicio = ttk.Entry(frame, font=('Arial', 12), width=20)
entrada_inicio.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

ttk.Label(frame, text="Objetivo", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entrada_objetivo = ttk.Entry(frame, font=('Arial', 12), width=20)
entrada_objetivo.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

# Selección de algoritmo
ttk.Label(frame, text="Algoritmo", font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
opciones_algoritmo = tk.StringVar(value="Dijkstra")
frame_algoritmo = ttk.Frame(frame)
frame_algoritmo.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
radio_dijkstra = ttk.Radiobutton(frame_algoritmo, text="Dijkstra", variable=opciones_algoritmo, value="Dijkstra")
radio_dijkstra.pack(side=tk.LEFT, padx=5)
radio_a_estrella = ttk.Radiobutton(frame_algoritmo, text="A*", variable=opciones_algoritmo, value="A*")
radio_a_estrella.pack(side=tk.LEFT, padx=5)

boton_calcular = ttk.Button(frame, text="Calcular", command=mostrar_resultado)
boton_calcular.grid(row=3, column=0, columnspan=2, pady=20)

# Frame y scrollbar para el resultado
frame_resultado = ttk.Frame(frame)
frame_resultado.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

scrollbar = ttk.Scrollbar(frame_resultado, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_resultado = tk.Text(frame_resultado, height=8, width=40, wrap=tk.WORD, yscrollcommand=scrollbar.set, state=tk.DISABLED)
text_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=text_resultado.yview)

# Estilo de los botones
style = ttk.Style()
style.configure('TButton', font=('Arial', 10))

ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(0, weight=1)

ventana.mainloop()
