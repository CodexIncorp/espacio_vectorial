import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

#Que escale para mostrar el nuevo origen...

# Configurar la ventana
root = tk.Tk()
root.update_idletasks()
wdth = root.winfo_width()
hght = root.winfo_height()
w = (root.winfo_screenwidth() // 2) - (wdth // 2)
h = (root.winfo_screenheight() // 2) - (hght // 2)
root.geometry(f"+{w}+{h}")
root.title("Espacio vectorial R3")
frame = tk.Frame(root)
frame.pack(pady=10)

# Instanciar gráfico
fig = plt.figure()
ax = plt.axes(projection="3d")
ax.set_title("Espacio vectorial", color="r")

# Establecer visualmente el origen (0, 0, 0)
ax.scatter(0, 0, 0, color="black", s=30)
ax.text(0, 0, 0, "O", fontsize=8, color="black")

# Crear canvas vacío
canvas_fig = FigureCanvasTkAgg(fig, master=root)
canvas_fig.get_tk_widget().pack()


def dibujar_prisma_rect():
    """
    Dibuja el prisma rectangular que corresponde a las coordenadas del vector
    """

    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())
    except Exception:
        lbl_error.config(text="Ingrese numeros validos.")
        return

    lbl_error.config(text="")

    try:
        ox = float(entry_ox.get()) if entry_ox.get() else 0
        oy = float(entry_oy.get()) if entry_oy.get() else 0
        oz = float(entry_oz.get()) if entry_oz.get() else 0
    except Exception:
        lbl_error.config(text="Origen invalido.")

    origen_p = [ox, oy, oz]
    vector = np.array([x, y, z])
    vc_final = origen_p + vector

    # Reconfigurar gráfico
    ax.clear()

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
    limite = np.max(np.abs(vector)) + 1
    ax.set_xlim([-limite, limite])
    ax.set_ylim([-limite, limite])
    ax.set_zlim([-limite, limite])
    ax.quiver(*origen_p, *vector, color="b", arrow_length_ratio=0.1)

    vertices = [
        origen_p,
        [vc_final[0], origen_p[1], origen_p[2]],
        [vc_final[0], vc_final[1], origen_p[2]],
        [origen_p[0], vc_final[1], origen_p[2]],
        [origen_p[0], origen_p[1], vc_final[2]],
        [vc_final[0], origen_p[1], vc_final[2]],
        [vc_final[0], vc_final[1], vc_final[2]],
        [origen_p[0], vc_final[1], vc_final[2]],
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

    # Mostrar en el canvas
    canvas_fig.draw()


# Inputs para definir el origen
frame_o = tk.LabelFrame(frame, text="Coordenadas del origen")
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


# Inputs para x, y, z
frame_vc = tk.LabelFrame(frame, text="Coordenadas del vector")
frame_vc.grid(row=0, column=1, padx=20)

tk.Label(frame_vc, text="x: ").grid(row=0, column=0)
entry_x = tk.Entry(frame_vc)
entry_x.grid(row=0, column=1)

tk.Label(frame_vc, text="y: ").grid(row=1, column=0)
entry_y = tk.Entry(frame_vc)
entry_y.grid(row=1, column=1)

tk.Label(frame_vc, text="z: ").grid(row=2, column=0)
entry_z = tk.Entry(frame_vc)
entry_z.grid(row=2, column=1)

tk.Button(root, text="Generar vector", command=dibujar_prisma_rect).pack(pady=5)

lbl_error = tk.Label(root, text="", fg="red")
lbl_error.pack()

root.mainloop()
