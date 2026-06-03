"""
Prueba de uso del MonticuloBinario.
Cubre: insertar, eliminarMin, construirMonticulo, esta_vacio, tamano,
       ver_lista_interna, orden correcto del heap, manejo de errores.
"""

from ayedfiuner.estructuras.monticulo_binario import MonticuloBinario

SEP = "=" * 45


# -----------------------------------------------
# 1. Insertar y extraer en orden creciente
# -----------------------------------------------
print(SEP)
print("1. INSERTAR Y EXTRAER (orden mínimo)")
print(SEP)

m = MonticuloBinario()
for valor in [5, 2, 8, 1, 4, 9, 3]:
    m.insertar(valor)

print("Lista interna (heap):", m.ver_lista_interna())
print("Extracciones en orden esperado: 1, 2, 3, 4, 5, 8, 9")
extraidos = []
while not m.esta_vacio():
    extraidos.append(m.eliminarMin())
print("Resultado:", extraidos)


# -----------------------------------------------
# 2. Un solo elemento
# -----------------------------------------------
print()
print(SEP)
print("2. UN SOLO ELEMENTO")
print(SEP)

m2 = MonticuloBinario()
m2.insertar(42)
print("Tamaño:", m2.tamano())            # 1
print("Mínimo:", m2.eliminarMin())       # 42
print("Vacío después:", m2.esta_vacio()) # True


# -----------------------------------------------
# 3. Elementos duplicados
# -----------------------------------------------
print()
print(SEP)
print("3. ELEMENTOS DUPLICADOS")
print(SEP)

m3 = MonticuloBinario()
for v in [3, 3, 3, 1, 1]:
    m3.insertar(v)
print("Lista interna:", m3.ver_lista_interna())
print("Extracciones esperadas: 1, 1, 3, 3, 3")
resultado = []
while not m3.esta_vacio():
    resultado.append(m3.eliminarMin())
print("Resultado:", resultado)


# -----------------------------------------------
# 4. construirMonticulo desde lista
# -----------------------------------------------
print()
print(SEP)
print("4. CONSTRUIR MONTÍCULO DESDE LISTA")
print(SEP)

m4 = MonticuloBinario()
m4.construirMonticulo([9, 6, 5, 2, 3])
print("Lista interna tras construir:", m4.ver_lista_interna())
print("Mínimo esperado: 2 →", m4.eliminarMin())
print("Tamaño restante:", m4.tamano())   # 4


# -----------------------------------------------
# 5. construirMonticulo con lista vacía
# -----------------------------------------------
print()
print(SEP)
print("5. CONSTRUIR DESDE LISTA VACÍA")
print(SEP)

m5 = MonticuloBinario()
m5.construirMonticulo([])
print("Vacío:", m5.esta_vacio())         # True
print("Tamaño:", m5.tamano())            # 0
print("eliminarMin en vacío:", m5.eliminarMin())  # None


# -----------------------------------------------
# 6. esta_vacio y tamano
# -----------------------------------------------
print()
print(SEP)
print("6. ESTA_VACIO Y TAMANO")
print(SEP)

m6 = MonticuloBinario()
print("Vacío inicial:", m6.esta_vacio())  # True
m6.insertar(10)
m6.insertar(20)
print("Tamaño con 2 elementos:", m6.tamano())  # 2
m6.eliminarMin()
print("Tamaño tras extraer uno:", m6.tamano())  # 1
m6.eliminarMin()
print("Vacío al final:", m6.esta_vacio())  # True


# -----------------------------------------------
# 7. Manejo de errores esperados
# -----------------------------------------------
print()
print(SEP)
print("7. MANEJO DE ERRORES")
print(SEP)

m7 = MonticuloBinario()

# insertar None
try:
    m7.insertar(None)
except ValueError as e:
    print("insertar(None) →", e)

# construirMonticulo con tipo incorrecto
try:
    m7.construirMonticulo("no soy lista")
except TypeError as e:
    print("construirMonticulo(str) →", e)

# construirMonticulo con None dentro
try:
    m7.construirMonticulo([1, None, 3])
except ValueError as e:
    print("construirMonticulo([1, None, 3]) →", e)

print()
print("Pruebas del montículo finalizadas.")
