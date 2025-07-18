import tkinter as tk
from turtle import color
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import math

# Configurar la ventana
root = tk.Tk()
root.update_idletasks()
w_window = 555
h_window = 660
center_x_screen = (root.winfo_screenwidth() // 2) - (w_window // 2)
center_y_screen = (root.winfo_screenheight() // 2) - (h_window // 2)
root.geometry(f"{w_window}x{h_window}+{center_x_screen}+{center_y_screen}")
root.title("Espacio vectorial R3")
frame_principal = tk.Frame(root)
frame_principal.pack()

modo_coord = tk.StringVar(value="rect")
coord_anterior = tk.StringVar(value="rect")
unidad_ang = tk.StringVar(value="grad")


def convertir_coords(anterior, nueva):
    try:
        if nueva == "rect":
            frame_rect.grid()
            frame_esf.grid_remove()
            frame_cil.grid_remove()

            if anterior == "esf":
                r = float(entry_r.get()) if entry_r.get() != 0 else 0
                theta = float(entry_theta.get()) if entry_theta.get() != 0 else 0
                phi = float(entry_phi.get()) if entry_phi.get() != 0 else 0

                if unidad_ang.get() == "grad":
                    theta = math.radians(theta)
                    phi = math.radians(phi)

                x = r * math.sin(phi) * math.cos(theta)
                y = r * math.sin(phi) * math.sin(theta)
                z = r * math.cos(phi)
            elif anterior == "cil":
                rho = float(entry_rho.get())
                theta = float(entry_theta_cil.get())
                z = float(entry_z_cil.get())

                if unidad_ang.get() == "grad":
                    theta = math.radians(theta)

                x = rho * math.cos(theta)
                y = rho * math.sin(theta)

            entry_x.delete(0, tk.END)
            entry_x.insert(0, f"{x:.4f}")
            entry_y.delete(0, tk.END)
            entry_y.insert(0, f"{y:.4f}")
            entry_z.delete(0, tk.END)
            entry_z.insert(0, f"{z:.4f}")

            trazar_vector()
        elif nueva == "esf":
            frame_esf.grid()
            frame_rect.grid_remove()
            frame_cil.grid_remove()

            if anterior == "rect":
                x = float(entry_x.get()) if entry_x.get() != 0 else 0
                y = float(entry_y.get()) if entry_y.get() != 0 else 0
                z = float(entry_z.get()) if entry_z.get() != 0 else 0
            elif anterior == "cil":
                rho = float(entry_rho.get())
                theta_cil = float(entry_theta_cil.get())
                z = float(entry_z_cil.get())

                if unidad_ang.get() == "grad":
                    theta_cil = math.radians(theta_cil)
                x = rho * math.cos(theta_cil)
                y = rho * math.sin(theta_cil)

            r = math.sqrt(x**2 + y**2 + z**2)
            theta = math.atan2(y, x)
            phi = math.acos(z / r) if r != 0 else 0

            if unidad_ang.get() == "grad":
                theta = math.degrees(theta)
                phi = math.degrees(phi)

            entry_r.delete(0, tk.END)
            entry_r.insert(0, f"{r:.4f}")
            entry_theta.delete(0, tk.END)
            entry_theta.insert(0, f"{theta:.4f}")
            entry_phi.delete(0, tk.END)
            entry_phi.insert(0, f"{phi:.4f}")

            trazar_vector()
        elif nueva == "cil":
            frame_cil.grid()
            frame_rect.grid_remove()
            frame_esf.grid_remove()

            if anterior == "rect":
                x = float(entry_x.get()) if entry_x.get() != 0 else 0
                y = float(entry_y.get()) if entry_y.get() != 0 else 0
                z = float(entry_z.get()) if entry_z.get() != 0 else 0
            elif anterior == "esf":
                r = float(entry_r.get()) if entry_r.get() != 0 else 0
                theta = float(entry_theta.get()) if entry_theta.get() != 0 else 0
                phi = float(entry_phi.get()) if entry_phi.get() != 0 else 0

                if unidad_ang.get() == "grad":
                    theta = math.radians(theta)
                    phi = math.radians(phi)

                x = r * math.sin(phi) * math.cos(theta)
                y = r * math.sin(phi) * math.sin(theta)
                z = r * math.cos(phi)

            rho = math.sqrt(x**2 + y**2)
            theta_cil = math.atan2(y, x)
            if unidad_ang.get() == "grad":
                theta_cil = math.degrees(theta_cil)

            entry_rho.delete(0, tk.END)
            entry_rho.insert(0, f"{rho:.4f}")
            entry_theta_cil.delete(0, tk.END)
            entry_theta_cil.insert(0, f"{theta_cil:.4f}")
            entry_z_cil.delete(0, tk.END)
            entry_z_cil.insert(0, f"{z:.4f}")

            trazar_vector()
    except:
        lbl_error.config(
            text="Ocurrio un error no esperado al intentar cambiar el sistema de coordenadas."
        )


def switch_coords_frame():
    anterior = coord_anterior.get()
    nueva = modo_coord.get()

    if anterior != nueva:
        convertir_coords(anterior=anterior, nueva=nueva)

    coord_anterior.set(nueva)


# Selector coords.
frame_selector_coords = tk.LabelFrame(frame_principal, text="Sistema de coordenadas: ")
frame_selector_coords.grid(row=1, column=0, padx=10)
tk.Radiobutton(
    frame_selector_coords,
    text="Rectangulares",
    variable=modo_coord,
    value="rect",
    command=lambda: switch_coords_frame(),
).grid(row=0, column=0, padx=5)
tk.Radiobutton(
    frame_selector_coords,
    text="Esfericas",
    variable=modo_coord,
    value="esf",
    command=lambda: switch_coords_frame(),
).grid(row=0, column=1, padx=5)
tk.Radiobutton(
    frame_selector_coords,
    text="Cilindricas",
    variable=modo_coord,
    value="cil",
    command=lambda: switch_coords_frame(),
).grid(row=0, column=2, padx=5)

# Selector de unidad angular
frame_selector_ang = tk.LabelFrame(frame_principal, text="Unidad angular: ")
frame_selector_ang.grid(row=1, column=1, padx=10)
tk.Radiobutton(frame_selector_ang, text="Grados", variable=unidad_ang, value="grad").grid(row=0, column=0, padx=5)
tk.Radiobutton(frame_selector_ang, text="Radianes", variable=unidad_ang, value="rad").grid(row=0, column=1, padx=5)

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

# Frame coords. cil.
frame_cil = tk.LabelFrame(frame_principal, text="Coordenadas cilindricas")
frame_cil.grid(row=0, column=1, padx=20)

tk.Label(frame_cil, text="rho: ").grid(row=0, column=0)
entry_rho = tk.Entry(frame_cil)
entry_rho.grid(row=0, column=1)

tk.Label(frame_cil, text="theta: ").grid(row=1, column=0)
entry_theta_cil = tk.Entry(frame_cil)
entry_theta_cil.grid(row=1, column=1)

tk.Label(frame_cil, text="z: ").grid(row=2, column=0)
entry_z_cil = tk.Entry(frame_cil)
entry_z_cil.grid(row=2, column=1)

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

    ax.plot_surface(xs, ys, zs, color="cyan", alpha=0.2, edgecolor="black")


def dibujar_cilindro(origen, rho, altura):
    theta = np.linspace(0, 2 * np.pi, 30)
    z = np.linspace(0, altura, 10)
    theta, z = np.meshgrid(theta, z)

    x = rho * np.cos(theta) + origen[0]
    y = rho * np.sin(theta) + origen[1]
    z = z + origen[2]

    ax.plot_surface(x, y, z, color="cyan", alpha=0.2, edgecolor="none")


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
    elif modo_coord.get() == "cil":
        rho = float(entry_rho.get())
        theta = float(entry_theta_cil.get())
        z = float(entry_z_cil.get())

        if unidad_ang.get() == "grad":
            theta = math.radians(theta)

        x = rho * math.cos(theta)
        y = rho * math.sin(theta)
        vector = np.array([x, y, z])

        dibujar_cilindro(origen=origen_p, rho=rho, altura=z)

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


tk.Button(root, text="Generar vector", command=trazar_vector).pack(pady=5)
frame_esf.grid_remove()
frame_cil.grid_remove()

root.mainloop()
