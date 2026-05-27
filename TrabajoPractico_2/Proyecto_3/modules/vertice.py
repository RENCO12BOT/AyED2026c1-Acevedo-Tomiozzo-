class Vertice:
    """
    Representa un nodo del grafo.
    Guarda sus vecinos y la ponderación de cada arista.
    """

    def __init__(self, clave):
        self.id = clave             # identificador del vértice
        self.conectadoA = {}        # {vecino: ponderacion}

        # atributos usados en algoritmos de recorrido
        self.color = 'blanco'       # blanco=no visitado, gris=en proceso, negro=terminado
        self.distancia = 0          # distancia desde el vértice de inicio
        self.predecesor = None      # vértice anterior en el camino

    # vecinos
    def agregarVecino(self, vecino, ponderacion=0):
        """Conecta este vértice con 'vecino' con un peso opcional."""
        self.conectadoA[vecino] = ponderacion

    def obtenerConexiones(self):
        """Devuelve todos los vértices vecinos."""
        return self.conectadoA.keys()

    def obtenerPonderacion(self, vecino):
        """Devuelve el peso de la arista hacia 'vecino'."""
        return self.conectadoA[vecino]

    # identificador
    def obtenerId(self):
        return self.id

    # color (estado del vértice en BEA/BEP)
    def asignarColor(self, color):
        self.color = color

    def obtenerColor(self):
        return self.color

    # distancia (usada en BEA y Dijkstra)
    def asignarDistancia(self, d):
        self.distancia = d

    def obtenerDistancia(self):
        return self.distancia

    # predecesor (para reconstruir el camino)
    def asignarPredecesor(self, p):
        self.predecesor = p

    def obtenerPredecesor(self):
        return self.predecesor

    def __str__(self):
        return str(self.id) + ' conectadoA: ' + str([v.id for v in self.conectadoA])