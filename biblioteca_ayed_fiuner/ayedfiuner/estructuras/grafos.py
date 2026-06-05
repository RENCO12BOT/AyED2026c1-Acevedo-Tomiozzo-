import heapq
import sys
from ayedfiuner.estructuras.vertice import Vertice

class Grafo:
    """
    Grafo no dirigido representado como lista de adyacencias.
    Cada clave del diccionario es el id de un vértice;
    su valor es el objeto Vertice correspondiente.
    """

    def __init__(self):
        """
        Postcondición:
            - Se crea un grafo vacío sin vértices ni aristas.
        """
        self.listaVertices = {}
        self.numVertices = 0

    def agregarVertice(self, clave):
        """
        Precondición:
            - clave es un string no vacío.
        Postcondición:
            - Si clave no existía, se agrega un nuevo Vertice y numVertices aumenta en 1.
            - Si ya existía, no se modifica nada.
        Retorna el Vertice (nuevo o existente).
        """
        if not isinstance(clave, str) or not clave.strip():
            raise ValueError(f"La clave debe ser un string no vacío. Se recibió: {repr(clave)}")
        if clave not in self.listaVertices:
            self.numVertices += 1
            self.listaVertices[clave] = Vertice(clave)
        return self.listaVertices[clave]

    def obtenerVertice(self, n):
        """
        Precondición:
            - n es un string.
        Postcondición:
            - Retorna el Vertice con id 'n', o None si no existe.
        """
        return self.listaVertices.get(n, None)

    def agregarArista(self, de, a, costo=0):
        """
        Agrega una arista NO DIRIGIDA entre 'de' y 'a' con peso 'costo'.

        Precondición:
            - de y a son strings no vacíos.
            - costo es un entero >= 0.
        Postcondición:
            - Si algún vértice no existía, se crea automáticamente.
            - Se agrega la arista en ambas direcciones (de→a y a→de).
        """
        if not isinstance(costo, (int, float)) or costo < 0:
            raise ValueError(f"El costo debe ser un número >= 0. Se recibió: {costo}")
        v_de = self.agregarVertice(de)
        v_a  = self.agregarVertice(a)
        v_de.agregarVecino(v_a, costo)
        v_a.agregarVecino(v_de, costo)   # no dirigido: arista en ambas direcciones

    def obtenerVertices(self):
        """Postcondición: retorna las claves (ids) de todos los vértices."""
        return self.listaVertices.keys()

    def __iter__(self):
        """Permite recorrer el grafo con un for (itera sobre objetos Vertice)."""
        return iter(self.listaVertices.values())

    def __contains__(self, n):
        """Permite usar 'in' para verificar si un vértice existe por su id."""
        return n in self.listaVertices


def prim(grafo, inicio):
    """
    Árbol de Expansión Mínima (MST) desde 'inicio' usando el algoritmo de Prim.

    Precondición:
        - grafo es una instancia de Grafo no vacía.
        - inicio es un Vertice perteneciente al grafo.
    Postcondición:
        - Cada vértice alcanzable tiene asignado su predecesor (el vértice del MST
          desde el cual se conecta) y su distancia (peso de esa arista).
        - Los vértices no alcanzables conservan distancia=sys.maxsize y predecesor=None.
    """
    if not isinstance(grafo, Grafo):
        raise TypeError("grafo debe ser una instancia de Grafo.")
    if not isinstance(inicio, Vertice):
        raise TypeError("inicio debe ser una instancia de Vertice.")
    if inicio.obtenerId() not in grafo:
        raise ValueError(f"El vértice '{inicio.obtenerId()}' no pertenece al grafo.")

    # Inicializar todos los vértices
    for v in grafo:
        v.asignarDistancia(sys.maxsize)
        v.asignarPredecesor(None)

    inicio.asignarDistancia(0)
    colaPrioridad = [(0, inicio)]
    visitados = set()

    while colaPrioridad:
        _, verticeActual = heapq.heappop(colaPrioridad)

        if verticeActual.obtenerId() in visitados:
            continue
        visitados.add(verticeActual.obtenerId())

        for vecino in verticeActual.obtenerConexiones():
            costo = verticeActual.obtenerPonderacion(vecino)
            if vecino.obtenerId() not in visitados and costo < vecino.obtenerDistancia():
                vecino.asignarPredecesor(verticeActual)
                vecino.asignarDistancia(costo)
                heapq.heappush(colaPrioridad, (costo, vecino))