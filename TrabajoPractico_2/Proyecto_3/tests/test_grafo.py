import sys
import os

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
    """
    if not isinstance(origen_id, str):
        raise TypeError(f"origen_id debe ser un string. Se recibió: {type(origen_id)}")
    if origen_id not in grafo:
        raise ValueError(f"La aldea origen '{origen_id}' no existe en el grafo.")

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