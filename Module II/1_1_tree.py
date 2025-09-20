'''
José Luis Haro Díaz
1.1 Tree
'''

class Token:
    class Type:
        Numero = "Numero"
        Suma = "Suma"
        Resta = "Resta"
        Multiplica = "Multiplica"
        Divide = "Divide"
        Fin = "Fin"
        Invalido = "Invalido"

    def __init__(self, type_, value):
        self.type = type_
        self.value = value


class Lexer:
    def __init__(self, origen: str):
        self.origen = origen
        self.index = 0
        self.n = len(origen)

    def next_token(self) -> Token:
        #Saltar espacios
        while self.index < self.n and self.origen[self.index].isspace():
            self.index += 1

        #Fin
        if self.index >= self.n:
            return Token(Token.Type.Fin, "")

        c = self.origen[self.index]

        #Número (multi-dígito)
        if c.isdigit():
            start = self.index
            self.index += 1
            while self.index < self.n and self.origen[self.index].isdigit():
                self.index += 1
            return Token(Token.Type.Numero, self.origen[start:self.index])

        #Operadores
        self.index += 1
        if c == '+':
            return Token(Token.Type.Suma, '+')
        if c == '-':
            return Token(Token.Type.Resta, '-')
        if c == '*':
            return Token(Token.Type.Multiplica, '*')
        if c == '/':
            return Token(Token.Type.Divide, '/')

        return Token(Token.Type.Invalido, c)


class TreeNode:
    def __init__(self, token: Token, left=None, right=None):
        self.token = token
        self.left = left
        self.right = right

    def print_tree(self, level: int = 0):
        indent = "    " * level
        t = self.token
        if t.type == Token.Type.Numero:
            print(f"{indent}Numero: {t.value}")
        elif t.type == Token.Type.Suma:
            print(f"{indent}Suma: {t.value}")
            if self.left:  self.left.print_tree(level + 1)
            if self.right: self.right.print_tree(level + 1)
        elif t.type == Token.Type.Resta:
            print(f"{indent}Resta: {t.value}")
            if self.left:  self.left.print_tree(level + 1)
            if self.right: self.right.print_tree(level + 1)
        elif t.type == Token.Type.Multiplica:
            print(f"{indent}Multiplica: {t.value}")
            if self.left:  self.left.print_tree(level + 1)
            if self.right: self.right.print_tree(level + 1)
        elif t.type == Token.Type.Divide:
            print(f"{indent}Divide: {t.value}")
            if self.left:  self.left.print_tree(level + 1)
            if self.right: self.right.print_tree(level + 1)
        else:
            print(f"{indent}{t.type}: {t.value}")

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.token_actual = lexer.next_token()

    def eat(self, token_type: str):
        if self.token_actual.type == token_type:
            self.token_actual = self.lexer.next_token()
        else:
            raise SyntaxError(
                f"Se esperaba {token_type} y llegó {self.token_actual.type}"
            )

    def parse(self) -> TreeNode:
        raiz = self.expr()
        if self.token_actual.type != Token.Type.Fin:
            raise SyntaxError("Símbolos extra después de la expresión")
        return raiz

    def expr(self) -> TreeNode:
        node = self.termino()
        while self.token_actual.type in (Token.Type.Suma, Token.Type.Resta):
            op = self.token_actual
            self.eat(op.type)
            right = self.termino()
            node = TreeNode(op, left=node, right=right)  #Asociatividad izquierda
        return node

    def termino(self) -> TreeNode:
        node = self.factor()
        while self.token_actual.type in (Token.Type.Multiplica, Token.Type.Divide):
            op = self.token_actual
            self.eat(op.type)
            right = self.factor()
            node = TreeNode(op, left=node, right=right)  #Asociatividad izquierda
        return node

    def factor(self) -> TreeNode:
        t = self.token_actual
        if t.type == Token.Type.Numero:
            self.eat(Token.Type.Numero)
            return TreeNode(t)
        raise SyntaxError(f"Token inesperado: {t.type} '{t.value}'")

#test: 9*4/5-7+1*3+2

if __name__ == "__main__":
    expr = input("Introduce una expresión: ").strip()
    lexer = Lexer(expr)
    parser = Parser(lexer)
    arbol = parser.parse()
    arbol.print_tree()
