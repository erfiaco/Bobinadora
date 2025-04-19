import numpy as np

# Generamos el vector de 2000 posiciones aleatorias entre 0 y 400 (inclusive)
vector = np.random.randint(0, 401, size=2000)

# Guardar el vector como texto (por si queres verlo o usarlo desde fuera de Python)
with open("datos.txt", "w") as archivo:
    archivo.write(','.join(map(str, vector)))  # convertimos a texto separado por comas

# Otra lista cualquiera
Test = [400, 300, 400, 300, 400, 300]

# Guardar en formato binario de NumPy (mas rapido y eficiente)
np.save("vector_guardado.npy", vector)
np.save("Test.npy", Test)

