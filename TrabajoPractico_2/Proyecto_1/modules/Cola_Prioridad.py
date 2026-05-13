from modules.monticulo_binario import monticulo_binario

class cola_prioridad:
    def __init__(self):
         self.__monticulo = monticulo_binario()
    
    def insertar(self,paciente):
        self.__monticulo.insertar(paciente)
    
    def extraer(self):
        if self.__monticulo.esta_vacia():
            return None
        clave_orden, dato = self.__monticulo.eliminarMinimo()
        return dato
    
    def estaVacio(self):
        return self.__monticulo.esta_vacia()
    
    def verProximo(self):
        if self.__monticulo.esta_vacia():
            return None
        clave_orden, dato = self.__monticulo._monticulo_lista[1]
        return dato
     
    def  verTodos(self):
        if self.estaVacio():
            return None 
        clave_orden, dato = self.__monticulo._monticulo_lista[1]
        return dato 
     
    def __len__(self):
        return self.__monticulo._tamano_actual
    
    def __iter__(self):
        return iter(self.__monticulo._monticulo_lista[1:])
    
    