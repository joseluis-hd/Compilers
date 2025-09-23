'''
José Luis Haro Díaz
3. Semantic Automaton
'''

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional


# -----------------------------
# Definiciones de Token
# -----------------------------
class TokenType(Enum):
    Numero = auto()
    Suma = auto()
    Resta = auto()
    Fin = auto()
    Invalido = auto()


@dataclass
class Token:
    type: TokenType
    value: Optional[str] = None


# -----------------------------
# Analizador Léxico (Lexer)
# -----------------------------
class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current = self.text[self.pos] if self.text else '\0'

    def _siguiente(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current = '\0'  #fin de cadena
        else:
            self.current = self.text[self.pos]

    def _saltar_espacios(self):
        while self.current != '\0' and self.current.isspace():
            self._siguiente()

    def _leer_numero(self) -> str:
        #Devuelve un número entero (multi-dígito).
        inicio = self.pos
        while self.current.isdigit():
            self._siguiente()
        return self.text[inicio:self.pos]

    def get_next_token(self) -> Token:
        #Produce el siguiente token.
        while self.current != '\0':
            if self.current.isspace():
                self._saltar_espacios()
                continue

            if self.current.isdigit():
                lex = self._leer_numero()
                return Token(TokenType.Numero, lex)

            if self.current == '+':
                self._siguiente()
                return Token(TokenType.Suma, '+')

            if self.current == '-':
                self._siguiente()
                return Token(TokenType.Resta, '-')

            #Cualquier otro carácter es inválido
            inval = self.current
            self._siguiente()
            return Token(TokenType.Invalido, inval)

        return Token(TokenType.Fin, None)

class Analizador:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.error_msg: Optional[str] = None

    def _eat(self, expected: TokenType) -> bool:
        if self.current_token.type == expected:
            self.current_token = self.lexer.get_next_token()
            return True
        self.error_msg = f"Se esperaba {expected.name} y llegó {self.current_token.type.name}"
        return False

    def gramatica(self) -> bool:
        #Debe iniciar con número
        if self.current_token.type == TokenType.Numero:
            print(f"Número encontrado: {self.current_token.value}")
            if not self._eat(TokenType.Numero):
                print("Token inválido")
                return False
        elif self.current_token.type == TokenType.Fin:
            self.error_msg = "Expresión vacía"
            print("Token inválido")
            return False
        elif self.current_token.type == TokenType.Invalido:
            print(f"Token inválido: {self.current_token.value}")
            return False
        else:
            print("Token inválido")
            self.error_msg = "La expresión debe iniciar con un número"
            return False

        #{ ( + | - ) Numero }*
        while self.current_token.type in (TokenType.Suma, TokenType.Resta, TokenType.Invalido):
            if self.current_token.type == TokenType.Invalido:
                print(f"Token inválido: {self.current_token.value}")
                return False

            #operador
            op = self.current_token
            print(f"Operador: {op.value}")
            if not self._eat(op.type):
                print("Token inválido")
                return False

            #número después del operador
            if self.current_token.type == TokenType.Numero:
                print(f"Número encontrado: {self.current_token.value}")
                if not self._eat(TokenType.Numero):
                    print("Token inválido")
                    return False
            else:
                print("Token inválido")
                self.error_msg = "Se esperaba un número después del operador"
                return False

        if self.current_token.type == TokenType.Fin:
            return True
        self.error_msg = "Símbolos extra después de la expresión"
        print("Token inválido")
        return False


# -----------------------------
# Main
#Ej. 12 + 3 - 7
# -----------------------------
if __name__ == "__main__":
    entrada = input("Ingrese una expresión: ").strip()
    lexer = Lexer(entrada)
    analizador = Analizador(lexer)

    es_valida = analizador.gramatica()
    if es_valida:
        print("Expresión válida")
    else:
        if analizador.error_msg:
            print(f"Expresión inválida: {analizador.error_msg}")
        else:
            print("Error.")
