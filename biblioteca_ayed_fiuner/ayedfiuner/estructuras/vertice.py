import sys

class Vertice:
    """
    Representa un nodo del grafo.
    Guarda sus vecinos y la ponderación de cada arista.
    """

    def __init__(self, clave):
        """
        Precondición:
            - clave es un string no vacío que identifica al vértice.
        Postcondición:
            - Se crea un vértice con id=clave, sin vecinos,
              distancia=sys.maxsize, predecesor=None, color='blanco'.
        """
        if not isinstance(clave, str) or not clave.strip():
            raise ValueError(f"La clave debe ser un string no vacío. Se recibió: {repr(clave)}")
        self.id = clave
        self.conectadoA = {}
        self.color = 'blanco'
        self.distancia = sys.maxsize
        self.predecesor = None

    def agregarVecino(self, vecino, ponderacion=0):
        """
        Precondición:
            - vecino es una instancia de Vertice.
            - ponderacion es un entero >= 0.
        Postcondición:
            - vecino queda registrado en conectadoA con su ponderación.
        """
        if not isinstance(vecino, Vertice):
            raise TypeError(f"El vecino debe ser un Vertice. Se recibió: {type(vecino)}")
        if not isinstance(ponderacion, (int, float)) or ponderacion < 0:
            raise ValueError(f"La ponderación debe ser un número >= 0. Se recibió: {ponderacion}")
        self.conectadoA[vecino] = ponderacion

    def obtenerConexiones(self):
        """
        Postcondición:
            - Retorna las claves (vértices vecinos) del diccionario conectadoA.
        """
        return self.conectadoA.keys()

    def obtenerPonderacion(self, vecino):
        """
        Precondición:
            - vecino es un Vertice presente en conectadoA.
        Postcondición:
            - Retorna el peso de la arista hacia vecino.
        Excepción:
            - KeyError si vecino no es vecino de este vértice.
        """
        if vecino not in self.conectadoA:
            raise KeyError(f"'{vecino.obtenerId()}' no es vecino de '{self.id}'")
        return self.conectadoA[vecino]

    def obtenerId(self):
        """Postcondición: retorna el id del vértice."""
        return self.id

    def asignarColor(self, color):
        """
        Precondición:
            - color es uno de: 'blanco', 'gris', 'negro'.
        Postcondición:
            - self.color queda igual al valor recibido.
        """
        if color not in ('blanco', 'gris', 'negro'):
            raise ValueError(f"Color inválido: '{color}'. Debe ser 'blanco', 'gris' o 'negro'.")
        self.color = color

    def obtenerColor(self):
        """Postcondición: retorna el color actual del vértice."""
        return self.color

    def asignarDistancia(self, d):
        """
        Precondición:
            - d es un número >= 0 o sys.maxsize.
        Postcondición:
            - self.distancia queda igual a d.
        """
        if not isinstance(d, (int, float)):
            raise TypeError(f"La distancia debe ser numérica. Se recibió: {type(d)}")
        self.distancia = d

    def obtenerDistancia(self):
        """Postcondición: retorna la distancia actual del vértice."""
        return self.distancia

    def asignarPredecesor(self, p):
        """
        Precondición:
            - p es una instancia de Vertice o None.
        Postcondición:
            - self.predecesor queda igual a p.
        """
        if p is not None and not isinstance(p, Vertice):
            raise TypeError(f"El predecesor debe ser un Vertice o None. Se recibió: {type(p)}")
        self.predecesor = p

    def obtenerPredecesor(self):
        """Postcondición: retorna el predecesor o None."""
        return self.predecesor

    def __lt__(self, otro):
        """Necesario para que heapq pueda comparar vértices por distancia."""
        if not isinstance(otro, Vertice):
            raise TypeError(f"No se puede comparar Vertice con {type(otro)}")
        return self.distancia < otro.distancia

    def __str__(self):
        return str(self.id) + ' conectadoA: ' + str([v.id for v in self.conectadoA])