import time
import matplotlib.pyplot as plt
import random
from ayedfiuner.algoritmos.radix_sort import Radix_sort
from ayedfiuner.algoritmos.quicksort import Quicksort
from ayedfiuner.algoritmos.burbuja import Burbuja

# Tus datos de prueba
tallas = [100, 500, 1000, 2000, 3000, 5000]
tiempos_radix = []
tiempos_quick = []
tiempos_burbuja = []
tiempos_sorted = []

for n in tallas:
    lista_original = [random.randint(0, 10000) for _ in range(n)]

    # Medir tu Radix Sort
    inicio = time.time()
    instancia = Radix_sort(lista_original.copy())
    instancia.ordenar()
    tiempos_radix.append((time.time() - inicio) * 1000)

    # Medir tu Quicksort
    inicio = time.time()
    instancia = Quicksort(lista_original.copy())
    instancia.ordenar()
    tiempos_quick.append((time.time() - inicio) * 1000)

    # Medir tu Burbuja
    inicio = time.time()
    instancia = Burbuja(lista_original.copy())
    instancia.ordenar_lista()
    tiempos_burbuja.append((time.time() - inicio) * 1000)

    # Medir sorted()
    inicio = time.time()
    sorted(lista_original.copy())
    tiempos_sorted.append((time.time() - inicio) * 1000)

# Crear gráfico
plt.plot(tallas, tiempos_radix,   label="Radix Sort")
plt.plot(tallas, tiempos_quick,   label="Quicksort")
plt.plot(tallas, tiempos_burbuja, label="Burbuja")
plt.plot(tallas, tiempos_sorted,  label="Python Sorted")

plt.xlabel("Tamaño de la lista (N)")
plt.ylabel("Tiempo (milisegundos)")
plt.legend()

# Guardar imagen
plt.savefig("grafico_todos.png")
# Mostrar gráfico
plt.show()
# Cerrar gráfico
plt.close()
