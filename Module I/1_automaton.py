'''
José Luis Haro Díaz
1. Automaton
'''

class Automata:
    def __init__(self) -> None:
        self.estado = 'inicio'  #Estado inicial
        self.prohibidos = {'$', '#', '/', '(', '@'}

    def transicion(self, caracter: str) -> None:
        #Si aparece un símbolo del dict de prohibidos, invalida de inmediato
        if caracter in self.prohibidos:
            self.estado = 'invalido'
            return

        if self.estado == 'inicio':
            #Debe iniciar con letra o guion bajo
            if caracter.isalpha() or caracter == '_':
                self.estado = 'valido'
            else:
                self.estado = 'invalido'

        elif self.estado == 'valido':
            #Luego van letras, dígitos o guion bajo
            if caracter.isalnum() or caracter == '_':
                self.estado = 'valido'
            else:
                self.estado = 'invalido'

    def evaluar(self, cadena: str) -> bool:
        self.estado = 'inicio'
        if not cadena:  # Vacio es inválido
            return False
        for caracter in cadena:
            self.transicion(caracter)
            if self.estado == 'invalido':
                return False
        return True


# Pruebas
automata = Automata()
palabras = [
    "variablees",
    "_variablees",
    "1variable",
    "var-name",
    "var_namees",
    "var12es",
    "varNamees",
    "varName_2es",
    "variable$",
    "Jos#e",
    "_LuI$",
    "3hAr-Oooo",
    "d1@zzzz"
]

for palabra in palabras:
    if automata.evaluar(palabra):
        print(f"{palabra} es un identificador válido.")
    else:
        print(f"{palabra} NO es un identificador válido.")
