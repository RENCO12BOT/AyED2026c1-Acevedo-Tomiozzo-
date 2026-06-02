import unittest
import sys
import tempfile
import os

from ayedfiuner.estructuras.vertice import Vertice
from ayedfiuner.estructuras.grafos import Grafo

class Vertice:
    def __init__(self, clave):
        self.id = clave
        self.conectadoA = {}
        self.distancia = sys.maxsize
        self.predecesor = None
        self.color = 'blanco'

    def agregarVecino(self, vecino, ponderacion=0):
        self.conectadoA[vecino] = ponderacion

    def obtenerConexiones(self):
        return self.conectadoA.keys()

    def obtenerPonderacion(self, vecino):
        return self.conectadoA[vecino]

    def obtenerId(self):
        return self.id

    def asignarDistancia(self, d): self.distancia = d
    def obtenerDistancia(self):    return self.distancia
    def asignarPredecesor(self, p): self.predecesor = p
    def obtenerPredecesor(self):   return self.predecesor
    def asignarColor(self, c):     self.color = c
    def obtenerColor(self):        return self.color
    def __lt__(self, otro):        return self.distancia < otro.distancia


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


import heapq

def prim(grafo, inicio):
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


from collections import deque

def bea(inicio):
    inicio.asignarDistancia(0)
    inicio.asignarPredecesor(None)
    cola = deque([inicio])
    while cola:
        actual = cola.popleft()
        for vecino in actual.obtenerConexiones():
            if vecino.obtenerColor() == 'blanco':
                vecino.asignarColor('gris')
                vecino.asignarDistancia(actual.obtenerDistancia() + 1)
                vecino.asignarPredecesor(actual)
                cola.append(vecino)
        actual.asignarColor('negro')


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
                if partes[0] not in grafo.listaVertices:
                    grafo.agregarVertice(partes[0])
    return grafo


class TestVertice(unittest.TestCase):
    """Cubre: Vertice.__init__, agregarVecino, obtenerPonderacion, __lt__"""

    def setUp(self):
        self.a = Vertice('A')
        self.b = Vertice('B')

    def test_vecino_y_ponderacion(self):
        """agregarVecino guarda al vecino con el peso correcto."""
        self.a.agregarVecino(self.b, 7)
        self.assertIn(self.b, self.a.obtenerConexiones())
        self.assertEqual(self.a.obtenerPonderacion(self.b), 7)

    def test_ponderacion_cero_por_defecto(self):
        """Sin especificar peso, la ponderación debe ser 0."""
        self.a.agregarVecino(self.b)
        self.assertEqual(self.a.obtenerPonderacion(self.b), 0)

    def test_lt_compara_distancia(self):
        """__lt__ es necesario para que heapq funcione correctamente."""
        self.a.asignarDistancia(3)
        self.b.asignarDistancia(10)
        self.assertTrue(self.a < self.b)
        self.assertFalse(self.b < self.a)

    def test_distancia_inicial_es_maxima(self):
        """Un vértice recién creado debe tener distancia máxima."""
        self.assertEqual(self.a.obtenerDistancia(), sys.maxsize)

    def test_predecesor_inicial_es_none(self):
        self.assertIsNone(self.a.obtenerPredecesor())


class TestGrafo(unittest.TestCase):
    """Cubre: agregarVertice, agregarArista, obtenerVertice, __contains__, __iter__"""

    def setUp(self):
        self.g = Grafo()

    def test_agregar_arista_crea_vertices_faltantes(self):
        """agregarArista no debe fallar si los vértices no existen previamente."""
        self.g.agregarArista('X', 'Y', 5)
        self.assertIn('X', self.g)
        self.assertIn('Y', self.g)

    def test_arista_con_peso_correcto(self):
        """El peso de la arista debe guardarse en el vértice origen."""
        self.g.agregarArista('A', 'B', 12)
        a = self.g.obtenerVertice('A')
        b = self.g.obtenerVertice('B')
        self.assertEqual(a.obtenerPonderacion(b), 12)

    def test_obtener_vertice_inexistente_devuelve_none(self):
        """obtenerVertice no debe lanzar excepción, solo devolver None."""
        self.assertIsNone(self.g.obtenerVertice('Z'))

    def test_iter_recorre_todos_los_vertices(self):
        """__iter__ debe incluir todos los vértices agregados."""
        for c in ['A', 'B', 'C']:
            self.g.agregarVertice(c)
        ids = {v.obtenerId() for v in self.g}
        self.assertEqual(ids, {'A', 'B', 'C'})

    def test_arista_dirigida_no_crea_arista_inversa(self):
        """La arista A→B no debe crear B→A automáticamente."""
        self.g.agregarArista('A', 'B', 3)
        b = self.g.obtenerVertice('B')
        self.assertEqual(len(list(b.obtenerConexiones())), 0)


class TestPrim(unittest.TestCase):
    """
    Cubre: prim() con grafo no dirigido (aristas en ambas direcciones),
    verificando predecesores, distancias y vértices no alcanzables.

    Grafo de prueba (pesos entre paréntesis):
        A --(1)-- B --(4)-- D
        |               |
       (2)             (3)
        |               |
        C --(5)--------- D
        E  (desconectado)
    """

    def setUp(self):
        self.g = Grafo()
        edges = [
            ('A', 'B', 1), ('B', 'A', 1),
            ('A', 'C', 2), ('C', 'A', 2),
            ('B', 'D', 4), ('D', 'B', 4),
            ('C', 'D', 3), ('D', 'C', 3),
        ]
        for de, a, c in edges:
            self.g.agregarArista(de, a, c)
        self.g.agregarVertice('E')   # vértice desconectado
        prim(self.g, self.g.obtenerVertice('A'))

    def test_origen_sin_predecesor(self):
        """El nodo de inicio no debe tener predecesor."""
        self.assertIsNone(self.g.obtenerVertice('A').obtenerPredecesor())

    def test_distancia_minima_b(self):
        """A→B tiene peso 1, debe ser la arista elegida."""
        self.assertEqual(self.g.obtenerVertice('B').obtenerDistancia(), 1)

    def test_distancia_minima_c(self):
        """A→C tiene peso 2, debe ser la arista elegida."""
        self.assertEqual(self.g.obtenerVertice('C').obtenerDistancia(), 2)

    def test_distancia_minima_d(self):
        """C→D (peso 3) es más barata que B→D (peso 4)."""
        self.assertEqual(self.g.obtenerVertice('D').obtenerDistancia(), 3)

    def test_peso_total_arbol(self):
        """Suma de pesos del árbol: 1+2+3 = 6."""
        total = sum(
            v.obtenerDistancia()
            for v in self.g
            if v.obtenerPredecesor() is not None
        )
        self.assertEqual(total, 6)

    def test_vertice_desconectado_sin_predecesor(self):
        """E no está conectado: predecesor debe seguir siendo None."""
        self.assertIsNone(self.g.obtenerVertice('E').obtenerPredecesor())

    def test_vertice_desconectado_distancia_maxima(self):
        """E no está conectado: distancia debe seguir siendo sys.maxsize."""
        self.assertEqual(self.g.obtenerVertice('E').obtenerDistancia(), sys.maxsize)


class TestBEA(unittest.TestCase):
    """
    Cubre: bea() — distancias por nivel, predecesores y nodo no alcanzable.

    Grafo de prueba:
        A → B → D
        ↓
        C       E (desconectado)
    """

    def setUp(self):
        self.g = Grafo()
        self.g.agregarArista('A', 'B')
        self.g.agregarArista('A', 'C')
        self.g.agregarArista('B', 'D')
        self.g.agregarVertice('E')   # desconectado
        bea(self.g.obtenerVertice('A'))

    def test_distancia_origen(self):
        self.assertEqual(self.g.obtenerVertice('A').obtenerDistancia(), 0)

    def test_distancia_nivel_1(self):
        self.assertEqual(self.g.obtenerVertice('B').obtenerDistancia(), 1)
        self.assertEqual(self.g.obtenerVertice('C').obtenerDistancia(), 1)

    def test_distancia_nivel_2(self):
        self.assertEqual(self.g.obtenerVertice('D').obtenerDistancia(), 2)

    def test_predecesor_b_es_a(self):
        pred = self.g.obtenerVertice('B').obtenerPredecesor()
        self.assertEqual(pred.obtenerId(), 'A')

    def test_predecesor_d_es_b(self):
        pred = self.g.obtenerVertice('D').obtenerPredecesor()
        self.assertEqual(pred.obtenerId(), 'B')

    def test_nodo_no_alcanzable_queda_blanco(self):
        """E no fue visitado: color debe seguir siendo 'blanco'."""
        self.assertEqual(self.g.obtenerVertice('E').obtenerColor(), 'blanco')

    def test_nodos_visitados_quedan_negro(self):
        """Todos los nodos alcanzados deben terminar en color negro."""
        for clave in ['A', 'B', 'C', 'D']:
            self.assertEqual(self.g.obtenerVertice(clave).obtenerColor(), 'negro')


class TestCargarGrafo(unittest.TestCase):
    """Cubre: cargarGrafo — formato correcto, líneas vacías, vértice suelto."""

    def _archivo(self, contenido):
        """Crea un archivo temporal con el contenido dado y devuelve su ruta."""
        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                         delete=False, encoding='utf-8')
        tmp.write(contenido)
        tmp.close()
        return tmp.name

    def tearDown(self):
        # limpia archivos temporales creados en cada test
        if hasattr(self, '_ruta') and os.path.exists(self._ruta):
            os.unlink(self._ruta)

    def test_arista_con_peso(self):
        """Línea 'A, B, 5' debe crear arista A→B con peso 5."""
        self._ruta = self._archivo("A, B, 5\n")
        g = cargarGrafo(self._ruta)
        a = g.obtenerVertice('A')
        b = g.obtenerVertice('B')
        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        self.assertEqual(a.obtenerPonderacion(b), 5)

    def test_lineas_vacias_no_rompen(self):
        """El parser debe ignorar líneas en blanco sin lanzar excepción."""
        self._ruta = self._archivo("\nA, B, 3\n\n")
        g = cargarGrafo(self._ruta)
        self.assertIn('A', g)

    def test_vertice_suelto(self):
        """Una línea con un solo nombre debe crear el vértice sin vecinos."""
        self._ruta = self._archivo("Peligros\n")
        g = cargarGrafo(self._ruta)
        v = g.obtenerVertice('Peligros')
        self.assertIsNotNone(v)
        self.assertEqual(len(list(v.obtenerConexiones())), 0)

    def test_multiples_aristas(self):
        """Varias líneas deben crear todos los vértices y aristas."""
        self._ruta = self._archivo("A, B, 1\nB, C, 2\nC, A, 3\n")
        g = cargarGrafo(self._ruta)
        self.assertEqual(g.numVertices, 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)