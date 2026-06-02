import random

class Quicksort:
    def __init__(self, lista):
        # Precondiciones del constructor
        assert isinstance(lista, list), "tiene que ser una lista"
        assert all(isinstance(x, (int, float)) for x in lista), \
            "todos los elementos tienen que ser numericos"

        self.__lista = lista

    def ordenar(self, indice_inicio=None, indice_final=None, lista=None):
        """
        Ordena la lista usando quicksort de forma recursiva.

        Precondiciones:
            - indice_inicio tiene que ser un entero mayor o igual a 0
            - indice_final tiene que ser menor que la longitud de la lista
            - indice_inicio no puede ser mayor que indice_final
            - lista tiene que tener solo numeros

        Postcondiciones:
            - la lista queda ordenada de menor a mayor
            - no se agregan ni se eliminan elementos
            - la longitud se mantiene igual
        """
        if lista is None:
            lista = self.__lista
        if indice_inicio is None:
            indice_inicio = 0
        if indice_final is None:
            indice_final = len(lista) - 1

        # PRECONDICIONES
        assert isinstance(lista, list), "lista tiene que ser una lista"
        assert all(isinstance(x, (int, float)) for x in lista), \
            "los elementos tienen que ser numericos"
        assert isinstance(indice_inicio, int) and indice_inicio >= 0, \
            "indice_inicio tiene que ser un entero no negativo"
        assert isinstance(indice_final, int) and indice_final < len(lista), \
            "indice_final se fue de rango"
        assert indice_inicio <= indice_final, \
            "indice_inicio no puede ser mayor que indice_final"

        # guardo para las postcondiciones (solo en la llamada inicial)
        es_llamada_raiz = (indice_inicio == 0 and indice_final == len(lista) - 1)
        if es_llamada_raiz:
            longitud_antes = len(self.__lista)
            elementos_antes = sorted(self.__lista)

        if indice_inicio < indice_final:
            posicion_pivote = self.__ubicar_pivote(indice_inicio, indice_final, lista)
            self.ordenar(indice_inicio, posicion_pivote - 1, lista)
            self.ordenar(posicion_pivote + 1, indice_final, lista)

        #  POSTCONDICIONES (solo al terminar el ordenamiento completo) 
        if es_llamada_raiz:
            assert len(self.__lista) == longitud_antes, \
                "la longitud cambio, algo salio mal"
            assert self.__lista == sorted(self.__lista), \
                "la lista no quedo ordenada"
            assert sorted(self.__lista) == elementos_antes, \
                "los elementos cambiaron, no deberia pasar"

        return self.__lista

    def __ubicar_pivote(self, indice_inicio, indice_final, lista):
        """
        Acomoda el pivote en su lugar correcto dentro de la lista.

        Precondiciones:
            - indice_inicio tiene que ser menor que indice_final
            - ambos indices tienen que estar dentro del rango de la lista

        Postcondiciones:
            - el indice devuelto esta entre indice_inicio e indice_final
            - todo lo que esta a la izquierda del pivote es menor o igual a el
            - todo lo que esta a la derecha es mayor o igual a el
        """
        # PRECONDICIONES 
        assert isinstance(lista, list), "lista tiene que ser una lista"
        assert 0 <= indice_inicio < len(lista), "indice_inicio fuera de rango"
        assert 0 <= indice_final < len(lista), "indice_final fuera de rango"
        assert indice_inicio < indice_final, \
            "indice_inicio tiene que ser menor que indice_final"

        # elijo el pivote al azar para evitar el peor caso
        pivote_idx = random.randint(indice_inicio, indice_final)
        lista[indice_inicio], lista[pivote_idx] = lista[pivote_idx], lista[indice_inicio]

        pivote = lista[indice_inicio]
        izquierda = indice_inicio + 1
        derecha = indice_final

        while True:
            while izquierda <= derecha and lista[izquierda] <= pivote:
                izquierda += 1
            while izquierda <= derecha and lista[derecha] >= pivote:
                derecha -= 1
            if izquierda <= derecha:
                lista[izquierda], lista[derecha] = lista[derecha], lista[izquierda]
            else:
                break

        lista[indice_inicio], lista[derecha] = lista[derecha], lista[indice_inicio]

        #  POSTCONDICIONES
        pos = derecha
        assert indice_inicio <= pos <= indice_final, \
            "la posicion del pivote quedo fuera de rango"
        assert all(lista[i] <= lista[pos] for i in range(indice_inicio, pos)), \
            "hay elementos a la izquierda del pivote que son mayores, algo fallo"
        assert all(lista[i] >= lista[pos] for i in range(pos + 1, indice_final + 1)), \
            "hay elementos a la derecha del pivote que son menores, algo fallo"

        return derecha