from ayedfiuner.estructuras.monticulo_binario import MonticuloBinario

class ColaPrioridad:
    """
    Cola de prioridad generica usando un monticulo binario minimo.
    El elemento con menor numero de prioridad sale primero.
    Si dos tienen la misma prioridad, sale el que llego antes.
    """

    def __init__(self):
        self._monticulo = MonticuloBinario()
        self._contador = 0  # para el orden de llegada en empates

    def insertar(self, prioridad, dato):
        # guardamos la prioridad y el orden de llegada juntos para comparar
        clave = (prioridad, self._contador)
        self._monticulo.insertar((clave, dato))
        self._contador += 1

    def extraer(self):
        if self.esta_vacia():
            return None
        clave, dato = self._monticulo.eliminarMin()
        return dato

    def ver_proximo(self):
        # muestra quien sigue sin sacarlo
        if self.esta_vacia():
            return None
        clave, dato = self._monticulo.listaMonticulo[1]
        return dato

    def ver_todos(self):
        # util para mostrar el estado de la cola sin modificarla
        elementos = self._monticulo.ver_lista_interna()
        return [dato for clave, dato in sorted(elementos)]

    def esta_vacia(self):
        return self._monticulo.esta_vacio()

    def tamano(self):
        return self._monticulo.tamano()

    def __len__(self):
        return self.tamano()

    def __iter__(self):
        return iter(self.ver_todos())

    def __repr__(self):
        return f"ColaPrioridad -> {self.ver_todos()}"