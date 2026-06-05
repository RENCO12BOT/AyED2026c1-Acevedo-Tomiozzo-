import os
from ayedfiuner.estructuras.grafos import Grafo, prim


def cargarGrafo(ruta):
    """Lee el archivo de aldeas y construye el grafo."""
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


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    grafo = cargarGrafo(os.path.join(base, '..', 'data', 'aldeas.txt'))

    inicio = grafo.obtenerVertice('Peligros')
    if inicio is None:
        print("No se encontró el vértice 'Peligros'")
        return

    prim(grafo, inicio)

    print("=" * 60)
    print("ALDEAS EN ORDEN ALFABÉTICO")
    print("=" * 60)
    aldeas_ordenadas = sorted(grafo.obtenerVertices())
    for a in aldeas_ordenadas:
        print(f"  {a}")

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

        envia_a = ', '.join(envios) if envios else "— (hoja, no reenvía)"

        print(f"\n  {aldea_id}")
        print(f"    Recibe de : {recibe_de}")
        print(f"    Envía a   : {envia_a}")

        dist_aldea = 0
        for hijo_id in hijos[aldea_id]:
            hijo = grafo.obtenerVertice(hijo_id)
            dist_aldea += hijo.obtenerDistancia()

        if hijos[aldea_id]:
            print(f"    Dist. enviadas: {dist_aldea} leguas")
            distancia_total_global += dist_aldea

    print()
    print("=" * 60)
    print(f"DISTANCIA TOTAL RECORRIDA POR TODAS LAS PALOMAS: {distancia_total_global} leguas")
    print("=" * 60)


if __name__ == '__main__':
    main()