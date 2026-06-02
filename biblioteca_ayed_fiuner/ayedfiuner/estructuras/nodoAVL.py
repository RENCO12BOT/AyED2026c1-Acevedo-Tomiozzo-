from datetime import datetime


class NodoAVL:
    """
    Nodo de un árbol AVL que almacena una fecha y una temperatura.
    """

    def __init__(self, fecha: datetime, temperatura: float):
        """
        Precondición:
            - fecha debe ser un objeto datetime válido.
            - temperatura debe ser un número float (puede ser negativo).
        Postcondición:
            - Se crea un nodo con fecha, temperatura, hijos None y altura 1.
        """
        self.fecha       = fecha
        self.temperatura = temperatura
        self.izquierdo   = None
        self.derecho     = None
        self.altura      = 1
        