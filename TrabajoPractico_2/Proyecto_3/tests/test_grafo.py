import sys
import os
import unittest
import tempfile

<<<<<<< HEAD
# Ajuste de ruta para importar desde biblioteca_ayed_fiuner
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'biblioteca_ayed_fiuner'))

from ayedfiuner.estructuras.grafos import Grafo, prim


def leer_aldeas(ruta):
    """
    Lee el archivo de aldeas y construye un grafo no dirigido.

    Precondición:
        - ruta es un string con la ruta a un archivo .txt existente.
        - Cada línea válida tiene el formato: "aldea1, aldea2, distancia"
          donde distancia es un entero positivo.
        - Líneas con un solo token (sin comas) son aldeas aisladas
          válidas; se agregan como vértice sin aristas (caso "Diosleguarde").
        - Líneas vacías o con solo espacios se ignoran silenciosamente.

    Postcondición:
        - Retorna un Grafo con todos los vértices y aristas del archivo.
        - Ninguna excepción se propaga por líneas mal formadas:
          se imprime una advertencia y se continúa con la siguiente línea.

    Excepciones:
        - FileNotFoundError si el archivo no existe.
        - TypeError  si ruta no es un string.
    """
    if not isinstance(ruta, str):
        raise TypeError(f"La ruta debe ser un string. Se recibió: {type(ruta)}")
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

=======
from ayedfiuner.estructuras.vertice import Vertice
from ayedfiuner.estructuras.grafos import Grafo, prim
from ayedfiuner.estructuras.vertice_Bea import bea


# ---------------------------------------------------------------------------
# Helper: grafo no dirigido desde lista de tuplas
# ---------------------------------------------------------------------------

def _grafo_desde_aristas(aristas):
    """Construye un Grafo no dirigido a partir de (origen, destino, costo)."""
    g = Grafo()
    for de, a, c in aristas:
        g.agregarArista(de, a, c)
    return g


def cargarGrafo(ruta):
    """Replica la función de Palomas_mensajeras para uso en tests."""
>>>>>>> 1c9ad682ebbe80c39e3f2f8538011f8338857b16
    grafo = Grafo()

    with open(ruta, encoding='utf-8') as f:
        for num_linea, linea in enumerate(f, start=1):
            linea = linea.strip()

            # Línea vacía → ignorar
            if not linea:
                continue

            partes = [p.strip() for p in linea.split(',')]

            # Aldea aislada (sin aristas): solo un token
            if len(partes) == 1:
                grafo.agregarVertice(partes[0])
                continue

            # Línea con exactamente 3 partes: aldea1, aldea2, distancia
            if len(partes) == 3:
<<<<<<< HEAD
                aldea1, aldea2, dist_str = partes
                try:
                    distancia = int(dist_str)
                    if distancia <= 0:
                        raise ValueError("distancia no positiva")
                    grafo.agregarArista(aldea1, aldea2, distancia)
                except ValueError as e:
                    print(f"  [Advertencia] Línea {num_linea} ignorada ({e}): '{linea}'")
                continue

            # Cualquier otro formato → advertencia y continuar
            print(f"  [Advertencia] Línea {num_linea} con formato inesperado ignorada: '{linea}'")

    return grafo


def mostrar_resultados(grafo, origen_id):
    """
    Ejecuta Prim desde 'origen_id' y muestra:
      1. Lista de aldeas en orden alfabético.
      2. Para cada aldea: de quién recibe la noticia y a quiénes reenvía.
      3. Suma total de distancias del MST.

    Precondición:
        - grafo es una instancia de Grafo no vacía.
        - origen_id es un string que existe en el grafo.

    Postcondición:
        - Se imprime por pantalla la información del MST.
        - Retorna la suma total de distancias (int).

    Excepciones:
        - ValueError si origen_id no está en el grafo.
=======
                origen, destino, costo = partes
                grafo.agregarArista(origen, destino, int(costo))
            elif len(partes) == 1:
                grafo.agregarVertice(partes[0])
    return grafo


# ===========================================================================
# Vertice
# ===========================================================================

class TestVertice(unittest.TestCase):
    """Cubre: __init__, agregarVecino, obtenerPonderacion, __lt__, validaciones."""

    def setUp(self):
        self.a = Vertice('A')
        self.b = Vertice('B')

    def test_vecino_y_ponderacion(self):
        self.a.agregarVecino(self.b, 7)
        self.assertIn(self.b, self.a.obtenerConexiones())
        self.assertEqual(self.a.obtenerPonderacion(self.b), 7)

    def test_ponderacion_cero_por_defecto(self):
        self.a.agregarVecino(self.b)
        self.assertEqual(self.a.obtenerPonderacion(self.b), 0)

    def test_lt_compara_distancia(self):
        self.a.asignarDistancia(3)
        self.b.asignarDistancia(10)
        self.assertTrue(self.a < self.b)
        self.assertFalse(self.b < self.a)

    def test_distancia_inicial_es_maxima(self):
        self.assertEqual(self.a.obtenerDistancia(), sys.maxsize)

    def test_predecesor_inicial_es_none(self):
        self.assertIsNone(self.a.obtenerPredecesor())

    def test_clave_vacia_lanza_error(self):
        with self.assertRaises(ValueError):
            Vertice('')

    def test_vecino_tipo_incorrecto_lanza_error(self):
        with self.assertRaises(TypeError):
            self.a.agregarVecino('no_soy_vertice', 5)

    def test_ponderacion_negativa_lanza_error(self):
        with self.assertRaises(ValueError):
            self.a.agregarVecino(self.b, -1)

    def test_obtener_ponderacion_vecino_inexistente(self):
        with self.assertRaises(KeyError):
            self.a.obtenerPonderacion(self.b)

    def test_color_invalido_lanza_error(self):
        with self.assertRaises(ValueError):
            self.a.asignarColor('rojo')


# ===========================================================================
# Grafo
# ===========================================================================

class TestGrafo(unittest.TestCase):
    """Cubre: agregarVertice, agregarArista, obtenerVertice, __contains__, __iter__."""

    def setUp(self):
        self.g = Grafo()

    def test_agregar_arista_crea_vertices_faltantes(self):
        self.g.agregarArista('X', 'Y', 5)
        self.assertIn('X', self.g)
        self.assertIn('Y', self.g)

    def test_arista_no_dirigida_existe_en_ambas_direcciones(self):
        """agregarArista debe crear arista en ambas direcciones."""
        self.g.agregarArista('A', 'B', 12)
        a = self.g.obtenerVertice('A')
        b = self.g.obtenerVertice('B')
        self.assertEqual(a.obtenerPonderacion(b), 12)
        self.assertEqual(b.obtenerPonderacion(a), 12)

    def test_obtener_vertice_inexistente_devuelve_none(self):
        self.assertIsNone(self.g.obtenerVertice('Z'))

    def test_iter_recorre_todos_los_vertices(self):
        for c in ['A', 'B', 'C']:
            self.g.agregarVertice(c)
        ids = {v.obtenerId() for v in self.g}
        self.assertEqual(ids, {'A', 'B', 'C'})

    def test_agregar_vertice_duplicado_no_duplica(self):
        self.g.agregarVertice('A')
        self.g.agregarVertice('A')
        self.assertEqual(self.g.numVertices, 1)

    def test_costo_negativo_lanza_error(self):
        with self.assertRaises(ValueError):
            self.g.agregarArista('A', 'B', -5)


# ===========================================================================
# Prim
# ===========================================================================

class TestPrim(unittest.TestCase):
    """
    Grafo de prueba (no dirigido, pesos entre paréntesis):
        A --(1)-- B --(4)-- D
        |                   |
       (2)                 (3)
        |                   |
        C ---------(5)------ D    (C-D directo)

    MST esperado: A-B(1), A-C(2), C-D(3) → total = 6
    E queda desconectado.
>>>>>>> 1c9ad682ebbe80c39e3f2f8538011f8338857b16
    """
    if not isinstance(origen_id, str):
        raise TypeError(f"origen_id debe ser un string. Se recibió: {type(origen_id)}")
    if origen_id not in grafo:
        raise ValueError(f"La aldea origen '{origen_id}' no existe en el grafo.")

<<<<<<< HEAD
    inicio = grafo.obtenerVertice(origen_id)
    prim(grafo, inicio)

    # Construir árbol: para cada nodo, quiénes son sus hijos en el MST
    hijos = {v.obtenerId(): [] for v in grafo}

    for v in grafo:
        pred = v.obtenerPredecesor()
        if pred is not None:
            hijos[pred.obtenerId()].append(v.obtenerId())

    # Lista alfabética de aldeas
    aldeas_ordenadas = sorted(grafo.obtenerVertices())

    print("=" * 60)
    print("  PALOMAS MENSAJERAS — MST desde '{}'".format(origen_id))
    print("=" * 60)

    print("\n── Lista de aldeas (orden alfabético) ──")
    for aldea in aldeas_ordenadas:
        print(f"   {aldea}")

    print("\n── Flujo de mensajes en el MST ──")
    distancia_total = 0

    for aldea in aldeas_ordenadas:
        v = grafo.obtenerVertice(aldea)
        pred = v.obtenerPredecesor()
        envios = hijos[aldea]
        dist = v.obtenerDistancia()

        if aldea == origen_id:
            recibe_de = "— (es el origen)"
        else:
            recibe_de = pred.obtenerId() if pred else "NO ALCANZABLE"
            distancia_total += dist if dist != sys.maxsize else 0

        if envios:
            envia_a = ", ".join(sorted(envios))
        else:
            envia_a = "— (hoja, no reenvía)"

        print(f"\n  {aldea}")
        print(f"    Recibe de : {recibe_de}")
        print(f"    Reenvía a : {envia_a}")
        if aldea != origen_id and dist != sys.maxsize:
            print(f"    Distancia : {dist} leguas")

    print("\n" + "=" * 60)
    print(f"  Suma total de distancias recorridas: {distancia_total} leguas")
    print("=" * 60)

    return distancia_total
=======
    def setUp(self):
        self.g = _grafo_desde_aristas([
            ('A', 'B', 1),
            ('A', 'C', 2),
            ('B', 'D', 4),
            ('C', 'D', 3),
        ])
        self.g.agregarVertice('E')
        prim(self.g, self.g.obtenerVertice('A'))

    def test_origen_sin_predecesor(self):
        self.assertIsNone(self.g.obtenerVertice('A').obtenerPredecesor())

    def test_distancia_minima_b(self):
        self.assertEqual(self.g.obtenerVertice('B').obtenerDistancia(), 1)

    def test_distancia_minima_c(self):
        self.assertEqual(self.g.obtenerVertice('C').obtenerDistancia(), 2)

    def test_distancia_minima_d_via_c(self):
        """C-D (3) es más barato que B-D (4): D debe entrar por C."""
        self.assertEqual(self.g.obtenerVertice('D').obtenerDistancia(), 3)

    def test_peso_total_arbol(self):
        total = sum(
            v.obtenerDistancia()
            for v in self.g
            if v.obtenerPredecesor() is not None
        )
        self.assertEqual(total, 6)

    def test_vertice_desconectado_sin_predecesor(self):
        self.assertIsNone(self.g.obtenerVertice('E').obtenerPredecesor())

    def test_vertice_desconectado_distancia_maxima(self):
        self.assertEqual(self.g.obtenerVertice('E').obtenerDistancia(), sys.maxsize)

    def test_prim_inicio_fuera_del_grafo_lanza_error(self):
        g2 = Grafo()
        g2.agregarArista('X', 'Y', 1)
        foraneo = Vertice('Z')
        with self.assertRaises(ValueError):
            prim(g2, foraneo)


# ===========================================================================
# BEA (BFS)
# ===========================================================================

class TestBEA(unittest.TestCase):
    """
    Grafo dirigido de prueba:
        A → B → D
        ↓
        C       E (desconectado)
    """

    def setUp(self):
        self.g = Grafo()
        # BEA usa el Grafo como dirigido (agregarArista ya agrega en ambas
        # direcciones; para BEA solo necesitamos la dirección de salida)
        self.g.agregarArista('A', 'B')
        self.g.agregarArista('A', 'C')
        self.g.agregarArista('B', 'D')
        self.g.agregarVertice('E')
        bea(self.g, self.g.obtenerVertice('A'))

    def test_distancia_origen(self):
        self.assertEqual(self.g.obtenerVertice('A').obtenerDistancia(), 0)

    def test_distancia_nivel_1(self):
        self.assertEqual(self.g.obtenerVertice('B').obtenerDistancia(), 1)
        self.assertEqual(self.g.obtenerVertice('C').obtenerDistancia(), 1)

    def test_distancia_nivel_2(self):
        self.assertEqual(self.g.obtenerVertice('D').obtenerDistancia(), 2)

    def test_predecesor_b_es_a(self):
        self.assertEqual(self.g.obtenerVertice('B').obtenerPredecesor().obtenerId(), 'A')

    def test_predecesor_d_es_b(self):
        self.assertEqual(self.g.obtenerVertice('D').obtenerPredecesor().obtenerId(), 'B')

    def test_nodo_no_alcanzable_queda_blanco(self):
        self.assertEqual(self.g.obtenerVertice('E').obtenerColor(), 'blanco')

    def test_nodos_visitados_quedan_negro(self):
        for clave in ['A', 'B', 'C', 'D']:
            self.assertEqual(self.g.obtenerVertice(clave).obtenerColor(), 'negro')


# ===========================================================================
# cargarGrafo
# ===========================================================================

class TestCargarGrafo(unittest.TestCase):
    """Cubre: formato correcto, líneas vacías, vértice suelto, múltiples aristas."""

    def _archivo(self, contenido):
        tmp = tempfile.NamedTemporaryFile(
            mode='w', suffix='.txt', delete=False, encoding='utf-8'
        )
        tmp.write(contenido)
        tmp.close()
        return tmp.name

    def tearDown(self):
        if hasattr(self, '_ruta') and os.path.exists(self._ruta):
            os.unlink(self._ruta)

    def test_arista_con_peso(self):
        self._ruta = self._archivo("A, B, 5\n")
        g = cargarGrafo(self._ruta)
        a = g.obtenerVertice('A')
        b = g.obtenerVertice('B')
        self.assertEqual(a.obtenerPonderacion(b), 5)

    def test_arista_no_dirigida(self):
        """cargarGrafo debe crear aristas en ambas direcciones."""
        self._ruta = self._archivo("A, B, 5\n")
        g = cargarGrafo(self._ruta)
        a = g.obtenerVertice('A')
        b = g.obtenerVertice('B')
        self.assertEqual(b.obtenerPonderacion(a), 5)

    def test_lineas_vacias_no_rompen(self):
        self._ruta = self._archivo("\nA, B, 3\n\n")
        g = cargarGrafo(self._ruta)
        self.assertIn('A', g)

    def test_vertice_suelto(self):
        self._ruta = self._archivo("Peligros\n")
        g = cargarGrafo(self._ruta)
        v = g.obtenerVertice('Peligros')
        self.assertIsNotNone(v)
        self.assertEqual(len(list(v.obtenerConexiones())), 0)

    def test_multiples_aristas(self):
        self._ruta = self._archivo("A, B, 1\nB, C, 2\nC, A, 3\n")
        g = cargarGrafo(self._ruta)
        self.assertEqual(g.numVertices, 3)
>>>>>>> 1c9ad682ebbe80c39e3f2f8538011f8338857b16

    def test_archivo_inexistente_lanza_error(self):
        from Palomas_mensajeras import cargarGrafo as cg_real
        with self.assertRaises(FileNotFoundError):
            cg_real('/ruta/que/no/existe/aldeas.txt')


# ===========================================================================
# Integración con aldeas.txt real
# ===========================================================================

class TestIntegracionAldeas(unittest.TestCase):
    """Prueba el flujo completo con el archivo real de la consigna."""

    @classmethod
    def setUpClass(cls):
        base = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(base, 'data', 'aldeas.txt')
        cls.grafo = cargarGrafo(ruta)
        inicio = cls.grafo.obtenerVertice('Peligros')
        prim(cls.grafo, inicio)

    def test_peligros_existe(self):
        self.assertIn('Peligros', self.grafo)

    def test_22_aldeas(self):
        self.assertEqual(self.grafo.numVertices, 22)

    def test_peligros_sin_predecesor(self):
        v = self.grafo.obtenerVertice('Peligros')
        self.assertIsNone(v.obtenerPredecesor())

    def test_todas_las_aldeas_alcanzadas(self):
        """Todas las aldeas excepto Peligros deben tener predecesor (grafo conexo)."""
        sin_predecesor = [
            v.obtenerId()
            for v in self.grafo
            if v.obtenerPredecesor() is None and v.obtenerId() != 'Peligros'
        ]
        self.assertEqual(sin_predecesor, [],
            msg=f"Aldeas no alcanzadas: {sin_predecesor}")

    def test_distancia_total_positiva(self):
        total = sum(
            v.obtenerDistancia()
            for v in self.grafo
            if v.obtenerPredecesor() is not None
        )
        self.assertGreater(total, 0)


if __name__ == '__main__':
    RUTA_ALDEAS = os.path.join(os.path.dirname(__file__), '..', 'data', 'aldeas.txt')
    ORIGEN = "Peligros"

    try:
        print("\nLeyendo aldeas.txt ...")
        grafo = leer_aldeas(RUTA_ALDEAS)
        print(f"Grafo construido: {grafo.numVertices} aldeas cargadas.\n")
        mostrar_resultados(grafo, ORIGEN)

    except (FileNotFoundError, TypeError, ValueError) as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)