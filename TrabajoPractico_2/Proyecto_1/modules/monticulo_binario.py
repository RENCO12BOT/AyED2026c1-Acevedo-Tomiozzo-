class monticulo_binario:
    def __init__(self):
        self.__monticulo_lista = [None]
        self._tamano_actual = 0

    def infilArriba(self, i):
        while i // 2 > 0:
            if self.__monticulo_lista[i] < self.__monticulo_lista[i // 2]:
                self.__monticulo_lista[i // 2], self.__monticulo_lista[i] = (
                    self.__monticulo_lista[i],
                    self.__monticulo_lista[i // 2],
                )
            i //= 2

    def insertar(self, elemento):
        self.__monticulo_lista.append(elemento)
        self._tamano_actual += 1
        self.infilArriba(self._tamano_actual)

    def hijo_minimo(self, i):
        if 2 * i + 1 > self._tamano_actual:
            return 2 * i
        else:
            if self.__monticulo_lista[2 * i] < self.__monticulo_lista[2 * i + 1]:
                return 2 * i
            else:
                return 2 * i + 1

    def infilAbajo(self, i):
        while 2 * i <= self._tamano_actual:
            hijo_minimo = self.hijo_minimo(i)
            if self.__monticulo_lista[i] > self.__monticulo_lista[hijo_minimo]:
                self.__monticulo_lista[hijo_minimo], self.__monticulo_lista[i] = (
                    self.__monticulo_lista[i],
                    self._monticulo_lista[hijo_minimo],
                )
            else:
                break
            i = hijo_minimo

    def eliminarMinimo(self):
        if self._tamano_actual == 0:
            return None
        minimo = self._monticulo_lista[1]
        self._monticulo_lista[1] = self._monticulo_lista[self._tamano_actual]
        self._monticulo_lista.pop()
        self._tamano_actual -= 1
        self.infilAbajo(1)
        return minimo

    def construirMonticulo(self, lista):
        self._monticulo_lista = [None] + lista[:]
        self._tamano_actual = len(lista)
        i = self._tamano_actual // 2
        while i > 0:
            self.infilAbajo(i)
            i -= 1

    def esta_vacia(self):
        return self._tamano_actual == 0

    def tamano(self):
        return self._tamano_actual

                    