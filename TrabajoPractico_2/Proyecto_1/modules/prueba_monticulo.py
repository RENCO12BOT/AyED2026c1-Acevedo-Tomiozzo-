from ayedfiuner.estructuras.monticulo_binario import MonticuloBinario

# prueba del monticulo binario
print("=" * 40)
print("PRUEBA MONTICULO BINARIO")
print("=" * 40)

m = MonticuloBinario()
m.insertar(5)
m.insertar(2)
m.insertar(8)
m.insertar(1)
m.insertar(4)

print("Lista interna:", m.ver_lista_interna())
print("Extraigo minimo:", m.eliminarMin())  # tiene que dar 1
print("Extraigo minimo:", m.eliminarMin())  # tiene que dar 2
print("Tamanio restante:", m.tamano())      # tiene que dar 3
print("Esta vacio:", m.esta_vacio())        # False

m2 = MonticuloBinario()
print("Monticulo vacio, eliminarMin:", m2.eliminarMin())  # None

