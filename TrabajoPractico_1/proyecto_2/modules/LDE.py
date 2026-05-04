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
    def __init__(self):                          # era _init_
        self.__cabeza = None
        self.__cola = None
        self.__tamanio = 0

    def esta_vacia(self):
        return self.__cabeza is None

    def agregar_al_inicio(self, item):
        nuevo = Nodo(item)
        if self.esta_vacia():
            self.__cabeza = self.__cola = nuevo  # era self._cabeza/_cola
        else:
            nuevo.asignar_siguiente(self.__cabeza)
            self.__cabeza.asignar_anterior(nuevo)
            self.__cabeza = nuevo
        self.__tamanio += 1

    def agregar_al_final(self, item):
        nuevo = Nodo(item)
        if self.esta_vacia():
            self.__cabeza = self.__cola = nuevo  # era self._cabeza/_cola
        else:
            self.__cola.asignar_siguiente(nuevo)
            nuevo.asignar_anterior(self.__cola)
            self.__cola = nuevo
        self.__tamanio += 1

    def __len__(self):                           # era _len_
        return self.__tamanio

    @property
    def tamanio(self):
        return self.__tamanio

    def insertar(self, item, posicion=None):
        if posicion is None:
            self.agregar_al_final(item)
            return
        if posicion < 0 or posicion > self.__tamanio:
            raise IndexError("Posición fuera de rango")
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
        if self.esta_vacia():
            raise IndexError("La lista está vacía")
        if posicion is None or posicion == -1:
            posicion = self.__tamanio - 1
        if posicion < 0 or posicion >= self.__tamanio:
            raise IndexError("Posición fuera de rango")
        if posicion == 0:
            valor = self.__cabeza.obtener_valor()
            self.__cabeza = self.__cabeza.obtener_siguiente()  # era self._cabeza
            if self.__cabeza:
                self.__cabeza.asignar_anterior(None)
            else:
                self.__cola = None
        elif posicion == self.__tamanio - 1:
            valor = self.__cola.obtener_valor()
            self.__cola = self.__cola.obtener_anterior()       # era self._cola
            if self.__cola:
                self.__cola.asignar_siguiente(None)
            else:
                self.__cabeza = None
        else:
            actual = self.__cabeza
            for _ in range(posicion):
                actual = actual.obtener_siguiente()
            valor = actual.obtener_valor()
            actual.obtener_anterior().asignar_siguiente(actual.obtener_siguiente())
            actual.obtener_siguiente().asignar_anterior(actual.obtener_anterior())
        self.__tamanio -= 1
        return valor

    def copiar(self):
        nueva = ListaDobleEnlazada()
        actual = self.__cabeza
        while actual:
            nueva.agregar_al_final(actual.obtener_valor())
            actual = actual.obtener_siguiente()
        return nueva

    def invertir(self):
        actual = self.__cabeza
        while actual:
            siguiente = actual.obtener_siguiente()
            actual.asignar_siguiente(actual.obtener_anterior())
            actual.asignar_anterior(siguiente)
            actual = siguiente
        self.__cabeza, self.__cola = self.__cola, self.__cabeza  # era self._cabeza/self.cola

    def concatenar(self, otra_lista):
        copia = otra_lista.copiar()  # ← clave: no tocamos los nodos originales
        if self.esta_vacia():
           self.__cabeza = copia._ListaDobleEnlazada__cabeza
           self.__cola = copia._ListaDobleEnlazada__cola
        elif not copia.esta_vacia():
             self.__cola.asignar_siguiente(copia._ListaDobleEnlazada__cabeza)
             copia._ListaDobleEnlazada__cabeza.asignar_anterior(self.__cola)
             self.__cola = copia._ListaDobleEnlazada__cola
        self.__tamanio += len(otra_lista)

    def __iter__(self):                          # era _iter_
        actual = self.__cabeza
        while actual:
            yield actual.obtener_valor()
            actual = actual.obtener_siguiente()

    def __add__(self, otra_lista):               # era _add_
        nueva = ListaDobleEnlazada()
        for item in self:
            nueva.agregar_al_final(item)
        for item in otra_lista:
            nueva.agregar_al_final(item)
        return nueva

    @property
    def cabeza(self):
        return self.__cabeza

    @property
    def cola(self):
        return self.__cola