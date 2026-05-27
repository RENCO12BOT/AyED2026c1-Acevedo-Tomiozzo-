import heapq
import sys

#Clase Vertice

class Vertice:
    def __init__(self, clave):
        self.id = clave
        self.conectadoA = {}        # {vecino: ponderacion}
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

    def asignarDistancia(self, d):
        self.distancia = d

    def obtenerDistancia(self):
        return self.distancia

    def asignarPredecesor(self, p):
        self.predecesor = p

    def obtenerPredecesor(self):
        return self.predecesor

    def __lt__(self, otro):         # necesario para heapq
        return self.distancia < otro.distancia


#Clase Grafo 

class Grafo:
    def __init__(self):
        self.listaVertices = {}
        self.numVertices = 0

    def agregarVertice(self, clave):
        self.numVertices += 1
        nuevo = Vertice(clave)
        self.listaVertices[clave] = nuevo
        return nuevo

    def obtenerVertice(self, n):
        return self.listaVertices.get(n, None)

    def agregarArista(self, de, a, costo=0):
        if de not in self.listaVertices:
            self.agregarVertice(de)
        if a not in self.listaVertices:
            self.agregarVertice(a)
        self.listaVertices[de].agregarVecino(self.listaVertices[a], costo)

    def obtenerVertices(self):
        return self.listaVertices.keys()

    def __iter__(self):
        return iter(self.listaVertices.values())

    def __contains__(self, n):
        return n in self.listaVertices


#Algoritmo de Prim 

def prim(grafo, inicio):
    """
    Árbol de expansión mínima desde 'inicio'.
    Retorna el conjunto de aristas del árbol como lista de tuplas
    (predecesor, vertice, costo).
    """
    for v in grafo:
        v.asignarDistancia(sys.maxsize)
        v.asignarPredecesor(None)

    inicio.asignarDistancia(0)

    # montículo de prioridad: (distancia, vertice)
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

# Leer aldeas.txt y recorrer el archvio de aldeas

def cargarGrafo(ruta):
    grafo = Grafo()
    with open(ruta, encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            partes = [p.strip() for p in linea.split(',')]
            if len(partes) == 3:
                origen, destino, costo = partes
                grafo.agregarArista(origen, destino, int(costo))
            elif len(partes) == 1:
                # vértice sin conexiones en esa línea
                if partes[0] not in grafo.listaVertices:
                    grafo.agregarVertice(partes[0])
    return grafo

# Main

def main():
    grafo = cargarGrafo('/mnt/user-data/uploads/aldeas.txt')
    inicio = grafo.obtenerVertice('Peligros')

    if inicio is None:
        print("No se encontró el vértice 'Peligros'")
        return

    prim(grafo, inicio)

    # 1. Lista de aldeas en orden alfabético
    print("=" * 60)
    print("ALDEAS EN ORDEN ALFABÉTICO")
    print("=" * 60)
    aldeas_ordenadas = sorted(grafo.obtenerVertices())
    for a in aldeas_ordenadas:
        print(f"  {a}")

    # 2. Para cada aldea: de quién recibe y a quiénes envía réplicas
    # Construimos el árbol: predecesor -> [hijos]
    hijos = {v: [] for v in grafo.obtenerVertices()}
    for v in grafo:
        if v.obtenerPredecesor() is not None:
            padre_id = v.obtenerPredecesor().obtenerId()
            hijos[padre_id].append(v.obtenerId())

    print()
    print("=" * 60)
    print("ÁRBOL DE DISTRIBUCIÓN (Prim desde Peligros)")
    print("=" * 60)

    distancia_total_global = 0

    for aldea_id in aldeas_ordenadas:
        v = grafo.obtenerVertice(aldea_id)
        pred = v.obtenerPredecesor()
        envios = sorted(hijos[aldea_id])

        if aldea_id == 'Peligros':
            recibe_de = "— (origen)"
        elif pred is None:
            recibe_de = "NO ALCANZABLE"
        else:
            recibe_de = pred.obtenerId()

        if envios:
            envia_a = ', '.join(envios)
        else:
            envia_a = "— (hoja, no reenvía)"

        print(f"\n  {aldea_id}")
        print(f"    Recibe de : {recibe_de}")
        print(f"    Envía a   : {envia_a}")

        # distancia total de palomas enviadas desde esta aldea
        dist_aldea = 0
        for hijo_id in hijos[aldea_id]:
            hijo = grafo.obtenerVertice(hijo_id)
            dist_aldea += hijo.obtenerDistancia()

        if hijos[aldea_id]:
            print(f"    Dist. enviadas: {dist_aldea} leguas")
            distancia_total_global += dist_aldea

    # 3. Suma total de distancias
    print()
    print("=" * 60)
    print(f"DISTANCIA TOTAL RECORRIDA POR TODAS LAS PALOMAS: {distancia_total_global} leguas")
    print("=" * 60)


if __name__ == '__main__':
    main()