from datetime import datetime  # manejo de fechas

# ── NodoAVL ───────────────────────────────────────────────────
class NodoAVL:
    def __init__(self, fecha: datetime, temperatura: float):
        self.fecha       = fecha         # clave de ordenamiento
        self.temperatura = temperatura   # valor asociado
        self.izquierdo   = None          # hijo izquierdo (fechas menores)
        self.derecho     = None          # hijo derecho (fechas mayores)
        self.altura      = 1             # nodo nuevo siempre empieza en 1

# ── ArbolAVL ──────────────────────────────────────────────────
class ArbolAVL:

    def __init__(self):
        self.raiz      = None  # árbol vacío al inicio
        self._cantidad = 0     # contador O(1) de muestras

    def _altura(self, nodo):
        return 0 if nodo is None else nodo.altura  # None → 0

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura(nodo.izquierdo),
                              self._altura(nodo.derecho))

    def _factor_balance(self, nodo):
        return 0 if nodo is None else (self._altura(nodo.izquierdo)
                                       - self._altura(nodo.derecho))

    def _rotar_derecha(self, z):        # caso II: subárbol izq demasiado alto
        y, T3      = z.izquierdo, z.izquierdo.derecho
        y.derecho  = z
        z.izquierdo = T3
        self._actualizar_altura(z)      # primero el que quedó abajo
        self._actualizar_altura(y)      # luego el que subió
        return y                        # nueva raíz del subárbol

    def _rotar_izquierda(self, z):      # caso DD: subárbol der demasiado alto
        y, T2       = z.derecho, z.derecho.izquierdo
        y.izquierdo = z
        z.derecho   = T2
        self._actualizar_altura(z)
        self._actualizar_altura(y)
        return y

    def _rebalancear(self, nodo):
        self._actualizar_altura(nodo)
        b = self._factor_balance(nodo)
        if b > 1  and self._factor_balance(nodo.izquierdo) >= 0:   # II
            return self._rotar_derecha(nodo)
        if b > 1  and self._factor_balance(nodo.izquierdo) < 0:    # ID
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)
        if b < -1 and self._factor_balance(nodo.derecho) <= 0:     # DD
            return self._rotar_izquierda(nodo)
        if b < -1 and self._factor_balance(nodo.derecho) > 0:      # DI
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)
        return nodo                     # ya balanceado, sin cambios

    def _insertar(self, nodo, fecha, temperatura):
        if nodo is None:                # lugar vacío → crear nodo
            self._cantidad += 1
            return NodoAVL(fecha, temperatura)
        if   fecha < nodo.fecha:
            nodo.izquierdo = self._insertar(nodo.izquierdo, fecha, temperatura)
        elif fecha > nodo.fecha:
            nodo.derecho   = self._insertar(nodo.derecho,   fecha, temperatura)
        else:                           # fecha duplicada → actualizar temp
            nodo.temperatura = temperatura
            return nodo
        return self._rebalancear(nodo)

    def _buscar(self, nodo, fecha):
        if nodo is None or fecha == nodo.fecha:
            return nodo
        return self._buscar(
            nodo.izquierdo if fecha < nodo.fecha else nodo.derecho, fecha)

    def _minimo_nodo(self, nodo):       # va siempre a la izquierda hasta el final
        while nodo.izquierdo:
            nodo = nodo.izquierdo
        return nodo

    def _borrar(self, nodo, fecha):
        if nodo is None:
            return None
        if   fecha < nodo.fecha:
            nodo.izquierdo = self._borrar(nodo.izquierdo, fecha)
        elif fecha > nodo.fecha:
            nodo.derecho   = self._borrar(nodo.derecho,   fecha)
        else:                           # nodo encontrado
            self._cantidad -= 1
            if not nodo.izquierdo: return nodo.derecho   # 0 o 1 hijo
            if not nodo.derecho:   return nodo.izquierdo
            suc = self._minimo_nodo(nodo.derecho)        # 2 hijos → sucesor inorden
            nodo.fecha, nodo.temperatura = suc.fecha, suc.temperatura
            nodo.derecho = self._borrar(nodo.derecho, suc.fecha)
            self._cantidad += 1         # compensar doble descuento del _borrar recursivo
        return self._rebalancear(nodo)

    def _rango_inorden(self, nodo, f1, f2, resultado):
        if nodo is None: return
        if nodo.fecha > f1: self._rango_inorden(nodo.izquierdo, f1, f2, resultado)  # poda izquierda
        if f1 <= nodo.fecha <= f2: resultado.append(nodo)                           # nodo en rango
        if nodo.fecha < f2: self._rango_inorden(nodo.derecho,   f1, f2, resultado)  # poda derecha

    # métodos públicos
    def insertar(self, f, t): self.raiz = self._insertar(self.raiz, f, t)
    def buscar(self, f):      return self._buscar(self.raiz, f)
    def borrar(self, f):      self.raiz = self._borrar(self.raiz, f)
    def rango(self, f1, f2):
        r = []; self._rango_inorden(self.raiz, f1, f2, r); return r
    def cantidad(self):       return self._cantidad


# ── TemperaturasDB ────────────────────────────────────────────
class TemperaturasDB:
    """Base de datos en memoria para mediciones de temperatura. Usa AVL internamente."""

    FORMATO_FECHA = "%d/%m/%Y"

    def __init__(self):
        self._arbol = ArbolAVL()        # árbol AVL interno (invisible al usuario)

    def _parsear_fecha(self, s: str) -> datetime:
        try:
            return datetime.strptime(s, self.FORMATO_FECHA)
        except ValueError:
            raise ValueError(f"Fecha inválida: '{s}'. Use dd/mm/aaaa")

    def guardar_temperatura(self, temperatura: float, fecha: str):
        """Guarda o actualiza una medición. O(log n)"""
        self._arbol.insertar(self._parsear_fecha(fecha), temperatura)

    def devolver_temperatura(self, fecha: str):
        """Devuelve la temperatura de una fecha o None si no existe. O(log n)"""
        n = self._arbol.buscar(self._parsear_fecha(fecha))
        return None if n is None else n.temperatura

    def max_temp_rango(self, fecha1: str, fecha2: str):
        """Temperatura máxima en el rango [fecha1, fecha2]. O(log n + k)"""
        ns = self._arbol.rango(self._parsear_fecha(fecha1), self._parsear_fecha(fecha2))
        return None if not ns else max(ns, key=lambda n: n.temperatura).temperatura

    def min_temp_rango(self, fecha1: str, fecha2: str):
        """Temperatura mínima en el rango [fecha1, fecha2]. O(log n + k)"""
        ns = self._arbol.rango(self._parsear_fecha(fecha1), self._parsear_fecha(fecha2))
        return None if not ns else min(ns, key=lambda n: n.temperatura).temperatura

    def temp_extremos_rango(self, fecha1: str, fecha2: str):
        """Devuelve (mínima, máxima) del rango. O(log n + k) — un solo recorrido"""
        ns = self._arbol.rango(self._parsear_fecha(fecha1), self._parsear_fecha(fecha2))
        if not ns: return (None, None)
        ts = [n.temperatura for n in ns]
        return (min(ts), max(ts))

    def borrar_temperatura(self, fecha: str):
        """Elimina la medición de una fecha. O(log n)"""
        self._arbol.borrar(self._parsear_fecha(fecha))

    def devolver_temperaturas(self, fecha1: str, fecha2: str) -> list:
        """Lista ordenada de mediciones en el rango. O(log n + k)"""
        ns = self._arbol.rango(self._parsear_fecha(fecha1), self._parsear_fecha(fecha2))
        return [f"{n.fecha.strftime(self.FORMATO_FECHA)}: {n.temperatura} ºC" for n in ns]

    def cantidad_muestras(self) -> int:
        """Cantidad de muestras almacenadas. O(1)"""
        return self._arbol.cantidad()

    def cargar_desde_archivo(self, ruta: str) -> int:
        """
        Lee un archivo .txt con el formato:
            dd/mm/aaaa,temperatura
        Líneas vacías y las que empiezan con '#' se ignoran.
        O(m · log(n+m))
        """
        cargadas = errores = 0

        with open(ruta, "r", encoding="utf-8") as archivo:
            for num, linea in enumerate(archivo, start=1):
                linea = linea.strip()                       # quita espacios y salto de línea

                if not linea or linea.startswith("#"):      # ignora vacías y comentarios
                    continue

                partes = linea.split(";")                   # separador punto y coma

                try:
                    if len(partes) != 2:
                        raise ValueError("Se esperaban 2 columnas: fecha,temperatura")
                    fecha_str   = partes[0].strip()         # primera columna → fecha
                    temperatura = float(partes[1].strip())  # segunda columna → float
                    self.guardar_temperatura(temperatura, fecha_str)
                    cargadas += 1

                except (ValueError, IndexError) as e:
                    print(f"  ⚠ Línea {num} ignorada: {e}")
                    errores += 1

        print(f"✔ Carga completada: {cargadas} mediciones cargadas, {errores} errores.")
        return cargadas


# ── Demo ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    print("=" * 60)
    print("  TEMPERATURAS_DB — Demo de Kevin Kelvin")
    print("=" * 60)

    db = TemperaturasDB()

    # carga manual de mediciones de ejemplo
    print("\n📥 Cargando mediciones manualmente...")
    mediciones = [
        (22.5,  "01/06/2023"),
        (18.0,  "05/06/2023"),
        (-3.2,  "10/06/2023"),
        (30.1,  "15/06/2023"),
        (25.8,  "20/06/2023"),
        (12.4,  "25/06/2023"),
        (8.9,   "30/06/2023"),
        (35.0,  "04/07/2023"),
        (-10.5, "10/07/2023"),
        (0.0,   "20/07/2023"),
    ]
    for temp, fecha in mediciones:
        db.guardar_temperatura(temp, fecha)
        print(f"  Guardada: {fecha} → {temp} ºC")

    print(f"\n📊 Cantidad de muestras: {db.cantidad_muestras()}")

    # búsqueda puntual
    print("\n🔍 Consulta de fecha específica:")
    print(f"  15/06/2023 → {db.devolver_temperatura('15/06/2023')} ºC")
    print(f"  01/01/2000 → {db.devolver_temperatura('01/01/2000')}")  # None

    # extremos de rango
    print("\n🌡 Extremos en rango 01/06/2023 → 30/06/2023:")
    minima, maxima = db.temp_extremos_rango("01/06/2023", "30/06/2023")
    print(f"  Mínima: {minima} ºC  |  Máxima: {maxima} ºC")

    # listado de rango
    print("\n📋 Temperaturas en rango 10/06/2023 → 25/06/2023:")
    for item in db.devolver_temperaturas("10/06/2023", "25/06/2023"):
        print(f"  {item}")

    # borrado
    print("\n🗑 Borrando medición del 10/06/2023...")
    db.borrar_temperatura("10/06/2023")
    print(f"  Muestras ahora: {db.cantidad_muestras()}")
    print(f"  10/06/2023 después de borrar: {db.devolver_temperatura('10/06/2023')}")

    # carga desde archivo .txt
    base = os.path.dirname(os.path.abspath(__file__))   # carpeta donde está este .py
    ruta = os.path.join(base, "..", "data", "muestras.txt")  # sube un nivel a data/
    if os.path.exists(ruta):
        print(f"\n📂 Cargando desde '{ruta}'...")
        db2 = TemperaturasDB()
        db2.cargar_desde_archivo(ruta)
        print(f"  Total de muestras: {db2.cantidad_muestras()}")
    else:
        print(f"\n📂 Archivo '{ruta}' no encontrado, saltando carga desde archivo.")
 
    print("\n" + "=" * 60)
    print("  Fin de la demo. ¡Hasta la próxima, Kevin!")
    print("=" * 60)