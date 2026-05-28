from ayedfiuner.estructuras.cola_prioridad import ColaPrioridad

# prueba de la cola de prioridad
print()
print("=" * 40)
print("PRUEBA COLA DE PRIORIDAD")
print("=" * 40)

# caso basico: distintas prioridades
cola = ColaPrioridad()
cola.insertar(3, "riesgo bajo")
cola.insertar(1, "riesgo critico")
cola.insertar(2, "riesgo moderado")

print("Orden de atencion esperado: critico, moderado, bajo")
print("Sale:", cola.extraer())   # critico
print("Sale:", cola.extraer())   # moderado
print("Sale:", cola.extraer())   # bajo

# caso empate: misma prioridad, respeta llegada
print()
print("Prueba empate FIFO:")
cola2 = ColaPrioridad()
cola2.insertar(2, "llego primero")
cola2.insertar(2, "llego segundo")
cola2.insertar(2, "llego tercero")

print("Sale:", cola2.extraer())  # llego primero
print("Sale:", cola2.extraer())  # llego segundo
print("Sale:", cola2.extraer())  # llego tercero

# cola vacia
print()
print("Prueba cola vacia:")
cola3 = ColaPrioridad()
print("Esta vacia:", cola3.esta_vacia())    # True
print("Extraer:", cola3.extraer())          # None
print("Ver proximo:", cola3.ver_proximo())  # None