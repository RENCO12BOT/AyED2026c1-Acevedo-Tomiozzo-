import os
from datetime import datetime
from ayedfiuner.estructuras.arbolAVL import ArbolAVL


class TemperaturasDB:
    """
    Base de datos en memoria para mediciones de temperatura.
    """

    FORMATO_FECHA = "%d/%m/%Y"

    def __init__(self):
        """
        Postcondición:
            - Se crea una base de datos vacía respaldada por un ArbolAVL vacío.
        """
        self._arbol = ArbolAVL()

    def _parsear_fecha(self, s: str) -> datetime:
        """
        Precondición:
            - s es una cadena no vacía.
        Postcondición:
            - Si s tiene el formato dd/mm/aaaa, retorna el datetime correspondiente.
            - Si el formato es inválido, lanza ValueError.
        """
        try:
            return datetime.strptime(s, self.FORMATO_FECHA)
        except ValueError:
            raise ValueError(f"Fecha inválida: '{s}'. Use dd/mm/aaaa")

    def guardar_temperatura(self, temperatura: float, fecha: str):
        """
        Precondición:
            - fecha es una cadena con formato dd/mm/aaaa.
            - temperatura es un float.
        Postcondición:
            - Si la fecha no existía, se agrega y la cantidad aumenta en 1.
            - Si la fecha ya existía, su temperatura queda reemplazada.
        """
        self._arbol.insertar(self._parsear_fecha(fecha), temperatura)

    def devolver_temperatura(self, fecha: str):
        """
        Precondición:
            - fecha es una cadena con formato dd/mm/aaaa.
        Postcondición:
            - Retorna el float almacenado para esa fecha, o None si no existe.
        """
        n = self._arbol.buscar(self._parsear_fecha(fecha))
        return None if n is None else n.valor

    def max_temp_rango(self, fecha1: str, fecha2: str):
        """
        Precondición:
            - fecha1 <= fecha2 en orden cronológico.
        Postcondición:
            - Retorna el float máximo en el rango, o None si el rango está vacío.
        """
        ns = self._arbol.rango(self._parsear_fecha(fecha1), self._parsear_fecha(fecha2))
        return None if not ns else max(ns, key=lambda n: n.valor).valor

    def min_temp_rango(self, fecha1: str, fecha2: str):
        """
        Precondición:
            - fecha1 <= fecha2 en orden cronológico.
        Postcondición:
            - Retorna el float mínimo en el rango, o None si el rango está vacío.
        """
        ns = self._arbol.rango(self._parsear_fecha(fecha1), self._parsear_fecha(fecha2))
        return None if not ns else min(ns, key=lambda n: n.valor).valor

    def temp_extremos_rango(self, fecha1: str, fecha2: str):
        """
        Precondición:
            - fecha1 <= fecha2 en orden cronológico.
        Postcondición:
            - Retorna (min_temp, max_temp), o (None, None) si el rango está vacío.
        """
        ns = self._arbol.rango(self._parsear_fecha(fecha1), self._parsear_fecha(fecha2))
        if not ns: return (None, None)
        ts = [n.valor for n in ns]
        return (min(ts), max(ts))

    def borrar_temperatura(self, fecha: str):
        """
        Precondición:
            - fecha es una cadena con formato dd/mm/aaaa.
        Postcondición:
            - Si la fecha existía, la medición es eliminada y la cantidad disminuye en 1.
        """
        self._arbol.borrar(self._parsear_fecha(fecha))

    def devolver_temperaturas(self, fecha1: str, fecha2: str) -> list:
        """
        Precondición:
            - fecha1 <= fecha2 en orden cronológico.
        Postcondición:
            - Retorna lista de strings 'dd/mm/aaaa: T ºC' ordenada cronológicamente.
        """
        ns = self._arbol.rango(self._parsear_fecha(fecha1), self._parsear_fecha(fecha2))
        return [f"{n.clave.strftime(self.FORMATO_FECHA)}: {n.valor} ºC" for n in ns]

    def cantidad_muestras(self) -> int:
        """
        Postcondición:
            - Retorna un entero >= 0 igual al número de mediciones en la base de datos.
        """
        return self._arbol.cantidad()

    def cargar_desde_archivo(self, ruta: str) -> int:
        """
        Precondición:
            - ruta es la ruta a un archivo de texto existente y legible.
            - Cada línea de datos tiene formato dd/mm/aaaa;temperatura.
        Postcondición:
            - Las líneas válidas son insertadas en la base de datos.
            - Las líneas con errores se ignoran y se imprime un aviso.
            - Retorna el número de mediciones cargadas exitosamente.
        """
        cargadas = errores = 0
        with open(ruta, "r", encoding="utf-8") as archivo:
            for num, linea in enumerate(archivo, start=1):
                linea = linea.strip()
                if not linea or linea.startswith("#"):
                    continue
                partes = linea.split(";")
                try:
                    if len(partes) != 2:
                        raise ValueError("Se esperaban 2 columnas: fecha;temperatura")
                    fecha_str   = partes[0].strip()
                    temperatura = float(partes[1].strip())
                    self.guardar_temperatura(temperatura, fecha_str)
                    cargadas += 1
                except (ValueError, IndexError) as e:
                    print(f"   Línea {num} ignorada: {e}")
                    errores += 1
        print(f" Carga completada: {cargadas} mediciones cargadas, {errores} errores.")
        return cargadas


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("  TEMPERATURAS_DB — Demo de Kevin Kelvin")
    print("=" * 60)

    db = TemperaturasDB()

    print("\n Cargando mediciones manualmente...")
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

    print(f"\n Cantidad de muestras: {db.cantidad_muestras()}")

    print("\n Consulta de fecha específica:")
    print(f"  15/06/2023 → {db.devolver_temperatura('15/06/2023')} ºC")
    print(f"  01/01/2000 → {db.devolver_temperatura('01/01/2000')}")

    print("\n Extremos en rango 01/06/2023 → 30/06/2023:")
    minima, maxima = db.temp_extremos_rango("01/06/2023", "30/06/2023")
    print(f"  Mínima: {minima} ºC  |  Máxima: {maxima} ºC")

    print("\n Temperaturas en rango 10/06/2023 → 25/06/2023:")
    for item in db.devolver_temperaturas("10/06/2023", "25/06/2023"):
        print(f"  {item}")

    print("\n Borrando medición del 10/06/2023...")
    db.borrar_temperatura("10/06/2023")
    print(f"  Muestras ahora: {db.cantidad_muestras()}")
    print(f"  10/06/2023 después de borrar: {db.devolver_temperatura('10/06/2023')}")

    base = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(base, "..", "data", "muestras.txt")
    if os.path.exists(ruta):
        print(f"\n Cargando desde '{ruta}'...")
        db2 = TemperaturasDB()
        db2.cargar_desde_archivo(ruta)
        print(f"  Total de muestras: {db2.cantidad_muestras()}")
    else:
        print(f"\n Archivo '{ruta}' no encontrado, saltando carga.")

    print("\n" + "=" * 60)
    print("  Fin de la demo.")
    print("=" * 60)
    