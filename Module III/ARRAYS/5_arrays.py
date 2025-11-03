'''
José Luis Haro Díaz
5. Arrays – 1D array with for + nested if/switch
'''

from typing import List, Tuple

# =============================
# Lexer
# =============================
class Lexico:
    def __init__(self, source: str, trace: int):
        self.source = source
        self.trace = 1 if trace else 0
        self.tokens, self._lines = self._tokenize(source)
        self.pos = 0
        self._current_line = 1
        self._buffer: List[Tuple[str, int]] = []  

    def existsTrace(self) -> int:
        return self.trace

    def currentLine(self) -> int:
        return self._current_line

    def _tokenize(self, s: str):
        i, n, line = 0, len(s), 1
        tokens: List[str] = []
        lines: List[int] = []

        def push(tok: str):
            tokens.append(tok); lines.append(line)

        while i < n:
            c = s[i]
            if c == '\n':
                line += 1; i += 1; continue
            if c.isspace():
                i += 1; continue
            if c == '/' and i + 1 < n and s[i+1] == '/':
                i += 2
                while i < n and s[i] != '\n':
                    i += 1
                continue

            if c.isalpha() or c == '_':
                j = i + 1
                while j < n and (s[j].isalnum() or s[j] == '_'):
                    j += 1
                lex = s[i:j]
                low = lex.lower()
                if low in ('int', 'for', 'if', 'switch'):
                    push(low)
                else:
                    push(lex)  
                i = j
                continue

            if c.isdigit():
                j = i + 1
                while j < n and s[j].isdigit():
                    j += 1
                push(s[i:j]); i = j; continue

            if i + 1 < n:
                pair = s[i:i+2]
                if pair in ('<=', '>=', '==', '!=', '++', '--'):
                    push(pair); i += 2; continue

            if c in '[](){};=:+-*/%<>,':
                push(c); i += 1; continue

            push(c); i += 1

        return tokens, lines

    def nextToken(self) -> str:
        if self._buffer:
            tok, lin = self._buffer.pop()
            self._current_line = lin
            if self.trace: print(f"LEXER: (buffer) -> '{tok}'")
            return tok

        if self.pos >= len(self.tokens):
            self._current_line = self._lines[-1] if self._lines else 1
            return '\0'

        tok = self.tokens[self.pos]
        self._current_line = self._lines[self.pos]
        self.pos += 1
        if self.trace: print(f"LEXER: token='{tok}' (line {self._current_line})")
        return tok

    def ungetToken(self, token: str):
        self._buffer.append((token, self._current_line))
        if self.trace:
            print(f"LEXER: unget '{token}' (line {self._current_line})")

class Parser:
    def __init__(self, src: str, trace: int = 1):
        self.lex = Lexico(src, trace)
        self.trace = self.lex.existsTrace()
        self.array_name: str | None = None

    @staticmethod
    def _is_ident(x: str) -> bool:
        return len(x) > 0 and (x[0].isalpha() or x[0] == '_') and all(ch.isalnum() or ch == '_' for ch in x)

    @staticmethod
    def _is_number(x: str) -> bool:
        return len(x) > 0 and x.isdigit()

    @staticmethod
    def _is_relop(x: str) -> bool:
        return x in ('<', '<=', '>', '>=', '==', '!=')

    def error(self, code: int, extra: str = ""):
        line = self.lex.currentLine()
        messages = {
            1: "EXPECTED 'int' (array declaration)",
            2: "EXPECTED identifier (array name)",
            3: "EXPECTED '['",
            4: "EXPECTED array size (number)",
            5: "EXPECTED ']'",
            6: "EXPECTED ';' after array declaration",
            7: "EXPECTED 'for'",
            8: "EXPECTED '('",
            9: "EXPECTED 'int' (for loop init)",
            10: "EXPECTED identifier (loop variable)",
            11: "EXPECTED '=' in for init",
            12: "EXPECTED number in for init",
            13: "EXPECTED ';' after for init",
            14: "EXPECTED relational condition in for",
            15: "EXPECTED ';' after for condition",
            16: "EXPECTED '++' in for update",
            17: "EXPECTED ')' after for update",
            18: "EXPECTED '{' to open for block",
            19: "EXPECTED 'if' or 'switch' inside for block",
            20: "EXPECTED '}' to close for block",
            21: "EXTRA SYMBOLS AFTER PROGRAM",
            22: "EXPECTED ')' after condition",
            23: "EXPECTED '{' to open if/switch block",
            24: "EXPECTED '}' to close if/switch block",
            25: "FOR VARIABLES MUST MATCH (init/cond/update)",
            26: "ARRAY MUST BE DECLARED BEFORE 'for'",
        }
        msg = messages.get(code, "UNDECLARED ERROR")
        if extra:
            msg += f" | {extra}"
        raise SystemExit(f"LINE {line} SYNTAX/SEMANTIC ERROR: {msg}")

    def parse(self) -> bool:
        if self.trace:
            print("PARSER: <PROGRAM>")
        self.array_decl()
        self.for_stmt()
        tail = self.lex.nextToken()
        if tail != '\0':
            self.error(21, f"got '{tail}'")
        if self.trace:
            print("PARSER: Program is valid")
        print("VALID ARRAY + FOR (+ nested if/switch)")
        return True

    def array_decl(self):
        if self.lex.nextToken() != 'int':
            self.error(1)
        name = self.lex.nextToken()
        if not self._is_ident(name):
            self.error(2, f"got '{name}'")
        if self.lex.nextToken() != '[':
            self.error(3)
        size = self.lex.nextToken()
        if not self._is_number(size):
            self.error(4, f"got '{size}'")
        if self.lex.nextToken() != ']':
            self.error(5)
        if self.lex.nextToken() != ';':
            self.error(6)
        self.array_name = name
        if self.trace:
            print(f"PARSER: array declared -> {name}[{size}]")

    def for_stmt(self):
        if self.array_name is None:
            self.error(26)
        if self.lex.nextToken() != 'for':
            self.error(7)
        if self.lex.nextToken() != '(':
            self.error(8)

        if self.lex.nextToken() != 'int':
            self.error(9)
        v1 = self.lex.nextToken()
        if not self._is_ident(v1):
            self.error(10, f"got '{v1}'")
        if self.lex.nextToken() != '=':
            self.error(11)
        n0 = self.lex.nextToken()
        if not self._is_number(n0):
            self.error(12, f"got '{n0}'")
        if self.lex.nextToken() != ';':
            self.error(13)

        v2 = self.lex.nextToken()
        if not self._is_ident(v2):
            self.error(10, f"got '{v2}'")
        op = self.lex.nextToken()
        if not self._is_relop(op):
            self.error(14, f"got '{op}'")
        n1 = self.lex.nextToken()
        if not self._is_number(n1):
            self.error(14, f"got '{n1}'")
        if self.lex.nextToken() != ';':
            self.error(15)

        v3 = self.lex.nextToken()
        if not self._is_ident(v3):
            self.error(10, f"got '{v3}'")
        inc = self.lex.nextToken()
        if inc != '++':
            self.error(16, f"got '{inc}'")

        if self.lex.nextToken() != ')':
            self.error(17)

        if not (v1 == v2 == v3):
            self.error(25, f"got '{v1}', '{v2}', '{v3}'")

        if self.lex.nextToken() != '{':
            self.error(18)

        self.inner_stmt_required()

        if self.lex.nextToken() != '}':
            self.error(20)

    def inner_stmt_required(self):
        t = self.lex.nextToken()
        if t == 'if':
            self.lex.ungetToken(t)
            self.if_stmt()
            return
        if t == 'switch':
            self.lex.ungetToken(t)
            self.switch_stmt()
            return
        self.lex.ungetToken(t)
        self.error(19, f"got '{t}'")

    def if_stmt(self):
        if self.lex.nextToken() != 'if':
            self.error(19)
        if self.lex.nextToken() != '(':
            self.error(8)
        self.cond()
        if self.lex.nextToken() != ')':
            self.error(22)
        if self.lex.nextToken() != '{':
            self.error(23)
        self._skip_block_body()
        if self.lex.nextToken() != '}':
            self.error(24)

    def switch_stmt(self):
        if self.lex.nextToken() != 'switch':
            self.error(19)
        if self.lex.nextToken() != '(':
            self.error(8)
        ident = self.lex.nextToken()
        if not self._is_ident(ident):
            self.error(10, f"got '{ident}'")
        if self.lex.nextToken() != ')':
            self.error(22)
        if self.lex.nextToken() != '{':
            self.error(23)
        self._skip_block_body()
        if self.lex.nextToken() != '}':
            self.error(24)

    def cond(self):
        ident = self.lex.nextToken()
        if not self._is_ident(ident):
            self.error(10, f"got '{ident}'")
        op = self.lex.nextToken()
        if not self._is_relop(op):
            self.error(14, f"got '{op}'")
        num = self.lex.nextToken()
        if not self._is_number(num):
            self.error(14, f"got '{num}'")

    def _skip_block_body(self):
        if self.trace:
            print("PARSER: <BLOCK_BODY> (skipping until matching '}')")
        depth = 0
        while True:
            t = self.lex.nextToken()
            if t == '\0':
                self.error(24, "unexpected EOF searching for '}'")
            if t == '{':
                depth += 1
            elif t == '}':
                if depth == 0:
                    self.lex.ungetToken(t)
                    return
                depth -= 1


# =============================
# Main
# =============================
def main():
    path = input("Source file (.txt) path: ").strip()
    try:
        trace = int(input("Trace (0/1): ").strip())
    except Exception:
        trace = 1

    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()

    Parser(src, trace).parse()


if __name__ == "__main__":
    main()
