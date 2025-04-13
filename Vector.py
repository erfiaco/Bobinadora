import numpy as np

# Generamos el vector de 5000 posiciones aleatorias entre 0 y 400 (inclusive)
vector = np.random.randint(0, 401, size=5000)

Test = [400, 300, 400, 300, 400, 300]

np.save("vector_guardado.npy", vector)
np.save("Test.npy", Test)
