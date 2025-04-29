import numpy as np
import matplotlib.pyplot as plt

# Cargar el vector desde un archivo .npy
vector = np.load("vector_guardado.npy")  # Reemplaza con el nombre real del archivo

#Verifica cuantos elementos tiene
print(f"Vector cargado con {len(vector)} elementos")

# Crear los indices como eje X
indices = np.arange(len(vector))

# Crear grafico de dispersion
plt.figure(figsize=(10, 5))
plt.scatter(indices, vector, s=10, c='blue', label='Puntos del vector')  # s = tamano de los puntos
plt.xlabel('Indice')
plt.ylabel('Valor')
plt.title('Grafico de dispersion del vector')
plt.grid(True)
plt.legend()

# Guardar el graficoo como imagen PNG
plt.savefig("grafico_vector_disperso.png")
print("Grafico guardado como grafico_vector_disperso.png")
