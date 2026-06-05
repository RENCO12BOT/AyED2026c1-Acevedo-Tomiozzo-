from ayedfiuner.estructuras.monticulo_binario import MonticuloBinario

class ColaPrioridad:
    """
    Cola de prioridad genérica basada en un montículo binario mínimo.

    El elemento con menor número de prioridad sale primero (prioridad 1 = más urgente).
    Si dos elementos tienen la misma prioridad, sale el que llegó antes (FIFO).

    Estructura genérica: no está acoplada a ningún tipo de dato específico.
    """

    def __init__(self):
        """
        Postcondición:
            - Se crea una cola vacía.
            - _monticulo es un MonticuloBinario vacío.
            - _contador = 0 (orden de llegada para resolver empates).
        """
        self._monticulo = MonticuloBinario()
        self._contador = 0

    def insertar(self, prioridad, dato):
        """
        Inserta un elemento con su prioridad asociada.

        Precondición:
            - prioridad es un entero o float >= 0.
            - dato no puede ser None.
        Postcondición:
            - El elemento queda almacenado con su clave (prioridad, orden_llegada).
            - La cola puede atenderlo en el orden correcto.
            - _contador aumenta en 1.
        """
        if not isinstance(prioridad, (int, float)):
            raise TypeError(
                f"La prioridad debe ser numérica. Se recibió: {type(prioridad)}"
            )
        if prioridad < 0:
            raise ValueError(
                f"La prioridad debe ser >= 0. Se recibió: {prioridad}"
            )
        if dato is None:
            raise ValueError("No se puede insertar None como dato.")
        clave = (prioridad, self._contador)
        self._monticulo.insertar((clave, dato))
        self._contador += 1

    def extraer(self):
        """
        Extrae y retorna el dato con mayor prioridad (menor número).
        En caso de empate, sale el que llegó antes (FIFO).

        Precondición:
            - Ninguna obligatoria; si la cola está vacía retorna None.
        Postcondición:
            - Retorna el dato del elemento con menor clave (prioridad, orden).
            - Si la cola estaba vacía, retorna None sin modificar el estado.
        """
        if self.esta_vacia():
            return None
        clave, dato = self._monticulo.eliminarMin()
        return dato

    def ver_proximo(self):
        """
        Retorna el dato del próximo a ser atendido sin extraerlo.

        Precondición:
            - Ninguna; si la cola está vacía retorna None.
        Postcondición:
            - El estado de la cola no se modifica.
            - Retorna el dato del elemento con mayor prioridad, o None si está vacía.
        """
        if self.esta_vacia():
            return None
        _, dato = self._monticulo.listaMonticulo[1]
        return dato

    def ver_todos(self):
        """
        Retorna los datos de todos los elementos ordenados por clave.

        Precondición:
            - Ninguna.
        Postcondición:
            - Retorna una lista (puede estar vacía) con los datos ordenados
              por (prioridad, orden_llegada). No modifica el estado de la cola.
        """
        elementos = self._monticulo.ver_lista_interna()
        return [dato for clave, dato in sorted(elementos)]

    def esta_vacia(self):
        """
        Postcondición:
            - Retorna True si la cola no tiene elementos, False en caso contrario.
        """
        return self._monticulo.esta_vacio()

    def tamano(self):
        """
        Postcondición:
            - Retorna un entero >= 0 igual a la cantidad de elementos en la cola.
        """
        return self._monticulo.tamano()

    def __len__(self):
        return self.tamano()

    def __iter__(self):
        return iter(self.ver_todos())

    def __repr__(self):
        return f"ColaPrioridad -> {self.ver_todos()}"