
'''
José Luis Haro Díaz
Práctica 3. Generación de código intermedio
'''

from typing import List

class Automata:
    def __init__(self):
        self.estado = 'inicio'
        self.identificador: List[str] = []
        self.codigo_intermedio: List[str] = []
        self.identificador_actual: str = ""
        self.token_invalido: bool = False
        self.prohibidos = {'$', '#', '/', '(', '@', '.'}

    def procesar_entrada(self, entrada: str) -> None:
        #Procesa toda la cadena y llena identificador[] y codigo_intermedio[].
        self._reiniciar_token()
        self.estado = 'inicio'

        for c in entrada:
            self.procesar_caracter(c)

        self._cerrar_token_si_valido()

    def procesar_caracter(self, c: str) -> None:
        #Cualquier prohibido invalida el token en curso y actúa como separador
        if c in self.prohibidos:
            if self.estado == 'en_id':
                self.token_invalido = True
                self._cerrar_token_si_valido()
            return

        if self.estado == 'inicio':
            #Solo letra o '_' pueden iniciar un identificador
            if c.isalpha() or c == '_':
                self.estado = 'en_id'
                self.identificador_actual = c
                self.token_invalido = False
            else:
                return

        elif self.estado == 'en_id':
            #Dentro del identificador permitimos letra, dígito o '_'
            if c.isalnum() or c == '_':
                self.identificador_actual += c
            else:
                self._cerrar_token_si_valido()
                if c.isalpha() or c == '_':
                    self.estado = 'en_id'
                    self.identificador_actual = c
                    self.token_invalido = False
                else:
                    self.estado = 'inicio'

    def get_identificador(self) -> List[str]:
        return list(self.identificador)

    def get_codigo_intermedio(self) -> List[str]:
        return list(self.codigo_intermedio)

    def _reiniciar_token(self) -> None:
        self.identificador_actual = ""
        self.token_invalido = False

    def _es_identificador_valido(self, s: str) -> bool:
        if not s:
            return False
        if not (s[0].isalpha() or s[0] == '_'):
            return False
        if any(ch in self.prohibidos for ch in s):
            return False
        return all(ch.isalnum() or ch == '_' for ch in s)

    def _cerrar_token_si_valido(self) -> None:
        if self.estado == 'en_id':
            if not self.token_invalido and self._es_identificador_valido(self.identificador_actual):
                self.identificador.append(self.identificador_actual)
                self.codigo_intermedio.append("IDENTIFICADOR: " + self.identificador_actual)
        self._reiniciar_token()
        self.estado = 'inicio'


def main():
    entrada = "variable1 _var2 anotherVar3 var invalid-var $badVar @haro /emma (jose) .diaZ 30RomEro"  
    automata = Automata()
    automata.procesar_entrada(entrada)

    print("Identificadores encontrados:")
    print(automata.get_identificador())

    print("\nCódigo intermedio generado:")
    for line in automata.get_codigo_intermedio():
        print(line)

if __name__ == "__main__":
    main()
