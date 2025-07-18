import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import math

# Configurar la ventana
root = tk.Tk()
root.update_idletasks()
w_window = 555
h_window = 650
center_x_screen = (root.winfo_screenwidth() // 2) - (w_window // 2)
center_y_screen = (root.winfo_screenheight() // 2) - (h_window // 2)
root.geometry(f"{w_window}x{h_window}+{center_x_screen}+{center_y_screen}")
root.title("Espacio vectorial R3")
frame_principal = tk.Frame(root)
frame_principal.pack()

# Selector coords.
modo_coord = tk.StringVar(value="rect")
frame_selector = tk.Frame(root)
frame_selector.pack(pady=5)


def switch_coords_frame():
    if modo_coord.get() == "rect":
        frame_rect.grid()
        frame_esf.grid_remove()
    elif modo_coord.get() == "esf":
        frame_esf.grid()
        frame_rect.grid_remove()


tk.Label(frame_selector, text="Sistema de coordenadas: ").pack(side=tk.LEFT)
tk.Radiobutton(
    frame_selector,
    text="Rectangulares",
    variable=modo_coord,
    value="rect",
    command=switch_coords_frame,
).pack(side=tk.LEFT)
tk.Radiobutton(
    frame_selector,
    text="Esfericas",
    variable=modo_coord,
    value="esf",
    command=switch_coords_frame,
).pack(side=tk.LEFT)

# Selector de unidad angular
unidad_ang = tk.StringVar(value="grad")
tk.Label(frame_selector, text="Unidad angular:").pack(side=tk.LEFT)
tk.Radiobutton(frame_selector, text="Grados", variable=unidad_ang, value="grad").pack(
    side=tk.LEFT
)
tk.Radiobutton(frame_selector, text="Radianes", variable=unidad_ang, value="rad").pack(
    side=tk.LEFT
)

# Frame origen personalizado
frame_o = tk.LabelFrame(frame_principal, text="Coordenadas de origen del vector")
frame_o.grid(row=0, column=0, padx=20)

tk.Label(frame_o, text="Ox: ").grid(row=0, column=0)
entry_ox = tk.Entry(frame_o)
entry_ox.grid(row=0, column=1)

tk.Label(frame_o, text="Oy: ").grid(row=1, column=0)
entry_oy = tk.Entry(frame_o)
entry_oy.grid(row=1, column=1)

tk.Label(frame_o, text="Oz: ").grid(row=2, column=0)
entry_oz = tk.Entry(frame_o)
entry_oz.grid(row=2, column=1)

# Frame coords. rect.
frame_rect = tk.LabelFrame(frame_principal, text="Coordenadas rectangulares")
frame_rect.grid(row=0, column=1, padx=20)

tk.Label(frame_rect, text="x: ").grid(row=0, column=0)
entry_x = tk.Entry(frame_rect)
entry_x.grid(row=0, column=1)

tk.Label(frame_rect, text="y: ").grid(row=1, column=0)
entry_y = tk.Entry(frame_rect)
entry_y.grid(row=1, column=1)

tk.Label(frame_rect, text="z: ").grid(row=2, column=0)
entry_z = tk.Entry(frame_rect)
entry_z.grid(row=2, column=1)

# Frame coords. esf.
frame_esf = tk.LabelFrame(frame_principal, text="Coordenadas esfericas")
frame_esf.grid(row=0, column=1, padx=20)

tk.Label(frame_esf, text="r (radio): ").grid(row=0, column=0)
entry_r = tk.Entry(frame_esf)
entry_r.grid(row=0, column=1)

tk.Label(frame_esf, text="theta: ").grid(row=1, column=0)
entry_theta = tk.Entry(frame_esf)
entry_theta.grid(row=1, column=1)

tk.Label(frame_esf, text="phi: ").grid(row=2, column=0)
entry_phi = tk.Entry(frame_esf)
entry_phi.grid(row=2, column=1)

# Etiqueta de error
lbl_error = tk.Label(root, text="", fg="red")
lbl_error.pack()

# Instanciar gráfico
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_title("Espacio vectorial", color="r")

# Establecer visualmente el origen (0, 0, 0)
ax.scatter(0, 0, 0, color="black", s=30)
ax.text(0, 0, 0, "O", fontsize=8, color="black")

# Crear canvas vacío
canvas_fig = FigureCanvasTkAgg(fig, master=root)
canvas_fig.get_tk_widget().pack()
switch_coords_frame()


def dibujar_prisma_rect(origen_p, pf_vector):
    """Dibuja el prisma rectangular que corresponde a las coordenadas del vector"""

    vertices = [
        origen_p,
        [pf_vector[0], origen_p[1], origen_p[2]],
        [pf_vector[0], pf_vector[1], origen_p[2]],
        [origen_p[0], pf_vector[1], origen_p[2]],
        [origen_p[0], origen_p[1], pf_vector[2]],
        [pf_vector[0], origen_p[1], pf_vector[2]],
        [pf_vector[0], pf_vector[1], pf_vector[2]],
        [origen_p[0], pf_vector[1], pf_vector[2]],
    ]

    caras = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Base inferior
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Base superior
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # Cara frontal
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # Cara posterior
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # Cara derecha
        [vertices[3], vertices[0], vertices[4], vertices[7]],  # Cara izquierda
    ]

    # Dibujar el prisma
    prisma = Poly3DCollection(caras, alpha=0.2, facecolors="cyan", edgecolor="black")
    ax.add_collection3d(prisma)


def dibujar_esfera(origen, vector):
    """Dibuja una esfera correspondiente a las coords. proporcionadas; en relacion al vector graficado."""

    radio = np.linalg.norm(vector)

    # Genera una malla de coordenadas angulares para construir la superficie de la esfera
    #'j' indica que quiero un número determinado de puntos sobre la superficie, en lugar de uno fijo
    # 0 : 2 * np.pi : Nj divide el angulo theta (horizontal) en 'N' pasos; divide el intervalo 0-360 en 'N' pasos uniformes
    # 0 : np.pi : Nj divide el angulo phi (vertical) en 'N' pasos; divide el intervalo 0-180 en 'N' pasos uniformes
    u, v = np.mgrid[0 : 2 * np.pi : 60j, 0 : np.pi : 60j]

    # Se transforma la malla a coords. cartesianas para generar todos los puntos de la esfera
    xs = radio * np.cos(u) * np.sin(v) + origen[0]
    ys = radio * np.sin(u) * np.sin(v) + origen[1]
    zs = radio * np.cos(v) + origen[2]

    entry_x = xs
    ax.plot_surface(xs, ys, zs, color="cyan", alpha=0.1, edgecolor="black")


def trazar_vector():
    # Reconfigurar gráfico
    ax.clear()

    try:
        ox = float(entry_ox.get()) if entry_ox.get() else 0
        oy = float(entry_oy.get()) if entry_oy.get() else 0
        oz = float(entry_oz.get()) if entry_oz.get() else 0
    except Exception:
        lbl_error.config(text="Origen invalido.")

    origen_p = [ox, oy, oz]

    if modo_coord.get() == "rect":
        try:
            x = float(entry_x.get())
            y = float(entry_y.get())
            z = float(entry_z.get())
        except Exception:
            lbl_error.config(text="Ingrese numeros validos.")
            return

        vector = np.array([x, y, z])
        pf_vector = origen_p + vector
        dibujar_prisma_rect(origen_p=origen_p, pf_vector=pf_vector)
    elif modo_coord.get() == "esf":
        r = float(entry_r.get())
        theta = float(entry_theta.get())
        phi = float(entry_phi.get())

        if unidad_ang.get() == "grad":
            theta = math.radians(theta)
            phi = math.radians(phi)

        x = r * math.sin(phi) * math.cos(theta) + origen_p[0]
        y = r * math.sin(phi) * math.sin(theta) + origen_p[1]
        z = r * math.cos(phi) + origen_p[2]

        vector = np.array([x, y, z])

        dibujar_esfera(origen=origen_p, vector=vector)

    lbl_error.config(text="")

    # Establecer visualmente el origen (0, 0, 0)
    ax.scatter(0, 0, 0, color="black", s=30)
    ax.text(0, 0, 0, "O", fontsize=8, color="black")

    ax.scatter(*origen_p, color="blue", s=30)
    ax.text(*origen_p, "P", fontsize=8, color="blue")

    # Etiquetar ejes
    ax.set_xlabel("X", color="r")
    ax.set_ylabel("Y", color="g")
    ax.set_zlabel("Z", color="b")

    # Ajustar límites (escala automática)
    limite = np.max(np.abs(vector)) + np.max(np.abs(origen_p)) + 1
    ax.set_xlim([-limite, limite])
    ax.set_ylim([-limite, limite])
    ax.set_zlim([-limite, limite])
    ax.quiver(*origen_p, *vector, color="b", arrow_length_ratio=0.1)

    # Mostrar en el canvas
    canvas_fig.draw()


def dibujar_cilindro():
    # Otro algo...
    hc = 1


tk.Button(root, text="Generar vector", command=trazar_vector).pack(pady=5)

root.mainloop()
