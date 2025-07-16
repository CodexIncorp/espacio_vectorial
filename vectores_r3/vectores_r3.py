import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Solicitar coordenadas del vector
coords = input("Ingrese el vector en la forma 'x,y,z': ")

# Procesar cadena para obtener valores
try:
    vector = [float(valor.strip()) for valor in coords.split(",")]
    if len(vector) != 3:
        raise ValueError("Ingrese exactamente 3 valores separados por comas (,)")
except Exception as e:
    print(f"Entrada invalida:{e}")

origen = [0, 0, 0]

# Instanciar gráfico
ax = plt.axes(projection="3d")

# Establecer título
ax.set_title("Espacio vectorial", color="r")

# Etiquetar ejes
ax.set_xlabel("X", color="r")
ax.set_ylabel("Y", color="g")
ax.set_zlabel("Z", color="b")

# Establecer visualmente el origen (0, 0, 0)
ax.scatter(0, 0, 0, color="black", s=40)

# Ajustar límites (escala automática)
limite = np.max(np.abs(vector)) + 1
ax.set_xlim([0, limite])
ax.set_ylim([0, limite])
ax.set_zlim([0, limite])


def trazar_prisma_rect():
    """
    Dibuja el prisma rectangular que corresponde a las coordenadas del vector
    """
    x, y, z = vector
    vertices = [
        [0, 0, 0],  # Origen (puede ser establecido por el usuario)
        [x, 0, 0],
        [x, y, 0],
        [0, y, 0],
        [0, 0, z],
        [x, 0, z],
        [x, y, z],
        [0, y, z],
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


# Trazar vectores
ax.quiver(*origen, *vector, color="b", arrow_length_ratio=0.1)
trazar_prisma_rect()

# Mostrar gráfico
plt.show()
