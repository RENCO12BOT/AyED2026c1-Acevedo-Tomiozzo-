from ayedfiuner.estructuras.LDE import ListaDobleEnlazada
from cartas import Carta

class DequeEmptyError(Exception):
    pass

class Mazo:
    
    def __init__(self):
        self._cartas = ListaDobleEnlazada()

    def poner_carta_arriba(self, carta):
        """
        Pone una carta en la parte de arriba del mazo.

        Precondiciones:
            - carta tiene que ser una instancia de Carta

        Postcondiciones:
            - el mazo tiene una carta mas que antes
            - la carta queda en la primera posicion
        """
        # PRECONDICIONES
        if not isinstance(carta, Carta):
            raise TypeError("solo se pueden agregar instancias de Carta al mazo")

        tamanio_antes = len(self._cartas)

        self._cartas.agregar_al_inicio(carta)

        # --- POSTCONDICIONES ---
        if len(self._cartas) != tamanio_antes + 1:
            raise RuntimeError("el mazo no aumento de tamanio correctamente")

    def poner_carta_abajo(self, carta):
        """
        Pone una carta en la parte de abajo del mazo.

        Precondiciones:
            - carta tiene que ser una instancia de Carta

        Postcondiciones:
            - el mazo tiene una carta mas que antes
            - la carta queda en la ultima posicion
        """
        # --- PRECONDICIONES ---
        if not isinstance(carta, Carta):
            raise TypeError("solo se pueden agregar instancias de Carta al mazo")

        tamanio_antes = len(self._cartas)

        self._cartas.agregar_al_final(carta)

        # --- POSTCONDICIONES ---
        if len(self._cartas) != tamanio_antes + 1:
            raise RuntimeError("el mazo no aumento de tamanio correctamente")

    def sacar_carta_arriba(self, mostrar=False):
        """
        Saca y devuelve la carta de arriba del mazo.

        Precondiciones:
            - el mazo no puede estar vacio
            - mostrar tiene que ser un booleano

        Postcondiciones:
            - el mazo tiene una carta menos que antes
            - la carta devuelta es una instancia de Carta
            - si mostrar es True, la carta devuelta tiene visible = True
        """
        # PRECONDICIONES
        if self._esta_vacio():
            raise DequeEmptyError("el mazo esta vacio, no hay carta para sacar")
        if not isinstance(mostrar, bool):
            raise TypeError("mostrar tiene que ser True o False")

        tamanio_antes = len(self._cartas)

        carta = self._cartas.extraer(0)
        if mostrar:
            carta.visible = True

        #POSTCONDICIONES 
        if len(self._cartas) != tamanio_antes - 1:
            raise RuntimeError("el mazo no disminuyo de tamanio correctamente")
        if not isinstance(carta, Carta):
            raise RuntimeError("lo que se saco no es una Carta, algo salio muy mal")
        if mostrar and not carta.visible:
            raise RuntimeError("la carta tendria que ser visible pero no lo es")

        return carta

    def _esta_vacio(self):
        return len(self._cartas) == 0

    def __len__(self):
        return len(self._cartas)

    def __str__(self):
        return "{" + ",".join([str(carta) for carta in self._cartas]) + "}"
    
    
    
        