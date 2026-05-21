import matplotlib
import matplotlib.pyplot as plt
import time
import random
from ayedfiuner.algoritmos.quicksort import Quicksort


tallas = [100, 500, 1000, 2000, 3000, 5000, 7500, 10000]
tiempos_quick = []
 
for n in tallas:
    lista_original = [random.randint(0, 10000) for _ in range(n)]
    inicio = time.time()
    Quicksort(lista_original.copy()).ordenar()
    tiempos_quick.append(time.time() - inicio)
 
plt.figure(figsize=(8, 5))
plt.plot(tallas, tiempos_quick, 'bs-', linewidth=2, markersize=6, label='Quicksort O(n log n)')
plt.title('Rendimiento Quicksort — O(n log n)', fontsize=13, fontweight='bold')
plt.xlabel('Tamaño de la lista (N)')
plt.ylabel('Tiempo (segundos)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('grafico_quicksort.png', dpi=150)
plt.show()
plt.close()

print("Guardado: grafico_quicksort.png")