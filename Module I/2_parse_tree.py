'''
José Luis Haro Díaz
Práctica 2. Árbol de Parseo
'''

import sys
import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass

#This class represents a token with its type, value, and position
class Token:
    type: str
    value: Optional[str] = None
    pos: int = -1

#This function converts a string into a list of tokens
def tokenize(s: str) -> List[Token]:
    s = s.replace(" ", "") #Delate spaces
    tokens: List[Token] = []

    i = 0
    num_re = re.compile(r'\d+(\.\d+)?')  #Ints and floats
    while i < len(s):
        c = s[i]
        if c.isdigit():
            m = num_re.match(s, i)
            t = m.group(0)
            tokens.append(Token("NUM", t, i))
            i = m.end()
            continue
        if c in "+-*/^":
            tokens.append(Token("OP", c, i))
            i += 1
            continue
        if c == "(":
            tokens.append(Token("LPAREN", c, i))
            i += 1
            continue
        if c == ")":
            tokens.append(Token("RPAREN", c, i))
            i += 1
            continue
        raise SyntaxError(f"Caracter inválido '{c}' en posición {i}")

    #This function inserts implicit multiplication tokens where needed
    def is_primary(tok: Token) -> bool:
        return tok.type in ("NUM", "RPAREN")

    #This function checks if a token can follow a primary expression
    def can_follow_primary(tok: Token) -> bool:
        return tok.type in ("NUM", "LPAREN")

    with_imp: List[Token] = []
    for idx, tok in enumerate(tokens):
        with_imp.append(tok)
        if idx + 1 < len(tokens):
            a = tok
            b = tokens[idx + 1]
            if is_primary(a) and can_follow_primary(b):
                with_imp.append(Token("OP", "*", a.pos))
    return with_imp

@dataclass
class Node:
    kind: str                 #'BinOp', 'UnaryOp', 'Number', 'Group'
    value: Optional[str]      #Operator or number as string
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    child: Optional['Node'] = None 

#This function creates a number node
def number_node(lex: str) -> Node:
    return Node("Number", lex)

#This function creates a binary operation node
def bin_node(op: str, left: Node, right: Node) -> Node:
    return Node("BinOp", op, left=left, right=right)

#This function creates a unary operation node
def unary_node(op: str, child: Node) -> Node:
    return Node("UnaryOp", op, child=child)

#This function creates a grouping node
def group_node(child: Node) -> Node:
    return Node("Group", None, child=child)

#This class implements a recursive descent parser for mathematical expressions
class Parser:
    def __init__(self, tokens: List[Token]):
        self.toks = tokens
        self.i = 0

    def peek(self) -> Optional[Token]:
        return self.toks[self.i] if self.i < len(self.toks) else None

    def eat(self, typ: Optional[str] = None, val: Optional[str] = None) -> Token:
        tok = self.peek()
        if tok is None:
            raise SyntaxError("Expresión inmcompleta.")
        if typ is not None and tok.type != typ:
            raise SyntaxError(f"Se esperaba {typ} en la posición {tok.pos}")
        if val is not None and tok.value != val:
            raise SyntaxError(f"Se esperaba '{val}' en la posición {tok.pos}")
        self.i += 1
        return tok

    def parse(self) -> Node:
        node = self.expr()
        if self.peek() is not None:
            tok = self.peek()
            raise SyntaxError(f"Símbolos extra después de la expresión en la posición {tok.pos}")
        return node

    def expr(self) -> Node:
        node = self.term()
        while True:
            tok = self.peek()
            if tok and tok.type == "OP" and tok.value in "+-":
                op = self.eat("OP").value
                right = self.term()
                node = bin_node(op, node, right)
            else:
                break
        return node

    def term(self) -> Node:
        node = self.power()
        while True:
            tok = self.peek()
            if tok and tok.type == "OP" and tok.value in "*/":
                op = self.eat("OP").value
                right = self.power()
                node = bin_node(op, node, right)
            else:
                break
        return node

    def power(self) -> Node:
        left = self.unary()
        tok = self.peek()
        if tok and tok.type == "OP" and tok.value == "^":
            self.eat("OP", "^")
            right = self.power()
            return bin_node("^", left, right)
        return left

    def unary(self) -> Node:
        tok = self.peek()
        if tok and tok.type == "OP" and tok.value in "+-":
            op = self.eat("OP").value
            return unary_node(op, self.unary())
        return self.primary()

    def primary(self) -> Node:
        tok = self.peek()
        if tok is None:
            raise SyntaxError("Expresión incompleta.")
        if tok.type == "NUM":
            self.eat("NUM")
            return number_node(tok.value)
        if tok.type == "LPAREN":
            self.eat("LPAREN")
            inner = self.expr()
            self.eat("RPAREN")
            return group_node(inner)
        raise SyntaxError(f"Token inesperado '{tok.value}' en pos {tok.pos}")


def draw_tree(node: Node, prefix: str = "", is_tail: bool = True) -> List[str]:
    lines = []
    connector = "└── " if is_tail else "├── "
    label = ""
    if node.kind == "Number":
        label = f"[NUM {node.value}]"
    elif node.kind == "BinOp":
        label = f"(op '{node.value}')"
    elif node.kind == "UnaryOp":
        label = f"(unary '{node.value}')"
    elif node.kind == "Group":
        label = "( )"
    else:
        label = node.kind

    lines.append(prefix + connector + label)

    children: List[Node] = []
    if node.kind == "BinOp":
        children = [node.left, node.right]
    elif node.kind in ("UnaryOp", "Group"):
        children = [node.child]

    for idx, ch in enumerate(children):
        if ch is None:
            continue
        tail = (idx == len(children) - 1)
        new_prefix = prefix + ("    " if is_tail else "│   ")
        lines.extend(draw_tree(ch, new_prefix, tail))
    return lines

def print_tree(node: Node):
    for line in draw_tree(node, "", True):
        print(line)

def main():
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
    else:
        expr = input("Ingrese una expresión: ") #(2+3)+((4*2)^2)*(7/2(8+2))-1

    try:
        toks = tokenize(expr)
        parser = Parser(toks)
        tree = parser.parse()
        print(f"\nExpresión: {expr}")
        print("\nÁrbol de Parseo:")
        print_tree(tree)
    except SyntaxError as e:
        print(f"Error de sintaxis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()