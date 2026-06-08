import os
import sys

# Ajustar los imports según la estructura de tu proyecto.
from ayedfiuner.estructuras.grafos import Grafo, prim

def cargar_grafo_desde_archivo(ruta_archivo):
    """
    Lee el archivo de aldeas y construye un Grafo no dirigido.
    """
    grafo = Grafo()
    
    if not os.path.exists(ruta_archivo):
        print(f"Error: No se encontró el archivo en {ruta_archivo}")
        sys.exit(1)

    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        for numero_linea, linea in enumerate(archivo, 1):
            linea = linea.strip()
            if not linea:
                continue
            
            partes = [p.strip() for p in linea.split(',')]
            
            if len(partes) == 3:
                origen, destino, peso_str = partes
                try:
                    peso = int(peso_str)
                    grafo.agregarArista(origen, destino, peso)
                except ValueError:
                    print(f"Advertencia: Peso inválido en línea {numero_linea}: '{linea}'")
                    
    return grafo


def resolver_problema():
    # Construimos la ruta dinámica hacia ../data/aldeas.txt basándonos en la ubicación de lector.py
    ruta_actual = os.path.dirname(__file__)
    ruta_txt = os.path.abspath(os.path.join(ruta_actual, '..', 'data', 'aldeas.txt'))
    
    # 1. Cargar el grafo
    grafo = cargar_grafo_desde_archivo(ruta_txt)
    
    # 2. Obtener y mostrar la lista de aldeas en orden alfabético
    aldeas_alfabetico = sorted(list(grafo.obtenerVertices()))
    print("1. LISTA DE ALDEAS EN ORDEN ALFABÉTICO:")
    for aldea in aldeas_alfabetico:
        print(f" * {aldea}")
    print()

    # 3. Ejecutar el algoritmo de Prim desde la aldea inicial "Peligros"
    nodo_inicio = grafo.obtenerVertice("Peligros")
    if not nodo_inicio:
        print("Error: La aldea de inicio 'Peligros' no se encuentra en el mapa.")
        return

    prim(grafo, nodo_inicio)

    # 4. Procesar el árbol de expansión mínima para responder los puntos 2 y 3
    replicas_enviadas_desde = {aldea: [] for aldea in aldeas_alfabetico}
    distancia_total_mst = 0

    for v in grafo:
        predecesor = v.obtenerPredecesor()
        if predecesor is not None:
            id_predecesor = predecesor.obtenerId()
            id_actual = v.obtenerId()
            replicas_enviadas_desde[id_predecesor].append(id_actual)
            distancia_total_mst += v.obtenerDistancia()

    print("2. RUTAS DE RECEPCIÓN Y ENVÍO DE RÉPLICAS:")
    for aldea in aldeas_alfabetico:
        v = grafo.obtenerVertice(aldea)
        predecesor = v.obtenerPredecesor()
        
        if aldea == "Peligros":
            origen_noticia = "ORIGEN (Inicia el envío de noticias William)"
        elif predecesor is not None:
            origen_noticia = predecesor.obtenerId()
        else:
            origen_noticia = "INCOMPRENSIBLE / NO ALCANZABLE"

        destinos = replicas_enviadas_desde[aldea]
        destinos_str = ", ".join(destinos) if destinos else "Ninguna (Aldea receptora final)"

        print(f"Aldea: {aldea}")
        print(f"   Recibe noticia desde: {origen_noticia}")
        print(f"   Envía réplicas a: {destinos_str}")
    print()

    print("3. EFICIENCIA DEL ENVÍO DE LA NOTICIA:")
    print(f"Suma total de distancias recorridas por las palomas: {distancia_total_mst} leguas.")


if __name__ == "__main__":
    resolver_problema()