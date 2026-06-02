class Burbuja:
    def __init__(self, lista):
        # Verifico que me pasen una lista y que tenga numeros
        assert isinstance(lista, list), "Tiene que ser una lista"
        assert all(isinstance(x, (int, float)) for x in lista), "Los elementos tienen que ser numeros"

        self.__lista = lista

    def ordenar_lista(self):
        """
        Ordena la lista de menor a mayor con el metodo burbuja.

        Precondiciones:
            - la lista no puede estar vacia (bueno, puede pero no hace nada)
            - todos los elementos tienen que ser int o float para poder compararlos

        Postcondiciones:
            - la lista queda ordenada de menor a mayor
            - la cantidad de elementos es la misma que antes
            - no se pierden ni se agregan elementos
        """

        # PRECONDICIONES 
        assert isinstance(self.__lista, list), "la lista tiene que ser una lista"
        assert all(isinstance(x, (int, float)) for x in self.__lista), \
            "todos los elementos tienen que ser numericos"

        # guardo estos datos para verificar al final que no cambio nada raro
        longitud_antes = len(self.__lista)
        elementos_antes = sorted(self.__lista)

        contador = 0
        while contador < len(self.__lista):
            esta_ordenada = True
            tamaño_lista = len(self.__lista) - contador
            for i in range(1, tamaño_lista):
                if self.__lista[i] < self.__lista[i - 1]:
                    aux = self.__lista[i]
                    self.__lista[i] = self.__lista[i - 1]
                    self.__lista[i - 1] = aux
                    esta_ordenada = False
            if esta_ordenada:
                break
            contador += 1

        # POSTCONDICIONES 
        # me fijo que no se haya perdido ni agregado ningun elemento
        assert len(self.__lista) == longitud_antes, \
            "la longitud cambio, algo salio mal"
        # chequeo que este ordenada
        assert self.__lista == sorted(self.__lista), \
            "la lista no quedo ordenada, revisar el algoritmo"
        # chequeo que los elementos sean los mismos de antes
        assert sorted(self.__lista) == elementos_antes, \
            "los elementos cambiaron, eso no deberia pasar"

        return self.__lista

    def __str__(self):
        return f"{self.__lista}"