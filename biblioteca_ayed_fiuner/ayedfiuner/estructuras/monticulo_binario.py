class MonticuloBinario:
    """Monticulo Binario Minimo - el elemento mas chico siempre queda arriba."""

    def __init__(self):
        self.listaMonticulo = [0]  # el 0 es de relleno, no es un elemento real
        self.tamanoActual = 0

    def infiltArriba(self, i):
        # sube el elemento hasta que este en su lugar correcto
        while i // 2 > 0:
            if self.listaMonticulo[i] < self.listaMonticulo[i // 2]:
                self.listaMonticulo[i], self.listaMonticulo[i // 2] = \
                    self.listaMonticulo[i // 2], self.listaMonticulo[i]
                i //= 2
            else:
                break

    def insertar(self, k):
        self.listaMonticulo.append(k)
        self.tamanoActual += 1
        self.infiltArriba(self.tamanoActual)

    def hijoMin(self, i):
        # si no tiene hijo derecho devuelve el izquierdo directamente
        if i * 2 + 1 > self.tamanoActual:
            return i * 2
        else:
            if self.listaMonticulo[i * 2] < self.listaMonticulo[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def infiltAbajo(self, i):
        # baja el elemento hasta que este en su lugar correcto
        while (i * 2) <= self.tamanoActual:
            hm = self.hijoMin(i)
            if self.listaMonticulo[i] > self.listaMonticulo[hm]:
                self.listaMonticulo[i], self.listaMonticulo[hm] = \
                    self.listaMonticulo[hm], self.listaMonticulo[i]
            i = hm

    def eliminarMin(self):
        if self.tamanoActual == 0:
            return None
        valorSacado = self.listaMonticulo[1]
        # ponemos el ultimo elemento en la raiz y despues lo bajamos
        self.listaMonticulo[1] = self.listaMonticulo[self.tamanoActual]
        self.tamanoActual -= 1
        self.listaMonticulo.pop()
        if self.tamanoActual > 0:
            self.infiltAbajo(1)
        return valorSacado

    def construirMonticulo(self, unaLista):
        i = len(unaLista) // 2
        self.tamanoActual = len(unaLista)
        self.listaMonticulo = [0] + unaLista[:]
        while i > 0:
            self.infiltAbajo(i)
            i -= 1

    def esta_vacio(self):
        return self.tamanoActual == 0

    def tamano(self):
        return self.tamanoActual

    def ver_lista_interna(self):
        return self.listaMonticulo[1:]