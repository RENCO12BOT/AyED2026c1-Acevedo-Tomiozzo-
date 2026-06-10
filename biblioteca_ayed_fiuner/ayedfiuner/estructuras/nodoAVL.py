from datetime import datetime


class NodoAVL:
    """
    Nodo de un árbol AVL que almacena una fecha y una temperatura.
    """

    def __init__(self, clave, valor):        
        """
        Precondición:
            - fecha debe ser un objeto datetime válido.
            - temperatura debe ser un número float (puede ser negativo).
        Postcondición:
            - Se crea un nodo con fecha, temperatura, hijos None y altura 1.
        """
        self.clave     = clave
        self.valor     = valor
        self.altura    = 1
        self.izquierdo = None
        self.derecho   = None
        