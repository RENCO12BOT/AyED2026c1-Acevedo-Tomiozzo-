from datetime import datetime  # Módulo estándar para manejar fechas
# ==============================================================
# CLASE: NodoAVL
# Representa un nodo (casillero) dentro del árbol AVL.
# Cada nodo guarda UNA fecha y SU temperatura asociada.
# ==============================================================
class NodoAVL:
    def __init__(self, fecha: datetime, temperatura: float):
        """
        Crea un nodo nuevo con una fecha y su temperatura.

        Parámetros:
            fecha       : objeto datetime (la clave de ordenamiento)
            temperatura : float (el valor que guardamos)
        """
        self.fecha = fecha            # La clave del nodo (se usa para ordenar)
        self.temperatura = temperatura  # El dato que queremos almacenar

        self.izquierdo = None  # Hijo izquierdo (fechas menores)
        self.derecho = None    # Hijo derecho (fechas mayores)
        self.altura = 1        # Altura del nodo (un nodo solo = altura 1)
        #   La altura sirve para saber si el árbol está balanceado.
        #   Si la diferencia de alturas entre hijo izq y der es > 1,
        #   hay que "rotar" para rebalancear.
        
# ==============================================================
# CLASE: ArbolAVL
# El árbol en sí. Maneja inserciones, búsquedas, borrados
# y consultas de rango, siempre manteniéndose balanceado.
# ==============================================================
class ArbolAVL:

    def __init__(self):
        """Crea un árbol vacío."""
        self.raiz = None  # Al inicio no hay ningún nodo
        self._cantidad = 0  # Contador de cuántas muestras tenemos

    # ----------------------------------------------------------
    # MÉTODOS PRIVADOS DE APOYO (internos del árbol AVL)
    # El prefijo "_" indica que son métodos internos, no para
    # usar desde afuera de la clase.
    # ----------------------------------------------------------

    def _altura(self, nodo: NodoAVL) -> int:
        """
        Devuelve la altura de un nodo.
        Si el nodo no existe (None), su altura es 0.
        Esto evita errores al pedir la altura de un nodo vacío.
        """
        if nodo is None:       # Si el nodo no existe...
            return 0           # ...su altura es 0 (no ocupa lugar)
        return nodo.altura     # Si existe, devolvemos su altura guardada

    def _actualizar_altura(self, nodo: NodoAVL):
        """
        Recalcula y actualiza la altura de un nodo.
        La altura de un nodo = 1 + la mayor altura de sus hijos.
        Ejemplo: si hijo izq tiene altura 2 y hijo der tiene altura 3,
                 la altura del nodo actual es 1 + 3 = 4.
        """
        nodo.altura = 1 + max(
            self._altura(nodo.izquierdo),   # Altura del subárbol izquierdo
            self._altura(nodo.derecho)      # Altura del subárbol derecho
        )

    def _factor_balance(self, nodo: NodoAVL) -> int:
        """
        Calcula el factor de balance de un nodo.
        Factor = altura(izquierdo) - altura(derecho)

        Si factor > 1  → el árbol está "cargado a la izquierda" → rotar
        Si factor < -1 → el árbol está "cargado a la derecha"  → rotar
        Si -1 ≤ factor ≤ 1 → el árbol está balanceado (OK)
        """
        if nodo is None:       # Un nodo vacío tiene balance 0
            return 0
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho)

    def _rotar_derecha(self, z: NodoAVL) -> NodoAVL:
        """
        Rotación simple a la DERECHA.
        Se usa cuando el subárbol izquierdo es demasiado alto.

        Antes:          Después:
             z               y
            / \             / \
           y   T4          x   z
          / \             /|   |\
         x   T3          T1 T2 T3 T4

        El nodo 'y' sube, 'z' baja a la derecha.
        """
        y = z.izquierdo    # 'y' es el hijo izquierdo de 'z'
        T3 = y.derecho     # Guardamos el subárbol derecho de 'y'

        # Realizamos la rotación
        y.derecho = z      # 'z' pasa a ser hijo derecho de 'y'
        z.izquierdo = T3   # El antiguo subárbol T3 pasa al lado izq de 'z'

        # Actualizamos alturas (primero 'z' porque ahora es hijo de 'y')
        self._actualizar_altura(z)  # Primero el que quedó abajo
        self._actualizar_altura(y)  # Luego el que subió

        return y  # 'y' es ahora la nueva raíz de este subárbol

    def _rotar_izquierda(self, z: NodoAVL) -> NodoAVL:
        """
        Rotación simple a la IZQUIERDA.
        Se usa cuando el subárbol derecho es demasiado alto.

        Antes:       Después:
           z              y
          / \            / \
         T1   y         z   x
             / \       /|   |\
            T2  x     T1 T2 T3 T4

        El nodo 'y' sube, 'z' baja a la izquierda.
        """
        y = z.derecho      # 'y' es el hijo derecho de 'z'
        T2 = y.izquierdo   # Guardamos el subárbol izquierdo de 'y'

        # Realizamos la rotación
        y.izquierdo = z    # 'z' pasa a ser hijo izquierdo de 'y'
        z.derecho = T2     # El antiguo T2 pasa al lado derecho de 'z'

        # Actualizamos alturas
        self._actualizar_altura(z)  # Primero el que quedó abajo
        self._actualizar_altura(y)  # Luego el que subió

        return y  # 'y' es la nueva raíz del subárbol

    def _rebalancear(self, nodo: NodoAVL) -> NodoAVL:
        """
        Revisa si el nodo está desbalanceado y aplica las rotaciones necesarias.
        Hay 4 casos posibles de desbalanceo:

        Caso 1 - Izquierda-Izquierda (II): rotar a la derecha
        Caso 2 - Izquierda-Derecha  (ID): rotar izq al hijo, luego der al padre
        Caso 3 - Derecha-Derecha   (DD): rotar a la izquierda
        Caso 4 - Derecha-Izquierda (DI): rotar der al hijo, luego izq al padre
        """
        self._actualizar_altura(nodo)  # Primero actualizamos la altura del nodo

        balance = self._factor_balance(nodo)  # Calculamos el balance

        # CASO 1: Izquierda-Izquierda (el peso está en la rama izq-izq)
        if balance > 1 and self._factor_balance(nodo.izquierdo) >= 0:
            return self._rotar_derecha(nodo)  # Una sola rotación a la derecha

        # CASO 2: Izquierda-Derecha (el peso está en la rama izq-der)
        if balance > 1 and self._factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)  # Rotar hijo izq
            return self._rotar_derecha(nodo)  # Luego rotar el nodo actual

        # CASO 3: Derecha-Derecha (el peso está en la rama der-der)
        if balance < -1 and self._factor_balance(nodo.derecho) <= 0:
            return self._rotar_izquierda(nodo)  # Una sola rotación a la izquierda

        # CASO 4: Derecha-Izquierda (el peso está en la rama der-izq)
        if balance < -1 and self._factor_balance(nodo.derecho) > 0:
            nodo.derecho = self._rotar_derecha(nodo.derecho)  # Rotar hijo der
            return self._rotar_izquierda(nodo)  # Luego rotar el nodo actual

        return nodo  # Si no hay desbalanceo, devolvemos el nodo sin cambios

    def _insertar(self, nodo: NodoAVL, fecha: datetime, temperatura: float) -> NodoAVL:
        """
        Inserta recursivamente un nuevo nodo en el subárbol con raíz 'nodo'.
        Después de insertar, rebalancea si es necesario.

        ¿Cómo funciona la recursión?
            - Si la fecha es menor → bajamos por la izquierda
            - Si la fecha es mayor → bajamos por la derecha
            - Si es igual → actualizamos la temperatura (no duplicamos)
            - Cuando llegamos a None → creamos el nodo ahí
        """
        # CASO BASE: llegamos a un lugar vacío, creamos el nodo nuevo
        if nodo is None:
            self._cantidad += 1  # Aumentamos el contador de muestras
            return NodoAVL(fecha, temperatura)  # Nodo recién nacido

        # CASO RECURSIVO: comparamos la fecha para saber por dónde bajar
        if fecha < nodo.fecha:
            # La fecha nueva es anterior → va al subárbol izquierdo
            nodo.izquierdo = self._insertar(nodo.izquierdo, fecha, temperatura)
        elif fecha > nodo.fecha:
            # La fecha nueva es posterior → va al subárbol derecho
            nodo.derecho = self._insertar(nodo.derecho, fecha, temperatura)
        else:
            # La fecha ya existe → actualizamos la temperatura (sin duplicar)
            nodo.temperatura = temperatura
            return nodo  # No hace falta rebalancear, el árbol no cambió

        # Después de insertar, rebalanceamos desde este nodo hacia arriba
        return self._rebalancear(nodo)

    def _buscar(self, nodo: NodoAVL, fecha: datetime):
        """
        Busca recursivamente el nodo con la fecha dada.
        Devuelve el nodo encontrado, o None si no existe.
        """
        if nodo is None:         # No encontramos nada
            return None
        if fecha == nodo.fecha:  # ¡Encontrado!
            return nodo
        elif fecha < nodo.fecha:
            return self._buscar(nodo.izquierdo, fecha)  # Buscar a la izquierda
        else:
            return self._buscar(nodo.derecho, fecha)    # Buscar a la derecha

    def _minimo_nodo(self, nodo: NodoAVL) -> NodoAVL:
        """
        Devuelve el nodo con la fecha más pequeña del subárbol.
        En un ABB el mínimo siempre está en el extremo más a la izquierda.
        Se usa durante el borrado para encontrar el sucesor.
        """
        actual = nodo
        while actual.izquierdo is not None:  # Seguimos yendo a la izquierda
            actual = actual.izquierdo         # hasta llegar al final
        return actual  # El más a la izquierda es el mínimo

    def _borrar(self, nodo: NodoAVL, fecha: datetime) -> NodoAVL:
        """
        Elimina recursivamente el nodo con la fecha dada.
        Hay 3 casos para el borrado en un ABB:
            1) El nodo no tiene hijos           → simplemente lo eliminamos
            2) El nodo tiene UN hijo            → lo reemplazamos por ese hijo
            3) El nodo tiene DOS hijos          → lo reemplazamos por su sucesor
               (el sucesor es el mínimo del subárbol derecho)
        """
        if nodo is None:          # La fecha no estaba en el árbol
            return None

        if fecha < nodo.fecha:
            # La fecha buscada es menor → borramos en el subárbol izquierdo
            nodo.izquierdo = self._borrar(nodo.izquierdo, fecha)
        elif fecha > nodo.fecha:
            # La fecha buscada es mayor → borramos en el subárbol derecho
            nodo.derecho = self._borrar(nodo.derecho, fecha)
        else:
            # ¡Encontramos el nodo a borrar!
            self._cantidad -= 1  # Reducimos el contador de muestras

            # CASO 1 y 2: el nodo tiene 0 o 1 hijo
            if nodo.izquierdo is None:
                return nodo.derecho   # Lo reemplazamos por el hijo derecho (o None)
            elif nodo.derecho is None:
                return nodo.izquierdo # Lo reemplazamos por el hijo izquierdo

            # CASO 3: el nodo tiene DOS hijos
            # Buscamos el sucesor inorden (el más pequeño del subárbol derecho)
            sucesor = self._minimo_nodo(nodo.derecho)
            # Copiamos los datos del sucesor al nodo actual
            nodo.fecha = sucesor.fecha
            nodo.temperatura = sucesor.temperatura
            # Borramos el sucesor del subárbol derecho (ya lo "copiamos")
            nodo.derecho = self._borrar(nodo.derecho, sucesor.fecha)
            self._cantidad += 1  # _borrar descontó de nuevo, compensamos

        # Rebalanceamos después de borrar
        return self._rebalancear(nodo)

    def _rango_inorden(self, nodo: NodoAVL, f1: datetime, f2: datetime, resultado: list):
        """
        Recorre el árbol en orden (inorden = izq → raíz → der) y agrega
        al listado 'resultado' todos los nodos cuya fecha esté en [f1, f2].

        El recorrido inorden en un ABB siempre da los elementos ordenados
        de menor a mayor. ¡Perfecto para rangos!

        Optimización: si la fecha del nodo es menor que f1, no tiene sentido
        explorar su subárbol izquierdo (todas serían menores). Igual para der.
        """
        if nodo is None:  # Llegamos a un lugar vacío, nada que hacer
            return

        # Solo bajamos a la izquierda si puede haber fechas válidas ahí
        if nodo.fecha > f1:
            self._rango_inorden(nodo.izquierdo, f1, f2, resultado)

        # Si la fecha del nodo está dentro del rango, la agregamos
        if f1 <= nodo.fecha <= f2:
            resultado.append(nodo)  # Guardamos el nodo entero

        # Solo bajamos a la derecha si puede haber fechas válidas ahí
        if nodo.fecha < f2:
            self._rango_inorden(nodo.derecho, f1, f2, resultado)

    # ----------------------------------------------------------
    # MÉTODOS PÚBLICOS DEL ÁRBOL AVL
    # ----------------------------------------------------------

    def insertar(self, fecha: datetime, temperatura: float):
        """Inserta o actualiza una medición en el árbol."""
        self.raiz = self._insertar(self.raiz, fecha, temperatura)

    def buscar(self, fecha: datetime):
        """Busca y devuelve el nodo de una fecha dada (o None si no existe)."""
        return self._buscar(self.raiz, fecha)

    def borrar(self, fecha: datetime):
        """Elimina la medición de una fecha dada del árbol."""
        self.raiz = self._borrar(self.raiz, fecha)

    def rango(self, f1: datetime, f2: datetime) -> list:
        """Devuelve la lista de nodos cuyas fechas están en [f1, f2], ordenados."""
        resultado = []                              # Lista vacía para ir llenando
        self._rango_inorden(self.raiz, f1, f2, resultado)  # Llenamos la lista
        return resultado                            # La devolvemos ordenada

    def cantidad(self) -> int:
        """Devuelve la cantidad de muestras almacenadas."""
        return self._cantidad


# ==============================================================
# CLASE: TemperaturasDB
# La interfaz amigable que usa el científico Kevin Kelvin.
# Internamente usa el ArbolAVL, pero Kevin no necesita saber eso.
# ==============================================================
class TemperaturasDB:
    """
    Base de datos en memoria para almacenar mediciones de temperatura
    organizadas por fecha. Usa un árbol AVL internamente para garantizar
    operaciones eficientes O(log n).
    """

    FORMATO_FECHA = "%d/%m/%Y"  # Formato de fecha: día/mes/año (ej: 25/12/2023)

    def __init__(self):
        """Inicializa la base de datos vacía."""
        self._arbol = ArbolAVL()  # El árbol AVL donde viven los datos

    # ----------------------------------------------------------
    # MÉTODO AUXILIAR PRIVADO: convertir string a datetime
    # ----------------------------------------------------------

    def _parsear_fecha(self, fecha_str: str) -> datetime:
        """
        Convierte un string "dd/mm/aaaa" en un objeto datetime.
        Ejemplo: "25/12/2023" → datetime(2023, 12, 25)

        Si el formato es incorrecto, lanza un ValueError con mensaje claro.
        """
        try:
            # strptime = "string parse time": convierte texto a fecha
            return datetime.strptime(fecha_str, self.FORMATO_FECHA)
        except ValueError:
            # Si el formato es inválido, avisamos con un mensaje claro
            raise ValueError(f"Fecha inválida: '{fecha_str}'. Use el formato dd/mm/aaaa")

    # ----------------------------------------------------------
    # MÉTODOS PÚBLICOS DE LA INTERFAZ TemperaturasDB
    # ----------------------------------------------------------

    def guardar_temperatura(self, temperatura: float, fecha: str):
        """
        Guarda (o actualiza) la temperatura de una fecha determinada.

        Parámetros:
            temperatura : valor en ºC (puede ser negativo, ej: -5.3)
            fecha       : string en formato "dd/mm/aaaa"

        Complejidad: O(log n)
            Insertar en un AVL siempre recorre la altura del árbol,
            que es O(log n) porque el árbol está siempre balanceado.
        """
        fecha_dt = self._parsear_fecha(fecha)        # Convertimos string a datetime
        self._arbol.insertar(fecha_dt, temperatura)  # Insertamos en el árbol AVL

    def devolver_temperatura(self, fecha: str) -> float:
        """
        Devuelve la temperatura registrada en una fecha específica.

        Parámetros:
            fecha : string en formato "dd/mm/aaaa"

        Retorna:
            float con la temperatura, o None si la fecha no existe.

        Complejidad: O(log n)
            Buscar en un AVL es recorrer la altura del árbol = O(log n).
        """
        fecha_dt = self._parsear_fecha(fecha)        # Convertimos string a datetime
        nodo = self._arbol.buscar(fecha_dt)          # Buscamos el nodo en el árbol
        if nodo is None:                             # Si no existe esa fecha...
            return None                              # ...devolvemos None
        return nodo.temperatura                      # Si existe, devolvemos la temp

    def max_temp_rango(self, fecha1: str, fecha2: str) -> float:
        """
        Devuelve la temperatura MÁXIMA entre fecha1 y fecha2 (inclusive).
        Si no hay mediciones en ese rango, devuelve None.

        Complejidad: O(log n + k)
            O(log n) para llegar al primer nodo del rango,
            O(k) para recorrer los k nodos dentro del rango.
        """
        f1 = self._parsear_fecha(fecha1)             # Convertimos fecha1
        f2 = self._parsear_fecha(fecha2)             # Convertimos fecha2
        nodos = self._arbol.rango(f1, f2)            # Obtenemos nodos del rango
        if not nodos:                                # Si el rango está vacío...
            return None                              # ...no hay máximo
        # max() sobre una lista de nodos, usando la temperatura como clave
        return max(nodos, key=lambda n: n.temperatura).temperatura

    def min_temp_rango(self, fecha1: str, fecha2: str) -> float:
        """
        Devuelve la temperatura MÍNIMA entre fecha1 y fecha2 (inclusive).
        Si no hay mediciones en ese rango, devuelve None.

        Complejidad: O(log n + k)  (igual que max_temp_rango)
        """
        f1 = self._parsear_fecha(fecha1)             # Convertimos fecha1
        f2 = self._parsear_fecha(fecha2)             # Convertimos fecha2
        nodos = self._arbol.rango(f1, f2)            # Obtenemos nodos del rango
        if not nodos:                                # Si el rango está vacío...
            return None                              # ...no hay mínimo
        return min(nodos, key=lambda n: n.temperatura).temperatura

    def temp_extremos_rango(self, fecha1: str, fecha2: str) -> tuple:
        """
        Devuelve una tupla (mínima, máxima) del rango de fechas.
        Si no hay mediciones, devuelve (None, None).

        Complejidad: O(log n + k)
            Un solo recorrido del rango para obtener ambos extremos.
        """
        f1 = self._parsear_fecha(fecha1)             # Convertimos fecha1
        f2 = self._parsear_fecha(fecha2)             # Convertimos fecha2
        nodos = self._arbol.rango(f1, f2)            # Obtenemos nodos del rango
        if not nodos:                                # Si el rango está vacío...
            return (None, None)                      # ...no hay extremos
        temps = [n.temperatura for n in nodos]       # Lista de temperaturas del rango
        return (min(temps), max(temps))              # Devolvemos (mínima, máxima)

    def borrar_temperatura(self, fecha: str):
        """
        Elimina del árbol la medición correspondiente a una fecha.

        Complejidad: O(log n)
            Borrar en un AVL es O(log n) porque el árbol está balanceado.
        """
        fecha_dt = self._parsear_fecha(fecha)        # Convertimos string a datetime
        self._arbol.borrar(fecha_dt)                 # Borramos el nodo del árbol

    def devolver_temperaturas(self, fecha1: str, fecha2: str) -> list:
        """
        Devuelve una lista de strings con las mediciones del rango,
        ordenadas por fecha, con formato "dd/mm/aaaa: temperatura ºC".

        Complejidad: O(log n + k)
            O(log n) para llegar al inicio del rango,
            O(k) para recorrer los k elementos dentro del rango.
        """
        f1 = self._parsear_fecha(fecha1)             # Convertimos fecha1
        f2 = self._parsear_fecha(fecha2)             # Convertimos fecha2
        nodos = self._arbol.rango(f1, f2)            # Obtenemos nodos ordenados

        resultado = []                               # Lista de strings a devolver
        for nodo in nodos:                           # Recorremos cada nodo
            # Formateamos la fecha de vuelta a string "dd/mm/aaaa"
            fecha_str = nodo.fecha.strftime(self.FORMATO_FECHA)
            # Armamos el string con formato pedido y lo agregamos a la lista
            resultado.append(f"{fecha_str}: {nodo.temperatura} ºC")
        return resultado                             # Devolvemos la lista formateada

    def cantidad_muestras(self) -> int:
        """
        Devuelve la cantidad total de muestras almacenadas en la BD.

        Complejidad: O(1)
            Tenemos un contador que se actualiza en cada inserción/borrado,
            así que no necesitamos recorrer nada.
        """
        return self._arbol.cantidad()                # Preguntamos al árbol su contador

    def cargar_desde_archivo(self, ruta_archivo: str):
        """
        Lee un archivo de texto con mediciones y las carga en la BD.

        Formato esperado del archivo (una medición por línea):
            dd/mm/aaaa,temperatura
        Ejemplo:
            01/01/2023,15.3
            02/01/2023,-3.7
            15/06/2023,28.0

        Las líneas que empiezan con '#' se consideran comentarios y se ignoran.
        Las líneas vacías también se ignoran.

        Complejidad: O(m · log(n+m))
            Donde m = cantidad de líneas en el archivo
                  n = muestras ya existentes en la BD
            Cada inserción es O(log n), y hacemos m inserciones.
        """
        cargadas = 0    # Contador de mediciones cargadas exitosamente
        errores = 0     # Contador de líneas con error

        # Abrimos el archivo en modo lectura con codificación UTF-8
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                # enumerate da el número de línea para mensajes de error claros

                linea = linea.strip()  # Eliminamos espacios y saltos de línea

                # Ignoramos líneas vacías y comentarios
                if not linea or linea.startswith("#"):
                    continue  # Saltamos esta línea y pasamos a la siguiente

                try:
                    # Separamos la línea por coma: ["01/01/2023", "15.3"]
                    partes = linea.split(",")

                    if len(partes) != 2:
                        # Si no hay exactamente 2 partes, el formato es inválido
                        raise ValueError("Se esperaban exactamente 2 columnas: fecha,temperatura")

                    fecha_str = partes[0].strip()        # Tomamos la fecha (quitamos espacios)
                    temperatura = float(partes[1].strip())  # Convertimos la temp a float

                    self.guardar_temperatura(temperatura, fecha_str)  # Guardamos en el árbol
                    cargadas += 1                        # Contamos como éxito

                except (ValueError, IndexError) as e:
                    # Si algo falla, avisamos pero continuamos con el resto
                    print(f"  ⚠ Línea {numero_linea} ignorada: {e}")
                    errores += 1                         # Contamos el error

        # Mostramos un resumen al final
        print(f"✔ Carga completada: {cargadas} mediciones cargadas, {errores} errores.")
        return cargadas  # Devolvemos la cantidad de mediciones cargadas


# ==============================================================
# SECCIÓN PRINCIPAL: pruebas y ejemplos de uso
# Se ejecuta solo cuando corremos este archivo directamente.
# ==============================================================
if __name__ == "__main__":

    print("=" * 60)
    print("  TEMPERATURAS_DB — Demo de Kevin Kelvin")
    print("=" * 60)

    # Creamos la base de datos
    db = TemperaturasDB()

    # --------------------------------------------------------
    # Carga manual de algunas mediciones de ejemplo
    # --------------------------------------------------------
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

    # --------------------------------------------------------
    # Mostrar cantidad de muestras
    # --------------------------------------------------------
    print(f"\n📊 Cantidad de muestras: {db.cantidad_muestras()}")

    # --------------------------------------------------------
    # Devolver temperatura de una fecha específica
    # --------------------------------------------------------
    print("\n🔍 Consulta de fecha específica:")
    temp = db.devolver_temperatura("15/06/2023")
    print(f"  Temperatura el 15/06/2023: {temp} ºC")

    temp_no_existe = db.devolver_temperatura("01/01/2000")
    print(f"  Temperatura el 01/01/2000: {temp_no_existe}")  # Debe imprimir None

    # --------------------------------------------------------
    # Máxima y mínima en un rango
    # --------------------------------------------------------
    print("\n🌡 Extremos en rango 01/06/2023 → 30/06/2023:")
    minima, maxima = db.temp_extremos_rango("01/06/2023", "30/06/2023")
    print(f"  Mínima: {minima} ºC")
    print(f"  Máxima: {maxima} ºC")

    # --------------------------------------------------------
    # Listado de temperaturas en un rango
    # --------------------------------------------------------
    print("\n📋 Temperaturas en rango 10/06/2023 → 25/06/2023:")
    lista = db.devolver_temperaturas("10/06/2023", "25/06/2023")
    for item in lista:
        print(f"  {item}")

    # --------------------------------------------------------
    # Borrar una medición
    # --------------------------------------------------------
    print("\n🗑 Borrando medición del 10/06/2023...")
    db.borrar_temperatura("10/06/2023")
    print(f"  Cantidad de muestras ahora: {db.cantidad_muestras()}")
    temp_borrada = db.devolver_temperatura("10/06/2023")
    print(f"  Temperatura el 10/06/2023 (después de borrar): {temp_borrada}")

    # --------------------------------------------------------
    # Carga desde archivo (si existe el archivo de muestra)
    # --------------------------------------------------------
    import os
    ruta = "muestras.csv"  # Cambiá esto a la ruta real del archivo
    if os.path.exists(ruta):
        print(f"\n📂 Cargando desde archivo '{ruta}'...")
        db2 = TemperaturasDB()
        db2.cargar_desde_archivo(ruta)
        print(f"  Total de muestras: {db2.cantidad_muestras()}")
    else:
        print(f"\n📂 (Archivo '{ruta}' no encontrado, saltando carga desde archivo)")

    print("\n" + "=" * 60)
    print("  Fin de la demo. ¡Hasta la próxima, Kevin!")
    print("=" * 60)