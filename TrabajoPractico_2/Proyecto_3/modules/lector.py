"""
Encuentra el Árbol de Expansión Mínima (MST) desde 'Peligros'
para distribuir noticias a todas las aldeas con el mínimo recorrido total.
"""

import os
from ayedfiuner.estructuras.grafos import Grafo, prim


def cargarGrafo(ruta):
    """
    Lee el archivo de aldeas y construye el grafo no dirigido.

    Precondición:
        - ruta es un string con la ruta válida a un archivo .txt existente.
        - Cada línea es: 'Aldea1, Aldea2, distancia' o 'Aldea' (vértice suelto).
    Postcondición:
        - Retorna un Grafo con todos los vértices y aristas no dirigidas.
    Excepciones:
        - FileNotFoundError si el archivo no existe.
        - ValueError si una línea tiene formato inválido o distancia no numérica.
    """
    if not os.path.isfile(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    grafo = Grafo()

    with open(ruta, encoding='utf-8') as f:
        for num_linea, linea in enumerate(f, start=1):
            linea = linea.strip()
            if not linea:
                continue

            partes = [p.strip() for p in linea.split(',')]

            if len(partes) == 3:
                origen, destino, costo_str = partes
                try:
                    costo = int(costo_str)
                except ValueError:
                    raise ValueError(
                        f"Línea {num_linea}: la distancia '{costo_str}' no es un entero válido."
                    )
                grafo.agregarArista(origen, destino, costo)

            elif len(partes) == 1:
                grafo.agregarVertice(partes[0])

            else:
                raise ValueError(
                    f"Línea {num_linea}: formato inesperado → '{linea}'"
                )

    return grafo


def construirMapaHijos(grafo):
    """
    Construye un diccionario aldea_id → lista de hijos en el MST.

    Precondición:
        - Se ejecutó prim() sobre el grafo previamente.
    Postcondición:
        - Retorna dict donde cada clave es un id de aldea y el valor
          es la lista de ids de las aldeas que reciben la noticia desde ella.
    """
    hijos = {v: [] for v in grafo.obtenerVertices()}
    for v in grafo:
        pred = v.obtenerPredecesor()
        if pred is not None:
            hijos[pred.obtenerId()].append(v.obtenerId())
    return hijos


def mostrarResultados(grafo, origen_id='Peligros'):
    """
    Muestra los resultados del MST por consola:
      1. Lista alfabética de aldeas.
      2. Para cada aldea: de quién recibe y a quiénes envía.
      3. Distancia total recorrida por todas las palomas.

    Precondición:
        - Se ejecutó prim() sobre el grafo desde el vértice con id=origen_id.
        - origen_id existe en el grafo.
    Postcondición:
        - Imprime los tres bloques de información requeridos por la consigna.
    """
    aldeas_ordenadas = sorted(grafo.obtenerVertices())
    hijos = construirMapaHijos(grafo)

    # --- Bloque 1: lista alfabética ---
    print("=" * 60)
    print("ALDEAS EN ORDEN ALFABÉTICO")
    print("=" * 60)
    for aldea in aldeas_ordenadas:
        print(f"  {aldea}")

    # --- Bloque 2: árbol de distribución ---
    print()
    print("=" * 60)
    print(f"ÁRBOL DE DISTRIBUCIÓN (MST desde {origen_id})")
    print("=" * 60)

    distancia_total = 0

    for aldea_id in aldeas_ordenadas:
        v = grafo.obtenerVertice(aldea_id)
        pred = v.obtenerPredecesor()
        envios = sorted(hijos[aldea_id])

        if aldea_id == origen_id:
            recibe_de = "— (origen, no recibe)"
        elif pred is None:
            recibe_de = "⚠ NO ALCANZABLE desde el origen"
        else:
            recibe_de = pred.obtenerId()

        envia_a = ', '.join(envios) if envios else "— (hoja, no reenvía)"

        print(f"\n  {aldea_id}")
        print(f"    Recibe de : {recibe_de}")
        print(f"    Envía a   : {envia_a}")

        # distancia enviada = suma de pesos de aristas hacia sus hijos
        dist_aldea = sum(
            grafo.obtenerVertice(hijo_id).obtenerDistancia()
            for hijo_id in hijos[aldea_id]
        )
        if hijos[aldea_id]:
            print(f"    Leguas enviadas desde aquí: {dist_aldea}")
            distancia_total += dist_aldea

    # --- Bloque 3: distancia total ---
    print()
    print("=" * 60)
    print(f"DISTANCIA TOTAL RECORRIDA POR TODAS LAS PALOMAS: {distancia_total} leguas")
    print("=" * 60)


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    ruta_aldeas = os.path.join(base, 'data', 'aldeas.txt')

    try:
        grafo = cargarGrafo(ruta_aldeas)
    except (FileNotFoundError, ValueError) as e:
        print(f"[ERROR] al cargar el grafo: {e}")
        return

    inicio = grafo.obtenerVertice('Peligros')
    if inicio is None:
        print("[ERROR] No se encontró el vértice 'Peligros' en el grafo.")
        return

    prim(grafo, inicio)
    mostrarResultados(grafo, origen_id='Peligros')


if __name__ == '__main__':
    main()