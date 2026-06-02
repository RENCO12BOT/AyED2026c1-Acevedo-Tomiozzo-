import sys

class Vertice:
    """
    Representa un nodo del grafo.
    Guarda sus vecinos y la ponderación de cada arista.
    """

    def __init__(self, clave):
        self.id = clave
        self.conectadoA = {}
        self.color = 'blanco'
        self.distancia = sys.maxsize
        self.predecesor = None

    def agregarVecino(self, vecino, ponderacion=0):
        self.conectadoA[vecino] = ponderacion

    def obtenerConexiones(self):
        return self.conectadoA.keys()

    def obtenerPonderacion(self, vecino):
        return self.conectadoA[vecino]

    def obtenerId(self):
        return self.id

    def asignarColor(self, color):
        self.color = color

    def obtenerColor(self):
        return self.color

    def asignarDistancia(self, d):
        self.distancia = d

    def obtenerDistancia(self):
        return self.distancia

    def asignarPredecesor(self, p):
        self.predecesor = p

    def obtenerPredecesor(self):
        return self.predecesor

    def __lt__(self, otro):
        return self.distancia < otro.distancia

    def __str__(self):
        return str(self.id) + ' conectadoA: ' + str([v.id for v in self.conectadoA])