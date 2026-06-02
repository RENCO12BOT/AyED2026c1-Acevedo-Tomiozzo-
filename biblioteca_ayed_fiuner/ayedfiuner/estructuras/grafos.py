import heapq
import sys
from ayedfiuner.estructuras.vertice import Vertice

class Grafo:
    """
    Grafo representado como lista de adyacencias.
    Cada clave del diccionario es el id de un vértice;
    su valor es el objeto Vertice correspondiente.
    """

    def __init__(self):
        self.listaVertices = {}
        self.numVertices = 0

    def agregarVertice(self, clave):
        """Crea un nuevo vértice y lo agrega al grafo."""
        self.numVertices += 1
        nuevo = Vertice(clave)
        self.listaVertices[clave] = nuevo
        return nuevo

    def obtenerVertice(self, n):
        """Devuelve el vértice con id 'n', o None si no existe."""
        return self.listaVertices.get(n, None)

    def agregarArista(self, de, a, costo=0):
        """
        Agrega una arista dirigida de 'de' hacia 'a' con peso 'costo'.
        Si alguno de los vértices no existe, lo crea automáticamente.
        """
        if de not in self.listaVertices:
            self.agregarVertice(de)
        if a not in self.listaVertices:
            self.agregarVertice(a)
        self.listaVertices[de].agregarVecino(self.listaVertices[a], costo)

    def obtenerVertices(self):
        """Devuelve todas las claves (ids) de los vértices."""
        return self.listaVertices.keys()

    def __iter__(self):
        """Permite recorrer el grafo con un for."""
        return iter(self.listaVertices.values())

    def __contains__(self, n):
        """Permite usar 'in' para verificar si un vértice existe."""
        return n in self.listaVertices


def prim(grafo, inicio):
    """
    Árbol de expansión mínima desde 'inicio'.
    Algoritmo de Prim usando montículo de prioridad.
    """
    for v in grafo:
        v.asignarDistancia(sys.maxsize)
        v.asignarPredecesor(None)

    inicio.asignarDistancia(0)
    cp = [(0, inicio)]
    visitados = set()

    while cp:
        _, verticeActual = heapq.heappop(cp)
        if verticeActual.obtenerId() in visitados:
            continue
        visitados.add(verticeActual.obtenerId())
        for vecino in verticeActual.obtenerConexiones():
            costo = verticeActual.obtenerPonderacion(vecino)
            if vecino.obtenerId() not in visitados and costo < vecino.obtenerDistancia():
                vecino.asignarPredecesor(verticeActual)
                vecino.asignarDistancia(costo)
                heapq.heappush(cp, (costo, vecino))


if __name__ == '__main__':
    g = Grafo()

    for ciudad in ['A', 'B', 'C', 'D']:
        g.agregarVertice(ciudad)

    g.agregarArista('A', 'B', 4)
    g.agregarArista('A', 'C', 2)
    g.agregarArista('B', 'D', 5)
    g.agregarArista('C', 'D', 1)

    print("Vértices:", list(g.obtenerVertices()))
    for v in g:
        print(v)