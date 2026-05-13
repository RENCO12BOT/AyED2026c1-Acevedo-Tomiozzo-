import matplotlib
matplotlib.use("Qt5Agg")
import time
import matplotlib.pyplot as plt
import random
from radix_sort import Radix_sort # type: ignore

# Tus datos de prueba
tallas = [100, 1000, 5000]
tiempos_radix = []
tiempos_sorted = []

for n in tallas:
    lista_original = [random.randint(0, 10000) for _ in range(n)]

    # Medir tu Radix Sort
    inicio = time.time()
    instancia = Radix_sort(lista_original.copy())
    instancia.ordenar()
    tiempos_radix.append(time.time() - inicio)

    # Medir sorted()
    inicio = time.time()
    sorted(lista_original.copy())
    tiempos_sorted.append(time.time() - inicio)

# Crear gráfico
plt.plot(tallas, tiempos_radix, label="Mi Radix Sort")
plt.plot(tallas, tiempos_sorted, label="Python Sorted")

plt.xlabel("Tamaño de la lista (N)")
plt.ylabel("Tiempo (segundos)")
plt.legend()

# Guardar imagen
plt.savefig("grafico.png")

# Mostrar ventana
plt.show()