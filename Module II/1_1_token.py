'''
José Luis Haro Díaz
1.1 Token
'''

class Token:
    class Type:
        Numero = "Numero"
        Suma = "Suma"
        Resta = "Resta"
        Multiplicar = "Multiplicar"
        Dividir = "Dividir"
        Fin = "Fin"
        Invalido = "Invalido"

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

class Lexico:
    def __init__(self, origen: str):
        self.origen = origen
        self.index = 0
        self.n = len(origen)

    def next_token(self) -> Token:
        while self.index < self.n and self.origen[self.index].isspace():
            self.index += 1

        if self.index >= self.n:
            return Token(Token.Type.Fin, "")

        c = self.origen[self.index]

        if c.isdigit():
            start = self.index
            self.index += 1
            while self.index < self.n and self.origen[self.index].isdigit():
                self.index += 1
            return Token(Token.Type.Numero, self.origen[start:self.index])

        self.index += 1
        if c == '+':
            return Token(Token.Type.Suma, '+')
        if c == '-':
            return Token(Token.Type.Resta, '-')
        if c == '*':
            return Token(Token.Type.Multiplicar, '*')
        if c == '/':
            return Token(Token.Type.Dividir, '/')

        return Token(Token.Type.Invalido, c)

class Parser:
    def __init__(self, lexer: Lexico):
        self.lexer = lexer
        self.token_actual = lexer.next_token()

    def parse(self):
        while self.token_actual.type != Token.Type.Fin:
            t = self.token_actual
            if t.type == Token.Type.Numero:
                print(f"Number: {t.value}")
            elif t.type in (Token.Type.Suma, Token.Type.Resta, Token.Type.Multiplicar, Token.Type.Dividir):
                print(f"Operator: {t.value}")
            elif t.type == Token.Type.Invalido:
                print(f"Invalid token: {t.value}")
            self.token_actual = self.lexer.next_token()


if __name__ == "__main__":
    expresion = input("Introduce una expresión: ") #Ex. 3+4-5
    lexer = Lexico(expresion)
    parser = Parser(lexer)
    parser.parse()
