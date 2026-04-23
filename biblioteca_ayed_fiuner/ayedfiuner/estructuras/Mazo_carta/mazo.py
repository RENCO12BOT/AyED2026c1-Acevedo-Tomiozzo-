from ayedfiuner.estructuras.Mazo_carta.LDE import LDE

class DequeEmptyError(Exception):
    pass

class Mazo:
    
    def __init__ (self):
        self._cartas = LDE()
    
    def poner_carta_arriba(self, carta):
        #Ponemos la carta arriba 
        
        self._cartas.agregar_al_inicio(carta)
        #Agregamos la carta boca arriba al inicio de la lista doblemente enlazada
        
    def poner_carta_abajo(self, carta):
        #Ponemos la carta abajo
        
        self._cartas.agregar_al_final(carta)
        #Agregamos la carta boca arriba al final de la lista doblemente enlazada
            
    def sacar_carta_arriba(self, mostrar = False):
        #Sacamos la carta arriba y antes de mostrar la carta el valor es False por que aun no sabes si la carta es mayor o menor a la del opentente
        
        if self._esta_vacio():
            raise DequeEmptyError("El mazo esta vacío")
        #Si el mazo esta vacio no va a tirar un error diciendo que el mazo esta vacio
        
        carta = self._extraer_carta(0)
        #Extraemos la primera carta del mazo para mostrala y presentar la carta boca abajo
        
        if mostrar:
            #Da vuelta la carta para mostrar el valor
            carta.visible = True   
            
        return carta
        # devuelve la carta que se eligio para mostrarla
    
    def __len__(self):
        #Nos muestra el tamaño de la lista 
        
        return len(self._lista)
        #Devuelve el tamaño de la lista
    
    def __string__(self):
        #Transforma el valor de la carta en string 
        return "{"+",".join([str(carta) for carta in self._cartas])
        # devuelve el valor de la carta en string 
    
    def estavacio(self):
        #lee dentro de la lista si el mazo esta vacio 
        
        return len(self._esta_vacio) == 0
        
    
    
    
    
        