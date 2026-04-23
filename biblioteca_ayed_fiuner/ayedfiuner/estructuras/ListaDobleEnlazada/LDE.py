class Nodo:
    """representa un nodo de una lista doblemente enlazada"""
    def __init__(self,valor):
        self .__valor = valor
        self .__anterior = None
        self .__siguiente = None
        
    def asignar_siguiente(self, nodo_siguiente):
        self.__siguiente = nodo_siguiente
        
    def obtener_siguiente(self):
        return self.__siguiente
    
    def asignar_anterior(self,nodo_anterior):
        self .__anterior = nodo_anterior
        
    def obtener_anterior(self):
        return self.__anterior
    
    def obtener_valor(self):
        return self.__valor
    
class ListaDobleEnlazada:
    """ representa una lista doblemente enlazada"""
    def __init__(self,):
        self.__cabeza = None
        self.__cola = None
        self .__tamanio = 0
    # PUNTO 1 
    
    def esta_vacia(self):
        return self.__cabeza is None
    
    # PUNTO 2
    def agregar_al_inicio(self,item):
        nuevo = Nodo(item)
        if self.esta_vacia():
            self.__cabeza = nuevo
            self.__cola = nuevo 
        else:
            nuevo.asignar_siguiente(self.__cabeza)
            self.__cabeza.asignar_anterior(nuevo)
            self.__cabeza = nuevo 
        self.__tamanio += 1
        
    # PUNTO 3
    def   agregar_al_final(self, item):
        nuevo = Nodo(item)
        if self.esta_vacia():
            self.__cabeza = nuevo
            self.__cola = nuevo       
        else:
            self.__cola.asignar_siguiente(nuevo)
            nuevo.asignar_anterior(self.__cola)
            self.__cola = nuevo
        self.__tamanio += 1
        
    # PUNTO 4        
    def __len__(self):
        return self.__tamanio
     
    # PUNTO 5 
    def insertar(self, item, posicion=None):
       if posicion is None:
          self.agregar_al_final(item)
       return
       if posicion < 0 or posicion > self.__tamanio:
          raise IndexError("Posición fuera de rango")
       if posicion == 0:
        self.agregar_al_inicio(item)
       elif posicion == self.__tamanio:
        self.agregar_al_final(item)
       else:
        actual = self.__cabeza
        i = 0
        while i < posicion:
            actual = actual.obtener_siguiente()
            i += 1
        nuevo = nodo(item)
        anterior = actual.obtener_anterior()
        nuevo.asignar_siguiente(actual)
        nuevo.asignar_anterior(anterior)
        anterior.asignar_siguiente(nuevo)
        actual.asignar_anterior(nuevo)
        self.__tamanio += 1
        
    # Punto 6
    def extraer(self, posicion=None):
        if self.esta_vacia():
           raise IndexError("La lista está vacía")
        if posicion is None:
           posicion = self.__tamanio - 1
        if posicion < 0 or posicion >= self.__tamanio:
           raise IndexError("Posición fuera de rango")
        if posicion == 0:
           valor = self.__cabeza.obtener_valor()
           self.__cabeza = self.__cabeza.obtener_siguiente()
           if self.__cabeza is not None:
            self.__cabeza.asignar_anterior(None)
           else:
              self.__cola = None
        elif posicion == self.__tamanio - 1:
             valor = self.__cola.obtener_valor()
             self.__cola = self.__cola.obtener_anterior()
             if self.__cola is not None:
                self.__cola.asignar_siguiente(None)
             else:
                  self.__cabeza = None
        else:
             actual = self.__cabeza
        i = 0
        while i < posicion:
            actual = actual.obtener_siguiente()
            i += 1
        valor = actual.obtener_valor()
        anterior = actual.obtener_anterior()
        siguiente = actual.obtener_siguiente()
        anterior.asignar_siguiente(siguiente)
        siguiente.asignar_anterior(anterior)
        self.__tamanio -= 1
        return valor
    
    # Punto 7
    def copiar(self):
        nueva = ListaDobleEnlazada()
        actual = self.__cabeza
        while actual is not None:
            nueva.agregar_al_final(actual.obtener_valor())
            actual = actual.obtener_siguiente()
        return nueva
    
    # Punto 8
    def invertir(self):
        actual = self.__cabeza
        while actual is not None:
            siguiente = actual.obtener_siguiente()
            actual.asignar_siguiente(actual.obtener_anterior())
            actual.asignar_anterior(siguiente)
            actual = siguiente
        self.__cabeza, self.__cola = self.__cola, self.__cabeza
        
    # Punto 9
    def concatenar(self, otra_lista):
        if self.esta_vacia():
            self.__cabeza = otra_lista.__cabeza
            self.__cola = otra_lista.__cola
        elif not otra_lista.esta_vacia():
            self.__cola.asignar_siguiente(otra_lista.__cabeza)
            otra_lista.__cabeza.asignar_anterior(self.__cola)
            self.__cola = otra_lista.__cola
        self.__tamanio += len(otra_lista)
        
    # Punto 10
    def __iter__ (self):
        actual = self.__cabeza
        while actual is not None:
            yield actual.obtener_valor()
            actual = actual.obtener_siguiente()
            
    # Punto 11
    def __add__ (self, otra_lista):
        nueva_lista = ListaDobleEnlazada()
        for item in self:
            nueva_lista.agregar_al_final(item)
        for item in otra_lista:
            nueva_lista.agregar_al_final(item)
        return nueva_lista
    @property
    def cabeza(self):
        return self.__cabeza
    @property
    def cola(self):
        return self.__cola
    