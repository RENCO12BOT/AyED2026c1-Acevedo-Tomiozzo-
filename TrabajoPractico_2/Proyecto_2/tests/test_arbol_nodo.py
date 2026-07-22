import unittest
from datetime import datetime

from ayedfiuner.estructuras.arbolAVL import ArbolAVL
from ayedfiuner.estructuras.nodoAVL import NodoAVL

def _fecha(s: str) -> datetime:
    return datetime.strptime(s, "%d/%m/%Y")


def _altura_real(nodo) -> int:
    if nodo is None:
        return 0
    return 1 + max(_altura_real(nodo.izquierdo), _altura_real(nodo.derecho))


def _es_avl(nodo) -> bool:
    if nodo is None:
        return True
    izq = _altura_real(nodo.izquierdo)
    der = _altura_real(nodo.derecho)
    if abs(izq - der) > 1:
        return False
    return _es_avl(nodo.izquierdo) and _es_avl(nodo.derecho)


def _inorden(nodo, resultado=None):
    if resultado is None:
        resultado = []
    if nodo is None:
        return resultado
    _inorden(nodo.izquierdo, resultado)
    resultado.append(nodo.fecha)
    _inorden(nodo.derecho, resultado)
    return resultado


class TestArbolAVLInsertar(unittest.TestCase):

    def setUp(self):
        self.avl = ArbolAVL()

    def test_arbol_vacio_cantidad(self):
        self.assertEqual(self.avl.cantidad(), 0)

    def test_arbol_vacio_buscar(self):
        self.assertIsNone(self.avl.buscar(_fecha("01/01/2024")))

    def test_insertar_un_nodo(self):
        self.avl.insertar(_fecha("01/01/2024"), 20.0)
        self.assertEqual(self.avl.cantidad(), 1)

    def test_insertar_varios_nodos(self):
        fechas = ["01/01/2024", "05/01/2024", "10/01/2024",
                  "15/01/2024", "20/01/2024"]
        for i, f in enumerate(fechas):
            self.avl.insertar(_fecha(f), float(i))
        self.assertEqual(self.avl.cantidad(), 5)

    def test_insertar_fecha_duplicada_actualiza_temperatura(self):
        self.avl.insertar(_fecha("01/01/2024"), 20.0)
        self.avl.insertar(_fecha("01/01/2024"), 99.9)
        self.assertEqual(self.avl.cantidad(), 1)
        nodo = self.avl.buscar(_fecha("01/01/2024"))
        self.assertAlmostEqual(nodo.temperatura, 99.9)

    def test_inorden_ordenado_tras_insercion_aleatoria(self):
        fechas = ["15/06/2023", "01/06/2023", "30/06/2023",
                  "10/06/2023", "20/06/2023"]
        for f in fechas:
            self.avl.insertar(_fecha(f), 0.0)
        resultado = _inorden(self.avl.raiz)
        self.assertEqual(resultado, sorted(resultado))

    def test_propiedad_avl_tras_insercion_secuencial(self):
        """Inserta 20 nodos en orden creciente — fuerza rotaciones DD."""
        for i in range(1, 21):
            self.avl.insertar(_fecha(f"{i:02d}/01/2024"), float(i))
        self.assertTrue(_es_avl(self.avl.raiz))

    def test_propiedad_avl_tras_insercion_decreciente(self):
        """Inserta en orden decreciente — fuerza rotaciones II."""
        for i in range(28, 0, -1):
            self.avl.insertar(_fecha(f"{i:02d}/01/2024"), float(i))
        self.assertTrue(_es_avl(self.avl.raiz))

    def test_propiedad_avl_tras_insercion_aleatoria(self):
        fechas = ["15/06/2023", "01/06/2023", "30/06/2023", "10/06/2023",
                  "20/06/2023", "05/06/2023", "25/06/2023", "12/06/2023"]
        for f in fechas:
            self.avl.insertar(_fecha(f), 0.0)
        self.assertTrue(_es_avl(self.avl.raiz))


class TestArbolAVLBuscar(unittest.TestCase):

    def setUp(self):
        self.avl = ArbolAVL()
        self.avl.insertar(_fecha("10/06/2023"), 25.0)
        self.avl.insertar(_fecha("20/06/2023"), 30.0)
        self.avl.insertar(_fecha("01/06/2023"), 18.0)

    def test_buscar_existente(self):
        nodo = self.avl.buscar(_fecha("20/06/2023"))
        self.assertIsNotNone(nodo)
        self.assertAlmostEqual(nodo.temperatura, 30.0)

    def test_buscar_inexistente(self):
        self.assertIsNone(self.avl.buscar(_fecha("01/01/2000")))

    def test_buscar_raiz(self):
        nodo = self.avl.buscar(_fecha("10/06/2023"))
        self.assertAlmostEqual(nodo.temperatura, 25.0)


class TestArbolAVLBorrar(unittest.TestCase):

    def setUp(self):
        self.avl = ArbolAVL()
        for f, t in [("01/06/2023", 22.5), ("05/06/2023", 18.0),
                     ("10/06/2023", -3.2), ("15/06/2023", 30.1),
                     ("20/06/2023", 25.8)]:
            self.avl.insertar(_fecha(f), t)

    def test_borrar_hoja(self):
        self.avl.borrar(_fecha("20/06/2023"))
        self.assertIsNone(self.avl.buscar(_fecha("20/06/2023")))
        self.assertEqual(self.avl.cantidad(), 4)

    def test_borrar_nodo_con_un_hijo(self):
        self.avl.borrar(_fecha("05/06/2023"))
        self.assertIsNone(self.avl.buscar(_fecha("05/06/2023")))
        self.assertEqual(self.avl.cantidad(), 4)

    def test_borrar_nodo_con_dos_hijos(self):
        self.avl.borrar(_fecha("05/06/2023"))
        self.assertIsNotNone(self.avl.buscar(_fecha("01/06/2023")))
        self.assertIsNotNone(self.avl.buscar(_fecha("10/06/2023")))

    def test_borrar_todos(self):
        for f in ["01/06/2023", "05/06/2023", "10/06/2023",
                  "15/06/2023", "20/06/2023"]:
            self.avl.borrar(_fecha(f))
        self.assertEqual(self.avl.cantidad(), 0)
        self.assertIsNone(self.avl.raiz)

    def test_borrar_inexistente_no_cambia_cantidad(self):
        self.avl.borrar(_fecha("01/01/2000"))
        self.assertEqual(self.avl.cantidad(), 5)

    def test_propiedad_avl_tras_borrado(self):
        self.avl.borrar(_fecha("10/06/2023"))
        self.assertTrue(_es_avl(self.avl.raiz))

    def test_inorden_correcto_tras_borrado(self):
        self.avl.borrar(_fecha("05/06/2023"))
        resultado = _inorden(self.avl.raiz)
        self.assertEqual(resultado, sorted(resultado))


class TestArbolAVLRango(unittest.TestCase):

    def setUp(self):
        self.avl = ArbolAVL()
        for f, t in [("01/06/2023", 10.0), ("10/06/2023", 20.0),
                     ("20/06/2023", 30.0), ("30/06/2023", 40.0),
                     ("10/07/2023", 50.0)]:
            self.avl.insertar(_fecha(f), t)

    def test_rango_todos(self):
        ns = self.avl.rango(_fecha("01/06/2023"), _fecha("10/07/2023"))
        self.assertEqual(len(ns), 5)

    def test_rango_parcial(self):
        ns = self.avl.rango(_fecha("10/06/2023"), _fecha("30/06/2023"))
        fechas = [n.fecha for n in ns]
        self.assertIn(_fecha("10/06/2023"), fechas)
        self.assertIn(_fecha("20/06/2023"), fechas)
        self.assertIn(_fecha("30/06/2023"), fechas)
        self.assertNotIn(_fecha("01/06/2023"), fechas)
        self.assertNotIn(_fecha("10/07/2023"), fechas)

    def test_rango_un_elemento(self):
        ns = self.avl.rango(_fecha("20/06/2023"), _fecha("20/06/2023"))
        self.assertEqual(len(ns), 1)
        self.assertAlmostEqual(ns[0].temperatura, 30.0)

    def test_rango_vacio(self):
        ns = self.avl.rango(_fecha("01/01/2000"), _fecha("31/12/2000"))
        self.assertEqual(ns, [])

    def test_rango_ordenado_inorden(self):
        ns = self.avl.rango(_fecha("01/06/2023"), _fecha("10/07/2023"))
        fechas = [n.fecha for n in ns]
        self.assertEqual(fechas, sorted(fechas))

    def test_rango_inverso_devuelve_vacio(self):
        """f1 > f2 no debe devolver resultados."""
        ns = self.avl.rango(_fecha("30/06/2023"), _fecha("01/06/2023"))
        self.assertEqual(ns, [])

    def test_avl_solo_un_nodo_es_avl(self):
        avl = ArbolAVL()
        avl.insertar(_fecha("01/01/2024"), 20.0)
        self.assertTrue(_es_avl(avl.raiz))

    def test_insertar_28_nodos_mantiene_avl(self):
        import random
        avl = ArbolAVL()
        random.seed(42)
        dias = random.sample(range(1, 29), 28)
        for d in dias:
            avl.insertar(_fecha(f"{d:02d}/01/2024"), float(d))
        self.assertTrue(_es_avl(avl.raiz))
        self.assertEqual(avl.cantidad(), 28)


if __name__ == "__main__":
    unittest.main()