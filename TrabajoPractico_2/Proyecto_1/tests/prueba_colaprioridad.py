"""
Prueba de uso de ColaPrioridad.
Cubre: insertar, extraer, ver_proximo, ver_todos, esta_vacia, tamano,
       orden por prioridad, empate FIFO, len, iter, manejo de errores.
"""

from ayedfiuner.estructuras.Cola_Prioridad import ColaPrioridad

SEP = "=" * 45


# -----------------------------------------------
# 1. Distintas prioridades — orden de atención
# -----------------------------------------------
print(SEP)
print("1. DISTINTAS PRIORIDADES")
print(SEP)

cola = ColaPrioridad()
cola.insertar(3, "riesgo bajo")
cola.insertar(1, "riesgo crítico")
cola.insertar(2, "riesgo moderado")

print("Tamaño:", cola.tamano())           # 3
print("Próximo (sin extraer):", cola.ver_proximo())  # riesgo crítico
print("Orden esperado: crítico → moderado → bajo")
print("Sale:", cola.extraer())   # riesgo crítico
print("Sale:", cola.extraer())   # riesgo moderado
print("Sale:", cola.extraer())   # riesgo bajo
print("Vacía:", cola.esta_vacia())  # True


# -----------------------------------------------
# 2. Empate de prioridad — FIFO
# -----------------------------------------------
print()
print(SEP)
print("2. EMPATE FIFO (misma prioridad)")
print(SEP)

cola2 = ColaPrioridad()
cola2.insertar(2, "llegó primero")
cola2.insertar(2, "llegó segundo")
cola2.insertar(2, "llegó tercero")

print("Orden esperado: primero → segundo → tercero")
print("Sale:", cola2.extraer())   # llegó primero
print("Sale:", cola2.extraer())   # llegó segundo
print("Sale:", cola2.extraer())   # llegó tercero


# -----------------------------------------------
# 3. Cola vacía
# -----------------------------------------------
print()
print(SEP)
print("3. COLA VACÍA")
print(SEP)

cola3 = ColaPrioridad()
print("Vacía:", cola3.esta_vacia())       # True
print("Tamaño:", cola3.tamano())          # 0
print("extraer():", cola3.extraer())      # None
print("ver_proximo():", cola3.ver_proximo())  # None
print("len():", len(cola3))              # 0


# -----------------------------------------------
# 4. ver_todos — sin modificar la cola
# -----------------------------------------------
print()
print(SEP)
print("4. VER_TODOS (no modifica la cola)")
print(SEP)

cola4 = ColaPrioridad()
cola4.insertar(3, "C")
cola4.insertar(1, "A")
cola4.insertar(2, "B")

print("ver_todos():", cola4.ver_todos())  # ['A', 'B', 'C']
print("Tamaño después de ver_todos:", cola4.tamano())  # sigue siendo 3


# -----------------------------------------------
# 5. Iterar con for
# -----------------------------------------------
print()
print(SEP)
print("5. ITERAR CON FOR")
print(SEP)

cola5 = ColaPrioridad()
cola5.insertar(2, "segundo")
cola5.insertar(1, "primero")
cola5.insertar(3, "tercero")

print("Iterando en orden de prioridad:")
for item in cola5:
    print(" ", item)


# -----------------------------------------------
# 6. Un solo elemento
# -----------------------------------------------
print()
print(SEP)
print("6. UN SOLO ELEMENTO")
print(SEP)

cola6 = ColaPrioridad()
cola6.insertar(1, "único")
print("ver_proximo:", cola6.ver_proximo())  # único
print("extraer:", cola6.extraer())          # único
print("vacía:", cola6.esta_vacia())         # True


# -----------------------------------------------
# 7. Datos de distinto tipo (genérica)
# -----------------------------------------------
print()
print(SEP)
print("7. GENÉRICA — distintos tipos de dato")
print(SEP)

cola7 = ColaPrioridad()
cola7.insertar(1, {"nombre": "tarea urgente", "id": 101})
cola7.insertar(3, "tarea baja")
cola7.insertar(2, 42)

print("Extrayendo objetos de distinto tipo:")
print(" ", cola7.extraer())   # dict
print(" ", cola7.extraer())   # int
print(" ", cola7.extraer())   # str


# -----------------------------------------------
# 8. Manejo de errores esperados
# -----------------------------------------------
print()
print(SEP)
print("8. MANEJO DE ERRORES")
print(SEP)

cola8 = ColaPrioridad()

try:
    cola8.insertar("alta", "dato")
except TypeError as e:
    print("prioridad str →", e)

try:
    cola8.insertar(-1, "dato")
except ValueError as e:
    print("prioridad negativa →", e)

try:
    cola8.insertar(1, None)
except ValueError as e:
    print("dato None →", e)

print()
print("Pruebas de ColaPrioridad finalizadas.")