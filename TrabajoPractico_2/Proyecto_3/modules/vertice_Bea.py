from collections import deque  # Cola estándar de Python

class verticeBEA:
    def __init__(self,):
        self.__vertice__ = {}   # vecinos conectados
        self.__distancia__ = 0  # distancia desde el inicio

    #métodos de color (estado del vértice en BEA)
    def asignarColor(self, color):
        self.__color__ = color

    def obtenerColor(self):
        return getattr(self, '__color__', 'blanco')  # blanco por defecto

    #métodos de distancia
    def asignarDistancia(self, d):
        self.__distancia__ = d

    def obtenerDistancia(self):
        return self.__distancia__

    #métodos de predecesor (para reconstruir el camino)
    def asignarPredecesor(self, p):
        self.__predecesor__ = p

    def obtenerPredecesor(self):
        return getattr(self, '__predecesor__', None)

    #conexiones del vértice   
    def agregarConexion(self, vecino):
        self.__vertice__[vecino] = True

    def obtenerConexiones(self):
        return self.__vertice__.keys()  # devuelve los vecinos


class Cola:
    """Cola FIFO usando deque para O(1) en ambos extremos."""
    def __init__(self):
        self._datos = deque()

    def agregar(self, item):   # encolar
        self._datos.append(item)

    def avanzar(self):         # desencolar
        return self._datos.popleft()

    def tamano(self):
        return len(self._datos)


def bea(g, inicio):
    """
    Búsqueda en Anchura (BEA / BFS).
    Recorre el grafo nivel por nivel desde 'inicio'.
    Asigna distancia y predecesor a cada vértice alcanzado.
    """
    inicio.asignarDistancia(0)          # el inicio está a distancia 0
    inicio.asignarPredecesor(None)      # no tiene predecesor

    colaVertices = Cola()
    colaVertices.agregar(inicio)        # arrancamos con el vértice inicial

    while (colaVertices.tamano() > 0):                      # mientras haya vértices por visitar
        verticeActual = colaVertices.avanzar()              # sacamos el siguiente

        for vecino in verticeActual.obtenerConexiones():    # revisamos sus vecinos
            if (vecino.obtenerColor() == 'blanco'):         # si no fue visitado
                vecino.asignarColor('gris')                             # lo marcamos como "en proceso"
                vecino.asignarDistancia(verticeActual.obtenerDistancia() + 1)  # distancia = padre + 1
                vecino.asignarPredecesor(verticeActual)                 # guardamos de dónde venimos
                colaVertices.agregar(vecino)                            # lo encolamos para procesarlo

        verticeActual.asignarColor('negro')                 # terminamos con este vértice

