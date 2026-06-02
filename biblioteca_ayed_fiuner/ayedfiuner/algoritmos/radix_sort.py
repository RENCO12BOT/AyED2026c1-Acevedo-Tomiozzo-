class Radix_sort:
    def __init__(self, lista):
        # Precondiciones del constructor
        assert isinstance(lista, list), "tiene que ser una lista"
        assert all(isinstance(x, int) for x in lista), \
            "radix sort solo funciona con enteros"
        assert all(x >= 0 for x in lista), \
            "radix sort no acepta numeros negativos"

        self.__lista = lista

    def ordenar(self):
        """
        Ordena la lista usando radix sort, yendo digito por digito.

        Precondiciones:
            - todos los elementos tienen que ser enteros
            - no puede haber numeros negativos (radix sort no los soporta)

        Postcondiciones:
            - la lista queda ordenada de menor a mayor
            - la longitud es la misma que antes
            - los elementos son exactamente los mismos, solo cambia el orden
        """
        #  PRECONDICIONES 
        assert isinstance(self.__lista, list), "la lista tiene que ser una lista"
        assert all(isinstance(x, int) for x in self.__lista), \
            "todos los elementos tienen que ser enteros"
        assert all(x >= 0 for x in self.__lista), \
            "no se aceptan negativos en radix sort"

        if not self.__lista:
            return self.__lista

        # guardo para verificar al final
        longitud_antes = len(self.__lista)
        elementos_antes = sorted(self.__lista)

        if min(self.__lista) < 0:
            raise ValueError("Radix Sort solo admite enteros no negativos")

        cantidad_de_digitos = 0
        for elemento in self.__lista:
            digitos = len(str(elemento))
            if digitos > cantidad_de_digitos:
                cantidad_de_digitos = digitos

        lista_normalizada = [
            str(elemento).zfill(cantidad_de_digitos) for elemento in self.__lista
        ]

        for posicion in range(cantidad_de_digitos - 1, -1, -1):
            lista_auxiliar = [[] for _ in range(10)]
            for elemento in lista_normalizada:
                digito = int(elemento[posicion])
                lista_auxiliar[digito].append(elemento)
            lista_normalizada = [
                elemento for sublista in lista_auxiliar for elemento in sublista
            ]

        self.__lista = [int(elemento) for elemento in lista_normalizada]

        #  POSTCONDICIONES
        assert len(self.__lista) == longitud_antes, \
            "la longitud cambio, algo esta mal"
        assert self.__lista == sorted(self.__lista), \
            "la lista no quedo ordenada, hay un bug en el algoritmo"
        assert sorted(self.__lista) == elementos_antes, \
            "los elementos cambiaron, eso no deberia pasar nunca"

        return self.__lista