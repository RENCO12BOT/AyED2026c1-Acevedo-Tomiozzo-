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
        # Nuevo nodo pasa a ser la cabeza; reenlaza el anterior primero
        nuevo = Nodo(item)
        if self.esta_vacia():
            self.__cabeza = self.__cola = nuevo
        else:
            nuevo.asignar_siguiente(self.__cabeza)
            self.__cabeza.asignar_anterior(nuevo)
            self.__cabeza = nuevo
        self.__tamanio += 1

    def agregar_al_final(self, item):
        # Nuevo nodo pasa a ser la cola; reenlaza el anterior último
        nuevo = Nodo(item)
        if self.esta_vacia():
            self.__cabeza = self.__cola = nuevo
        else:
            self.__cola.asignar_siguiente(nuevo)
            nuevo.asignar_anterior(self.__cola)
            self.__cola = nuevo
        self.__tamanio += 1

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
        # Agrega el elemento en la posición dada; acepta índices negativos
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

    def extraer(self, posicion=None):
        # Elimina y devuelve el elemento en la posición dada; acepta índices negativos
        if self.esta_vacia():
            raise IndexError("La lista está vacía")
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
            # Reconecta los vecinos saltando el nodo eliminado
            actual.obtener_anterior().asignar_siguiente(actual.obtener_siguiente())
            actual.obtener_siguiente().asignar_anterior(actual.obtener_anterior())
        self.__tamanio -= 1
        return valor

    def copiar(self):
        # Devuelve una nueva lista con los mismos valores pero nodos independientes
        nueva = ListaDobleEnlazada()
        actual = self.__cabeza
        while actual:
            nueva.agregar_al_final(actual.obtener_valor())
            actual = actual.obtener_siguiente()
        return nueva

    def invertir(self):
        # Invierte el orden de la lista en el lugar intercambiando punteros de cada nodo
        actual = self.__cabeza
        while actual:
            siguiente = actual.obtener_siguiente()
            actual.asignar_siguiente(actual.obtener_anterior())
            actual.asignar_anterior(siguiente)
            actual = siguiente
        self.__cabeza, self.__cola = self.__cola, self.__cabeza

    def concatenar(self, otra_lista):
        # Une otra_lista al final de esta; opera sobre una copia para no compartir nodos
        copia = otra_lista.copiar()
        if self.esta_vacia():
            self.__cabeza = copia._ListaDobleEnlazada__cabeza
            self.__cola = copia._ListaDobleEnlazada__cola
        elif not copia.esta_vacia():
            self.__cola.asignar_siguiente(copia._ListaDobleEnlazada__cabeza)
            copia._ListaDobleEnlazada__cabeza.asignar_anterior(self.__cola)
            self.__cola = copia._ListaDobleEnlazada__cola
        self.__tamanio += len(otra_lista)

    def __iter__(self):
        # Permite recorrer la lista con un for, de cabeza a cola
        actual = self.__cabeza
        while actual:
            yield actual.obtener_valor()
            actual = actual.obtener_siguiente()

    def __add__(self, otra_lista):
        # Devuelve una nueva lista combinada sin modificar las originales
        nueva = self.copiar()
        nueva.concatenar(otra_lista)
        return nueva

    @property
    def cabeza(self):
        return self.__cabeza

    @property
    def cola(self):
        return self.__cola