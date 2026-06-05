class MonticuloBinario:
    """
    Montículo Binario Mínimo (Min-Heap) genérico.

    El elemento con menor valor siempre queda en la raíz.
    Los elementos deben ser comparables entre sí (soportar < y >).
    Estructura de propósito general: no está acoplada a ningún dominio.
    """

    def __init__(self):
        """
        Postcondición:
            - Se crea un montículo vacío.
            - listaMonticulo = [0] (el 0 en índice 0 es relleno, no un elemento real).
            - tamanoActual = 0.
        """
        self.listaMonticulo = [0]
        self.tamanoActual = 0

    # ------------------------------------------------------------------
    # Métodos internos (no forman parte de la interfaz pública)
    # ------------------------------------------------------------------

    def infiltArriba(self, i):
        """
        Sube el elemento en la posición i hasta restaurar la propiedad del montículo.

        Precondición:
            - i es un entero con 1 <= i <= tamanoActual.
            - El elemento en i ya fue insertado en listaMonticulo.
        Postcondición:
            - El elemento queda en la posición correcta según el orden del montículo.
            - La propiedad de montículo mínimo se mantiene en todo el árbol.
        """
        if not isinstance(i, int) or i < 1 or i > self.tamanoActual:
            raise ValueError(
                f"infiltArriba: índice fuera de rango. "
                f"Se recibió {i}, rango válido [1, {self.tamanoActual}]."
            )
        while i // 2 > 0:
            if self.listaMonticulo[i] < self.listaMonticulo[i // 2]:
                self.listaMonticulo[i], self.listaMonticulo[i // 2] = \
                    self.listaMonticulo[i // 2], self.listaMonticulo[i]
                i //= 2
            else:
                break

    def hijoMin(self, i):
        """
        Retorna el índice del hijo con menor valor del nodo en posición i.

        Precondición:
            - i es un entero con 1 <= i <= tamanoActual.
            - El nodo en i tiene al menos un hijo (i * 2 <= tamanoActual).
        Postcondición:
            - Retorna i*2 si el nodo solo tiene hijo izquierdo.
            - Retorna el índice del hijo con menor valor si tiene ambos hijos.
        """
        if not isinstance(i, int) or i < 1 or i * 2 > self.tamanoActual:
            raise ValueError(
                f"hijoMin: el nodo en posición {i} no tiene hijos o el índice es inválido."
            )
        if i * 2 + 1 > self.tamanoActual:
            return i * 2
        if self.listaMonticulo[i * 2] < self.listaMonticulo[i * 2 + 1]:
            return i * 2
        return i * 2 + 1

    def infiltAbajo(self, i):
        """
        Baja el elemento en la posición i hasta restaurar la propiedad del montículo.

        Precondición:
            - i es un entero con 1 <= i <= tamanoActual.
        Postcondición:
            - El elemento queda en la posición correcta según el orden del montículo.
            - La propiedad de montículo mínimo se mantiene en todo el árbol.
        """
        if not isinstance(i, int) or i < 1 or i > self.tamanoActual:
            raise ValueError(
                f"infiltAbajo: índice fuera de rango. "
                f"Se recibió {i}, rango válido [1, {self.tamanoActual}]."
            )
        while (i * 2) <= self.tamanoActual:
            hm = self.hijoMin(i)
            if self.listaMonticulo[i] > self.listaMonticulo[hm]:
                self.listaMonticulo[i], self.listaMonticulo[hm] = \
                    self.listaMonticulo[hm], self.listaMonticulo[i]
            else:
                break
            i = hm

    # ------------------------------------------------------------------
    # Interfaz pública
    # ------------------------------------------------------------------

    def insertar(self, k):
        """
        Inserta el elemento k en el montículo.

        Precondición:
            - k no puede ser None.
            - k debe ser comparable con los demás elementos ya insertados
              (debe soportar los operadores < y >).
        Postcondición:
            - k queda almacenado en el montículo.
            - tamanoActual aumenta en 1.
            - La propiedad de montículo mínimo se mantiene.
        """
        if k is None:
            raise ValueError("No se puede insertar None en el montículo.")
        self.listaMonticulo.append(k)
        self.tamanoActual += 1
        self.infiltArriba(self.tamanoActual)

    def eliminarMin(self):
        """
        Extrae y retorna el elemento mínimo del montículo.

        Precondición:
            - Ninguna obligatoria; si el montículo está vacío retorna None.
        Postcondición:
            - Si el montículo no estaba vacío: retorna el elemento con menor valor,
              tamanoActual disminuye en 1, y la propiedad de montículo se restaura.
            - Si estaba vacío: retorna None sin modificar el estado.
        """
        if self.tamanoActual == 0:
            return None
        valorSacado = self.listaMonticulo[1]
        self.listaMonticulo[1] = self.listaMonticulo[self.tamanoActual]
        self.tamanoActual -= 1
        self.listaMonticulo.pop()
        if self.tamanoActual > 0:
            self.infiltAbajo(1)
        return valorSacado

    def construirMonticulo(self, unaLista):
        """
        Construye el montículo a partir de una lista existente en O(n).

        Precondición:
            - unaLista es una lista (puede estar vacía).
            - Ningún elemento de unaLista puede ser None.
            - Todos los elementos deben ser comparables entre sí.
        Postcondición:
            - El montículo contiene exactamente los elementos de unaLista.
            - tamanoActual = len(unaLista).
            - La propiedad de montículo mínimo se cumple.
        """
        if not isinstance(unaLista, list):
            raise TypeError(
                f"construirMonticulo espera una lista. Se recibió: {type(unaLista)}"
            )
        if any(x is None for x in unaLista):
            raise ValueError("La lista no puede contener elementos None.")
        i = len(unaLista) // 2
        self.tamanoActual = len(unaLista)
        self.listaMonticulo = [0] + unaLista[:]
        while i > 0:
            self.infiltAbajo(i)
            i -= 1

    def esta_vacio(self):
        """
        Postcondición:
            - Retorna True si el montículo no tiene elementos, False en caso contrario.
        """
        return self.tamanoActual == 0

    def tamano(self):
        """
        Postcondición:
            - Retorna un entero >= 0 igual a la cantidad de elementos almacenados.
        """
        return self.tamanoActual

    def ver_lista_interna(self):
        """
        Postcondición:
            - Retorna una copia de la lista interna sin el elemento de relleno (índice 0).
            - No modifica el estado del montículo.
        """
        return self.listaMonticulo[1:]