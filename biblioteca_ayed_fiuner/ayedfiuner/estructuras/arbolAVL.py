from ayedfiuner.estructuras.nodoAVL import NodoAVL


class ArbolAVL:
    """
    Árbol AVL que ordena nodos por fecha (datetime).
    Estructura de datos genérica de propósito general.
    """

    def __init__(self):
        """
        Precondición:
            - Ninguna.
        Postcondición:
            - Se crea un árbol AVL vacío con raíz None y contador en 0.
        """
        self.raiz      = None
        self._cantidad = 0

    def _altura(self, nodo):
        """
        Precondición:
            - nodo puede ser None o una instancia de NodoAVL.
        Postcondición:
            - Retorna 0 si nodo es None; de lo contrario, retorna nodo.altura (>= 1).
        """
        return 0 if nodo is None else nodo.altura

    def _actualizar_altura(self, nodo):
        """
        Precondición:
            - nodo es una instancia válida de NodoAVL (no None).
            - Los hijos de nodo, si existen, tienen alturas correctas.
        Postcondición:
            - nodo.altura queda igual a 1 + max(altura_izq, altura_der).
        """
        nodo.altura = 1 + max(self._altura(nodo.izquierdo),
                              self._altura(nodo.derecho))

    def _factor_balance(self, nodo):
        """
        Precondición:
            - nodo puede ser None o una instancia de NodoAVL con altura actualizada.
        Postcondición:
            - Retorna 0 si nodo es None.
            - Retorna altura_izquierdo - altura_derecho (puede ser negativo).
        """
        return 0 if nodo is None else (self._altura(nodo.izquierdo)
                                       - self._altura(nodo.derecho))

    def _rotar_derecha(self, z):
        """
        Precondición:
            - z es un NodoAVL no None con hijo izquierdo no None.
        Postcondición:
            - Retorna el nuevo nodo raíz del subárbol (y).
            - Las alturas de z e y quedan actualizadas correctamente.
        """
        y, T3       = z.izquierdo, z.izquierdo.derecho
        y.derecho   = z
        z.izquierdo = T3
        self._actualizar_altura(z)
        self._actualizar_altura(y)
        return y

    def _rotar_izquierda(self, z):
        """
        Precondición:
            - z es un NodoAVL no None con hijo derecho no None.
        Postcondición:
            - Retorna el nuevo nodo raíz del subárbol (y).
            - Las alturas de z e y quedan actualizadas correctamente.
        """
        y, T2       = z.derecho, z.derecho.izquierdo
        y.izquierdo = z
        z.derecho   = T2
        self._actualizar_altura(z)
        self._actualizar_altura(y)
        return y

    def _rebalancear(self, nodo):
        """
        Precondición:
            - nodo es un NodoAVL no None.
        Postcondición:
            - Retorna el nodo raíz del subárbol, posiblemente nuevo tras una rotación.
            - El subárbol resultante queda balanceado (factor de balance en [-1, 1]).
        """
        self._actualizar_altura(nodo)
        b = self._factor_balance(nodo)
        if b > 1  and self._factor_balance(nodo.izquierdo) >= 0:
            return self._rotar_derecha(nodo)
        if b > 1  and self._factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)
        if b < -1 and self._factor_balance(nodo.derecho) <= 0:
            return self._rotar_izquierda(nodo)
        if b < -1 and self._factor_balance(nodo.derecho) > 0:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)
        return nodo

    def _insertar(self, nodo, fecha, temperatura):
        """
        Precondición:
            - fecha es un datetime válido.
            - temperatura es un float.
            - nodo puede ser None o un NodoAVL válido.
        Postcondición:
            - Si fecha no existía, se crea un nuevo NodoAVL y self._cantidad aumenta en 1.
            - Si fecha ya existía, su temperatura se actualiza sin alterar self._cantidad.
            - Retorna la nueva raíz del subárbol, balanceada.
        """
        if nodo is None:
            self._cantidad += 1
            return NodoAVL(fecha, temperatura)
        if   fecha < nodo.fecha:
            nodo.izquierdo = self._insertar(nodo.izquierdo, fecha, temperatura)
        elif fecha > nodo.fecha:
            nodo.derecho   = self._insertar(nodo.derecho,   fecha, temperatura)
        else:
            nodo.temperatura = temperatura
            return nodo
        return self._rebalancear(nodo)

    def _buscar(self, nodo, fecha):
        """
        Precondición:
            - fecha es un datetime válido.
            - nodo puede ser None o un NodoAVL válido.
        Postcondición:
            - Retorna el NodoAVL cuya fecha coincide, o None si no existe.
        """
        if nodo is None or fecha == nodo.fecha:
            return nodo
        return self._buscar(
            nodo.izquierdo if fecha < nodo.fecha else nodo.derecho, fecha)

    def _minimo_nodo(self, nodo):
        """
        Precondición:
            - nodo es un NodoAVL no None.
        Postcondición:
            - Retorna el NodoAVL con la menor fecha en el subárbol.
        """
        while nodo.izquierdo:
            nodo = nodo.izquierdo
        return nodo

    def _borrar(self, nodo, fecha):
        """
        Precondición:
            - fecha es un datetime válido.
            - nodo puede ser None o un NodoAVL válido.
        Postcondición:
            - Si fecha existía, el nodo es eliminado y self._cantidad disminuye en 1.
            - Retorna la nueva raíz del subárbol, balanceada.
        """
        if nodo is None:
            return None
        if   fecha < nodo.fecha:
            nodo.izquierdo = self._borrar(nodo.izquierdo, fecha)
        elif fecha > nodo.fecha:
            nodo.derecho   = self._borrar(nodo.derecho,   fecha)
        else:
            self._cantidad -= 1
            if not nodo.izquierdo: return nodo.derecho
            if not nodo.derecho:   return nodo.izquierdo
            suc = self._minimo_nodo(nodo.derecho)
            nodo.fecha, nodo.temperatura = suc.fecha, suc.temperatura
            nodo.derecho = self._borrar(nodo.derecho, suc.fecha)
            self._cantidad += 1
        return self._rebalancear(nodo)

    def _rango_inorden(self, nodo, f1, f2, resultado):
        """
        Precondición:
            - nodo puede ser None o un NodoAVL válido.
            - f1 y f2 son datetime válidos con f1 <= f2.
            - resultado es una lista.
        Postcondición:
            - resultado contiene en orden ascendente todos los NodoAVL en [f1, f2].
        """
        if nodo is None: return
        if nodo.fecha > f1: self._rango_inorden(nodo.izquierdo, f1, f2, resultado)
        if f1 <= nodo.fecha <= f2: resultado.append(nodo)
        if nodo.fecha < f2: self._rango_inorden(nodo.derecho,   f1, f2, resultado)

    # -------------------------------------------------------------------------
    # Métodos públicos
    # -------------------------------------------------------------------------

    def insertar(self, fecha, temperatura):
        """
        Precondición:
            - fecha es un datetime válido.
            - temperatura es un float.
        Postcondición:
            - Si fecha no existía, se agrega y self._cantidad aumenta en 1.
            - Si fecha ya existía, su temperatura queda actualizada.
        """
        self.raiz = self._insertar(self.raiz, fecha, temperatura)

    def buscar(self, fecha):
        """
        Precondición:
            - fecha es un datetime válido.
        Postcondición:
            - Retorna el NodoAVL con esa fecha, o None si no existe.
        """
        return self._buscar(self.raiz, fecha)

    def borrar(self, fecha):
        """
        Precondición:
            - fecha es un datetime válido.
        Postcondición:
            - Si fecha existía, el nodo es eliminado y self._cantidad disminuye en 1.
        """
        self.raiz = self._borrar(self.raiz, fecha)

    def rango(self, f1, f2):
        """
        Precondición:
            - f1 y f2 son datetime válidos con f1 <= f2.
        Postcondición:
            - Retorna lista de NodoAVL ordenados por fecha en el intervalo [f1, f2].
        """
        r = []
        self._rango_inorden(self.raiz, f1, f2, r)
        return r

    def cantidad(self):
        """
        Postcondición:
            - Retorna un entero >= 0 igual al número de nodos almacenados.
        """
        return self._cantidad