class Nodo:

    def __init__(self, valor):
        self.__valor = valor
        self.__anterior = None
        self.__siguiente = None

    def asignar_siguiente(self, nodo_siguiente):
        self.__siguiente = nodo_siguiente

    def obtener_siguiente(self):
        return self.__siguiente

    def asignar_anterior(self, nodo_anterior):
        self.__anterior = nodo_anterior

    def obtener_anterior(self):
        return self.__anterior

    def obtener_valor(self):
        return self.__valor

    @property
    def dato(self):
        return self.__valor

    @property
    def siguiente(self):
        return self.__siguiente

    @property
    def anterior(self):
        return self.__anterior


class ListaDobleEnlazada:

    def __init__(self):
        # Parte de vacía: sin cabeza, sin cola, tamaño cero
        self.__cabeza = None
        self.__cola = None
        self.__tamanio = 0

    def esta_vacia(self):
        # True si no hay ningún nodo
        return self.__cabeza is None

    def agregar_al_inicio(self, item):
        """
        Agrega un elemento al principio de la lista.

        Precondiciones:
            - item puede ser cualquier valor, no hay restriccion de tipo

        Postcondiciones:
            - la lista tiene un elemento mas que antes
            - el nuevo elemento es ahora la cabeza
            - si la lista estaba vacia, el elemento es tambien la cola
        """
        #  PRECONDICIONES 
        if item is None:
            raise ValueError("no se puede agregar None a la lista")

        tamanio_antes = self.__tamanio
        
        # guardo la cabeza anterior para verificar despues
        cabeza_antes = self.__cabeza

        nuevo = Nodo(item)
        if self.esta_vacia():
            self.__cabeza = self.__cola = nuevo
        else:
            nuevo.asignar_siguiente(self.__cabeda)
            self.__cabeza.asignar_anterior(nuevo)
            self.__cabeza = nuevo
        self.__tamanio += 1

        #  POSTCONDICIONES
        if self.__tamanio != tamanio_antes + 1:
            raise RuntimeError("el tamanio no aumento correctamente")
        if self.__cabeza.obtener_valor() != item:
            raise RuntimeError("el nuevo elemento no quedo como cabeza")
        if tamanio_antes == 0 and self.__cola.obtener_valor() != item:
            raise RuntimeError("si la lista estaba vacia, el elemento tiene que ser tambien la cola")

    def agregar_al_final(self, item):
        """
        Agrega un elemento al final de la lista.

        Precondiciones:
            - item no puede ser None

        Postcondiciones:
            - la lista tiene un elemento mas que antes
            - el nuevo elemento es ahora la cola
            - si la lista estaba vacia, el elemento es tambien la cabeza
        """
        #  PRECONDICIONES |
        if item is None:
            raise ValueError("no se puede agregar None a la lista")

        tamanio_antes = self.__tamanio
        estaba_vacia = self.esta_vacia()

        nuevo = Nodo(item)
        if self.esta_vacia():
            self.__cabeza = self.__cola = nuevo
        else:
            self.__cola.asignar_siguiente(nuevo)
            nuevo.asignar_anterior(self.__cola)
            self.__cola = nuevo
        self.__tamanio += 1

        #  POSTCONDICIONES
        if self.__tamanio != tamanio_antes + 1:
            raise RuntimeError("el tamanio no aumento correctamente")
        if self.__cola.obtener_valor() != item:
            raise RuntimeError("el nuevo elemento no quedo como cola")
        if estaba_vacia and self.__cabeza.obtener_valor() != item:
            raise RuntimeError("si la lista estaba vacia, el elemento tiene que ser tambien la cabeza")

    def __len__(self):
        return self.__tamanio

    @property
    def tamanio(self):
        return self.__tamanio

    def _normalizar_posicion(self, posicion, para_insertar=False):
        # Convierte índices negativos a positivos; lanza error si queda fuera de rango
        limite = self.__tamanio if para_insertar else self.__tamanio - 1
        if posicion < 0:
            posicion = self.__tamanio + posicion + (1 if para_insertar else 0)
        if posicion < 0 or posicion > limite:
            raise IndexError("Posición fuera de rango")
        return posicion

    def insertar(self, item, posicion=None):
        """
        Agrega un elemento en la posicion indicada.

        Precondiciones:
            - item no puede ser None
            - posicion, si se da, tiene que ser un entero
            - posicion tiene que estar dentro del rango valido de la lista

        Postcondiciones:
            - la lista tiene un elemento mas que antes
            - el elemento insertado esta en la posicion correcta
        """
        # --- PRECONDICIONES ---
        if item is None:
            raise ValueError("no se puede insertar None en la lista")
        if posicion is not None and not isinstance(posicion, int):
            raise TypeError("la posicion tiene que ser un entero")

        tamanio_antes = self.__tamanio

        if posicion is None:
            self.agregar_al_final(item)
            return
        
        posicion = self._normalizar_posicion(posicion, para_insertar=True)
        
        if posicion == 0:
            self.agregar_al_inicio(item)
        elif posicion == self.__tamanio:
            self.agregar_al_final(item)
        else:
            actual = self.__cabeza
            for _ in range(posicion):
                actual = actual.obtener_siguiente()
            nuevo = Nodo(item)
            anterior = actual.obtener_anterior()
            nuevo.asignar_siguiente(actual)
            nuevo.asignar_anterior(anterior)
            anterior.asignar_siguiente(nuevo)
            actual.asignar_anterior(nuevo)
            self.__tamanio += 1

        #  POSTCONDICIONES
        if self.__tamanio != tamanio_antes + 1:
            raise RuntimeError("el tamanio no aumento, algo salio mal al insertar")

    def extraer(self, posicion=None):
        """
        Elimina y devuelve el elemento en la posicion dada.

        Precondiciones:
            - la lista no puede estar vacia
            - posicion, si se da, tiene que ser un entero
            - posicion tiene que estar dentro del rango valido

        Postcondiciones:
            - la lista tiene un elemento menos que antes
            - el valor devuelto es el que estaba en esa posicion
            - los enlaces de los nodos vecinos quedaron bien reconectados
        """
        # --- PRECONDICIONES ---
        if self.esta_vacia():
            raise IndexError("la lista esta vacia, no hay nada que extraer")
        if posicion is not None and not isinstance(posicion, int):
            raise TypeError("la posicion tiene que ser un entero")

        tamanio_antes = self.__tamanio

        if posicion is None:
            posicion = self.__tamanio - 1
        else:
            posicion = self._normalizar_posicion(posicion, para_insertar=False)

        if posicion == 0:
            valor = self.__cabeza.obtener_valor()
            self.__cabeza = self.__cabeza.obtener_siguiente()
            if self.__cabeza:
                self.__cabeza.asignar_anterior(None)
            else:
                self.__cola = None
        elif posicion == self.__tamanio - 1:
            valor = self.__cola.obtener_valor()
            self.__cola = self.__cola.obtener_anterior()
            if self.__cola:
                self.__cola.asignar_siguiente(None)
            else:
                self.__cabeza = None
        else:
            actual = self.__cabeza
            for _ in range(posicion):
                actual = actual.obtener_siguiente()
            valor = actual.obtener_valor()
            # reconecta los vecinos saltando el nodo eliminado
            actual.obtener_anterior().asignar_siguiente(actual.obtener_siguiente())
            actual.obtener_siguiente().asignar_anterior(actual.obtener_anterior())

        self.__tamanio -= 1

        #  POSTCONDICIONES
        if self.__tamanio != tamanio_antes - 1:
            raise RuntimeError("el tamanio no disminuyo correctamente")
        if self.__tamanio == 0 and (self.__cabeza is not None or self.__cola is not None):
            raise RuntimeError("si la lista quedo vacia, cabeza y cola tienen que ser None")

        return valor

    def copiar(self):
        """
        Devuelve una nueva lista con los mismos valores pero nodos independientes.

        Precondiciones:
            - ninguna, funciona aunque la lista este vacia

        Postcondiciones:
            - la nueva lista tiene el mismo tamanio que la original
            - los valores son iguales y en el mismo orden
            - modificar la copia no afecta a la original
        """
        nueva = ListaDobleEnlazada()
        actual = self.__cabeza
        while actual:
            nueva.agregar_al_final(actual.obtener_valor())
            actual = actual.obtener_siguiente()

        # --- POSTCONDICIONES ---
        if len(nueva) != self.__tamanio:
            raise RuntimeError("la copia no tiene el mismo tamanio que la original")
        
        # verifico que los valores sean iguales en orden
        valores_original = list(self)
        valores_copia = list(nueva)
        if valores_original != valores_copia:
            raise RuntimeError("la copia no tiene los mismos valores que la original")

        return nueva

    def invertir(self):
        """
        Invierte el orden de la lista intercambiando los punteros de cada nodo.

        Precondiciones:
            - ninguna, funciona aunque la lista este vacia o tenga un solo elemento

        Postcondiciones:
            - la cabeza pasa a ser la cola y viceversa
            - los valores en orden inverso son los mismos que antes
            - el tamanio no cambia
        """
        # guardo los valores antes para verificar despues
        valores_antes = list(self)
        tamanio_antes = self.__tamanio

        actual = self.__cabeza
        while actual:
            siguiente = actual.obtener_siguiente()
            actual.asignar_siguiente(actual.obtener_anterior())
            actual.asignar_anterior(siguiente)
            actual = siguiente
        self.__cabeza, self.__cola = self.__cola, self.__cabeza

        # POSTCONDICIONES
        if self.__tamanio != tamanio_antes:
            raise RuntimeError("el tamanio cambio al invertir, algo salio mal")
        valores_despues = list(self)
        if valores_despues != valores_antes[::-1]:
            raise RuntimeError("los valores no quedaron en orden inverso correctamente")

    def concatenar(self, otra_lista):
        """
        Une otra_lista al final de esta lista.

        Precondiciones:
            - otra_lista tiene que ser una instancia de ListaDobleEnlazada
            - no se puede concatenar la lista consigo misma

        Postcondiciones:
            - el tamanio de esta lista aumenta en len(otra_lista)
            - los elementos de otra_lista aparecen al final y en el mismo orden
            - otra_lista no se modifica
        """
        # --- PRECONDICIONES ---
        if not isinstance(otra_lista, ListaDobleEnlazada):
            raise TypeError("solo se puede concatenar con otra ListaDobleEnlazada")
        if otra_lista is self:
            raise ValueError("no se puede concatenar la lista consigo misma")

        tamanio_antes = self.__tamanio
        tamanio_otra = len(otra_lista)
        valores_otra_antes = list(otra_lista)  # guardo para verificar que no se modifica

        copia = otra_lista.copiar()
        if self.esta_vacia():
            self.__cabeza = copia._ListaDobleEnlazada__cabeza
            self.__cola = copia._ListaDobleEnlazada__cola
        elif not copia.esta_vacia():
            self.__cola.asignar_siguiente(copia._ListaDobleEnlazada__cabeza)
            copia._ListaDobleEnlazada__cabeza.asignar_anterior(self.__cola)
            self.__cola = copia._ListaDobleEnlazada__cola
        self.__tamanio += len(otra_lista)

        # POSTCONDICIONES 
        if self.__tamanio != tamanio_antes + tamanio_otra:
            raise RuntimeError("el tamanio no quedo bien despues de concatenar")
        if list(otra_lista) != valores_otra_antes:
            raise RuntimeError("otra_lista se modifico, no deberia pasar")

    def __iter__(self):
        # Permite recorrer la lista con un for, de cabeza a cola
        actual = self.__cabeza
        while actual:
            yield actual.obtener_valor()
            actual = actual.obtener_siguiente()

    def __add__(self, otra_lista):
        """
        Devuelve una nueva lista combinada sin modificar las originales.

        Precondiciones:
            - otra_lista tiene que ser una instancia de ListaDobleEnlazada

        Postcondiciones:
            - la nueva lista tiene los elementos de ambas listas en orden
            - ninguna de las dos listas originales se modifica
        """
        # PRECONDICIONES
        if not isinstance(otra_lista, ListaDobleEnlazada):
            raise TypeError("solo se puede sumar con otra ListaDobleEnlazada")

        valores_self_antes = list(self)
        valores_otra_antes = list(otra_lista)

        nueva = self.copiar()
        nueva.concatenar(otra_lista)

        #  POSTCONDICIONES
        if list(self) != valores_self_antes:
            raise RuntimeError("la lista original se modifico, no deberia pasar")
        if list(otra_lista) != valores_otra_antes:
            raise RuntimeError("otra_lista se modifico, no deberia pasar")
        if len(nueva) != len(valores_self_antes) + len(valores_otra_antes):
            raise RuntimeError("la nueva lista no tiene el tamanio correcto")

        return nueva

    @property
    def cabeza(self):
        return self.__cabeza

    @property
    def cola(self):
        return self.__cola