from modules.LDE import ListaDobleEnlazada


class DequeEmptyError(Exception):
    pass

class Mazo:

    def __init__(self):
        self._cartas = ListaDobleEnlazada()

    def poner_carta_arriba(self, carta):
        self._cartas.agregar_al_inicio(carta)

    def poner_carta_abajo(self, carta):
        self._cartas.agregar_al_final(carta)

    def sacar_carta_arriba(self, mostrar=False):
        if self._esta_vacio():
            raise DequeEmptyError("El mazo está vacío")
        carta = self._cartas.extraer(0)   # ← usamos extraer directamente
        if mostrar:
            carta.visible = True
        return carta

    def _esta_vacio(self):                
        return len(self._cartas) == 0

    def __len__(self):
        return len(self._cartas)          

    def __str__(self):                    
        return "{" + ",".join([str(carta) for carta in self._cartas]) + "}"
    
    
    
    
        