import matplotlib
import matplotlib.pyplot as plt
import time
import random
from ayedfiuner.algoritmos.burbuja import Burbuja
 
tallas = [100, 500, 1000, 2000, 3000, 5000, 7500, 10000]
tiempos_burbuja = []
 
for n in tallas:
    lista_original = [random.randint(0, 10000) for _ in range(n)]
    inicio = time.time()
    Burbuja(lista_original.copy()).ordenar_lista()
    tiempos_burbuja.append(time.time() - inicio)
 
plt.figure(figsize=(8, 5))
plt.plot(tallas, tiempos_burbuja, 'ro-', linewidth=2, markersize=6, label='Burbuja O(n²)')
plt.title('Rendimiento Burbuja — O(n²)', fontsize=13, fontweight='bold')
plt.xlabel('Tamaño de la lista (N)')
plt.ylabel('Tiempo (segundos)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('grafico_burbuja.png', dpi=150)
plt.show()
plt.close()

print("Guardado: grafico_burbuja.png")