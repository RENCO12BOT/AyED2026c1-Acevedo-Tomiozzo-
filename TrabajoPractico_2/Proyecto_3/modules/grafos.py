from vertice import Vertice

class Grafo:
    """
    Grafo representado como lista de adyacencias.
    Cada clave del diccionario es el id de un vértice;
    su valor es el objeto Vertice correspondiente.
    """

    def __init__(self):
        self.listaVertices = {}     # {id: Vertice}
        self.numVertices = 0        # cantidad de vértices

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

        # conecta el vértice origen con el destino
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


#Ejemplo de uso 
if __name__ == '__main__':
    g = Grafo()

    # armamos un grafo de ciudades
    for ciudad in ['A', 'B', 'C', 'D']:
        g.agregarVertice(ciudad)

    g.agregarArista('A', 'B', 4)
    g.agregarArista('A', 'C', 2)
    g.agregarArista('B', 'D', 5)
    g.agregarArista('C', 'D', 1)

    print("Vértices:", list(g.obtenerVertices()))
    for v in g:
        print(v)