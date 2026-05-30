class Carta:
    
    VALORES_VALIDOS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    PALOS_VALIDOS = ['♣','♦','♥','♠']
    
    def __init__(self, valor='', palo=''):
        #  PRECONDICIONES 
        if not isinstance(valor, str):
            raise TypeError("el valor tiene que ser un string")
        if not isinstance(palo, str):
            raise TypeError("el palo tiene que ser un string")
        if valor and valor not in self.VALORES_VALIDOS:
            raise ValueError(f"el valor '{valor}' no es valido, tiene que ser uno de {self.VALORES_VALIDOS}")
        if palo and palo not in self.PALOS_VALIDOS:
            raise ValueError(f"el palo '{palo}' no es valido, tiene que ser uno de {self.PALOS_VALIDOS}")
        
        self.valor = valor
        self.palo = palo
        self.visible: bool = False

    @property
    def visible(self):
        return self._visible
        
    @visible.setter
    def visible(self, visible):
        #  PRECONDICIONES 
        if not isinstance(visible, bool):
            raise TypeError("visible tiene que ser True o False")
        self._visible = visible
        
    @property
    def valor(self):
        return self._valor
    
    @valor.setter
    def valor(self, valor):
        # --- PRECONDICIONES ---
        if not isinstance(valor, str):
            raise TypeError("el valor tiene que ser un string")
        if valor and valor not in self.VALORES_VALIDOS:
            raise ValueError(f"el valor '{valor}' no es valido")
        self._valor = valor
        
    @property
    def palo(self):
        return self._palo
    
    @palo.setter
    def palo(self, palo):
        #  PRECONDICIONES 
        if not isinstance(palo, str):
            raise TypeError("el palo tiene que ser un string")
        if palo and palo not in self.PALOS_VALIDOS:
            raise ValueError(f"el palo '{palo}' no es valido")
        self._palo = palo

    def _valor_numerico(self):
        """
        Devuelve el valor numerico de la carta.

        Precondiciones:
            - la carta tiene que tener un valor asignado y valido

        Postcondiciones:
            - devuelve un entero entre 2 y 14
        """
        #  PRECONDICIONES 
        if not self._valor:
            raise ValueError("la carta no tiene valor asignado todavia")

        valores = ['J', 'Q', 'K', 'A']
        if self.valor in valores:
            idx = valores.index(self.valor)
            resultado = 11 + idx
        else:
            resultado = int(self.valor)

        #  POSTCONDICIONES 
        if not isinstance(resultado, int):
            raise RuntimeError("el valor numerico tendria que ser un entero")
        if not (2 <= resultado <= 14):
            raise RuntimeError(f"el valor numerico {resultado} esta fuera del rango esperado (2-14)")

        return resultado

    def __gt__(self, otra):
        """
        Compara dos cartas por su valor numerico.

        Precondiciones:
            - otra tiene que ser una instancia de Carta
            - ambas cartas tienen que tener un valor asignado

        Postcondiciones:
            - devuelve True si esta carta es mayor, False si no
        """
        #  PRECONDICIONES 
        if not isinstance(otra, Carta):
            raise TypeError("solo se puede comparar con otra Carta")
        if not self._valor or not otra._valor:
            raise ValueError("las dos cartas tienen que tener un valor para poder compararse")

        resultado = self._valor_numerico() > otra._valor_numerico()

        #  POSTCONDICIONES 
        if not isinstance(resultado, bool):
            raise RuntimeError("la comparacion tendria que devolver un booleano")

        return resultado
        
    def __str__(self):
        if self.visible == False:
            return "-X"
        else:
            return self.valor + self.palo
    
    def __repr__(self):
        return str(self)
    