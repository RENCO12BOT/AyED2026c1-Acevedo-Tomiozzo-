import heapq
import sys
import os

# ── Vertice ───────────────────────────────────────────────────

class Vertice:
    """
    Nodo del grafo que representa una aldea.

    Atributos:
        id          : identificador único (string con el nombre de la aldea)
        conectadoA  : diccionario {vecino: ponderacion} con las aristas salientes
        distancia   : distancia mínima desde el origen (usada por Prim)
        predecesor  : vértice desde el cual se alcanzó este nodo en el MST
    """

    def __init__(self, clave):
        """
        Precondición  : clave es un string no vacío.
        Postcondición : vértice creado con distancia = sys.maxsize y sin predecesor.
        """
        assert isinstance(clave, str) and len(clave) > 0, \
            "Precondición fallida: clave debe ser un string no vacío"
        self.id         = clave
        self.conectadoA = {}
        self.distancia  = sys.maxsize
        self.predecesor = None

    def agregarVecino(self, vecino, ponderacion=0):
        """
        Precondición  : vecino es una instancia de Vertice; ponderacion es int >= 0.
        Postcondición : vecino queda registrado en conectadoA con su ponderación.
        """
        assert isinstance(vecino, Vertice), \
            "Precondición fallida: vecino debe ser una instancia de Vertice"
        assert isinstance(ponderacion, (int, float)) and ponderacion >= 0, \
            f"Precondición fallida: ponderacion debe ser un número >= 0, se recibió {ponderacion}"
        self.conectadoA[vecino] = ponderacion

    def obtenerConexiones(self):
        """Postcondición: retorna los vértices vecinos (claves del dict conectadoA)."""
        return self.conectadoA.keys()

    def obtenerPonderacion(self, vecino):
        """
        Precondición  : vecino existe en conectadoA.
        Postcondición : retorna el peso de la arista hacia vecino.
        """
        assert vecino in self.conectadoA, \
            f"Precondición fallida: {vecino.obtenerId()} no es vecino de {self.id}"
        return self.conectadoA[vecino]

    def obtenerId(self):
        """Postcondición: retorna el string identificador del vértice."""
        return self.id

    def asignarDistancia(self, d):
        """
        Precondición  : d es un número >= 0 o sys.maxsize.
        Postcondición : self.distancia == d.
        """
        assert isinstance(d, (int, float)) and d >= 0, \
            f"Precondición fallida: d debe ser un número >= 0, se recibió {d}"
        self.distancia = d

    def obtenerDistancia(self):
        """Postcondición: retorna la distancia asignada al vértice."""
        return self.distancia

    def asignarPredecesor(self, p):
        """
        Precondición  : p es una instancia de Vertice o None.
        Postcondición : self.predecesor == p.
        """
        assert p is None or isinstance(p, Vertice), \
            "Precondición fallida: p debe ser un Vertice o None"
        self.predecesor = p

    def obtenerPredecesor(self):
        """Postcondición: retorna el predecesor (Vertice o None)."""
        return self.predecesor

    def __lt__(self, otro):
        """Necesario para heapq cuando dos distancias son iguales."""
        return self.distancia < otro.distancia

    def __str__(self):
        return f"{self.id} -> {[v.id for v in self.conectadoA]}"

# ── Grafo ─────────────────────────────────────────────────────

class Grafo:
    """
    Grafo dirigido y ponderado representado como lista de adyacencias.
    Cada clave del diccionario es el id de un vértice;
    su valor es el objeto Vertice correspondiente.
    """

    def __init__(self):
        """Postcondición: grafo vacío, sin vértices ni aristas."""
        self.listaVertices = {}
        self.numVertices   = 0

    def agregarVertice(self, clave):
        """
        Precondición  : clave es un string no vacío.
        Postcondición : el vértice con ese id existe en el grafo; numVertices aumenta en 1.
        """
        assert isinstance(clave, str) and len(clave) > 0, \
            "Precondición fallida: clave debe ser un string no vacío"
        self.numVertices += 1
        nuevo = Vertice(clave)
        self.listaVertices[clave] = nuevo
        return nuevo

    def obtenerVertice(self, n):
        """
        Precondición  : n es un string.
        Postcondición : retorna el Vertice con id n, o None si no existe.
        """
        assert isinstance(n, str), \
            "Precondición fallida: n debe ser un string"
        return self.listaVertices.get(n, None)

    def agregarArista(self, de, a, costo=0):
        """
        Agrega una arista dirigida de 'de' hacia 'a' con peso 'costo'.
        Si alguno de los vértices no existe, lo crea automáticamente.

        Precondición  : de y a son strings no vacíos; costo es int >= 0.
        Postcondición : existe una arista de->a con el costo dado.
        """
        assert isinstance(de, str) and len(de) > 0, \
            "Precondición fallida: 'de' debe ser un string no vacío"
        assert isinstance(a, str) and len(a) > 0, \
            "Precondición fallida: 'a' debe ser un string no vacío"
        assert isinstance(costo, (int, float)) and costo >= 0, \
            f"Precondición fallida: costo debe ser un número >= 0, se recibió {costo}"

        if de not in self.listaVertices:
            self.agregarVertice(de)
        if a not in self.listaVertices:
            self.agregarVertice(a)
        self.listaVertices[de].agregarVecino(self.listaVertices[a], costo)

    def obtenerVertices(self):
        """Postcondición: retorna las claves (ids) de todos los vértices."""
        return self.listaVertices.keys()

    def __iter__(self):
        """Permite recorrer el grafo con un for."""
        return iter(self.listaVertices.values())

    def __contains__(self, n):
        """Permite usar 'in' para verificar si un vértice existe."""
        return n in self.listaVertices

# ── Algoritmo de Prim ─────────────────────────────────────────

def prim(grafo, inicio):
    """
    Construye el Árbol de Expansión Mínima (MST) desde 'inicio' usando el algoritmo de Prim.
    Modifica en el lugar los atributos distancia y predecesor de cada vértice del grafo.

    Precondiciones:
        - grafo es una instancia de Grafo con al menos un vértice.
        - inicio es una instancia de Vertice que pertenece al grafo.

    Postcondiciones:
        - Cada vértice alcanzable tiene asignado su predecesor en el MST.
        - Cada vértice alcanzable tiene asignada la distancia mínima al MST.
        - El vértice de inicio tiene distancia 0 y predecesor None.
    """
    assert isinstance(grafo, Grafo) and grafo.numVertices > 0, \
        "Precondición fallida: grafo debe ser una instancia de Grafo con al menos un vértice"
    assert isinstance(inicio, Vertice), \
        "Precondición fallida: inicio debe ser una instancia de Vertice"
    assert inicio.obtenerId() in grafo.listaVertices, \
        f"Precondición fallida: el vértice '{inicio.obtenerId()}' no pertenece al grafo"

    # Inicializar todos los vértices
    for v in grafo:
        v.asignarDistancia(sys.maxsize)
        v.asignarPredecesor(None)

    inicio.asignarDistancia(0)

    cp       = [(0, inicio)]   # montículo de prioridad: (distancia, vertice)
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

    # Postcondición: el vértice de inicio siempre queda con distancia 0
    assert inicio.obtenerDistancia() == 0, \
        "Postcondición fallida: el vértice de inicio debería tener distancia 0"

# ── Carga del grafo desde archivo ─────────────────────────────

def cargarGrafo(ruta):
    """
    Lee un archivo de texto con el formato:
        origen, destino, costo
    y construye el grafo correspondiente.
    Las líneas vacías se ignoran.

    Precondiciones:
        - ruta es un string no vacío.
        - El archivo existe y es legible.
        - Cada línea tiene exactamente 3 campos separados por coma,
          donde los dos primeros son strings y el tercero es un entero >= 0.

    Postcondiciones:
        - Retorna un Grafo con todos los vértices y aristas del archivo.
        - Si una línea tiene formato incorrecto, se ignora con un aviso.
    """
    assert isinstance(ruta, str) and len(ruta) > 0, \
        "Precondición fallida: ruta debe ser un string no vacío"
    assert os.path.isfile(ruta), \
        f"Precondición fallida: el archivo '{ruta}' no existe o no es accesible"

    grafo   = Grafo()
    errores = 0

    with open(ruta, encoding='utf-8') as f:
        for num, linea in enumerate(f, start=1):
            linea = linea.strip()
            if not linea:
                continue
            partes = [p.strip() for p in linea.split(',')]
            try:
                if len(partes) != 3:
                    raise ValueError(f"Se esperaban 3 columnas, se encontraron {len(partes)}")
                origen, destino, costo_str = partes
                if not origen or not destino:
                    raise ValueError("El nombre de la aldea no puede estar vacío")
                costo = int(costo_str)
                if costo < 0:
                    raise ValueError(f"El costo debe ser >= 0, se recibió {costo}")
                grafo.agregarArista(origen, destino, costo)
            except (ValueError, AssertionError) as e:
                print(f"  Línea {num} ignorada: {e}")
                errores += 1

    if errores:
        print(f"  Carga completada con {errores} línea(s) con error.")

    # Postcondición: el grafo retornado tiene al menos un vértice
    assert grafo.numVertices > 0, \
        "Postcondición fallida: el archivo no aportó ningún vértice válido"

    return grafo


# ── Main ──────────────────────────────────────────────────────

def main():
    """
    Punto de entrada del programa.
    Lee el grafo de aldeas, aplica Prim desde 'Peligros' y muestra:
        1. Lista de aldeas en orden alfabético.
        2. Para cada aldea: de quién recibe la noticia y a quiénes la reenvía.
        3. Distancia total recorrida por todas las palomas.
    """
    ruta  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aldeas.txt')
    grafo = cargarGrafo(ruta)

    inicio = grafo.obtenerVertice('Peligros')
    if inicio is None:
        raise ValueError("El grafo no contiene el vértice 'Peligros'. Verificar aldeas.txt.")

    prim(grafo, inicio)

    # ── 1. Lista de aldeas en orden alfabético ────────────────
    print("=" * 60)
    print("ALDEAS EN ORDEN ALFABÉTICO")
    print("=" * 60)
    aldeas_ordenadas = sorted(grafo.obtenerVertices())
    for a in aldeas_ordenadas:
        print(f"  {a}")

    # ── 2. Árbol de distribución ──────────────────────────────
    # Construimos el árbol inverso: predecesor -> [hijos]
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
        v      = grafo.obtenerVertice(aldea_id)
        pred   = v.obtenerPredecesor()
        envios = sorted(hijos[aldea_id])

        recibe_de = ("— (origen)"      if aldea_id == 'Peligros'
                     else "NO ALCANZABLE" if pred is None
                     else pred.obtenerId())

        envia_a   = (', '.join(envios) if envios
                     else "— (hoja, no reenvía)")

        print(f"\n  {aldea_id}")
        print(f"    Recibe de : {recibe_de}")
        print(f"    Envía a   : {envia_a}")

        # Distancia total de palomas enviadas desde esta aldea
        dist_aldea = sum(grafo.obtenerVertice(h).obtenerDistancia()
                         for h in hijos[aldea_id])
        if hijos[aldea_id]:
            print(f"    Dist. enviadas: {dist_aldea} leguas")
            distancia_total_global += dist_aldea

    # ── 3. Suma total de distancias ───────────────────────────
    print()
    print("=" * 60)
    print(f"DISTANCIA TOTAL RECORRIDA POR TODAS LAS PALOMAS: {distancia_total_global} leguas")
    print("=" * 60)

if __name__ == '__main__':
    main()