'''
José Luis Haro Díaz
1. If Analyzer (Python, OOP)
'''

from typing import List, Optional, Tuple

# -----------------------------
# Lexer
# -----------------------------
class Lexico:
    def __init__(self, source: str, trace: int):
        self.source = source
        self.trace = 1 if trace else 0
        self.tokens, self._lines = self._tokenize(source)
        self.pos = 0
        self._current_line = 1
        self._buffer: List[Tuple[str, int]] = []  # (token, line)

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

            # identifiers / reserved ('if'), letters only
            if c.isalpha():
                j = i + 1
                while j < n and s[j].isalpha():
                    j += 1
                push(s[i:j]); i = j; continue

            # numbers (multi-digit)
            if c.isdigit():
                j = i + 1
                while j < n and s[j].isdigit():
                    j += 1
                push(s[i:j]); i = j; continue

            # two-char operator '=='
            if c == '=' and i + 1 < n and s[i + 1] == '=':
                push('=='); i += 2; continue

            # single-char symbols
            if c in '(){}=':
                push(c); i += 1; continue

            # anything else becomes a single token (will be rejected in syntax)
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
            return '\0'  # EOF sentinel

        tok = self.tokens[self.pos]
        self._current_line = self._lines[self.pos]
        self.pos += 1
        if self.trace: print(f"LEXER: token='{tok}' (line {self._current_line})")
        return tok

    def ungetToken(self, token: str):
        self._buffer.append((token, self._current_line))
        if self.trace: print(f"LEXER: unget '{token}' (line {self._current_line})")


# -----------------------------
# Parser (with simple semantics)
# Grammar (target of this activity):
#   IfStmt -> 'if' '(' Ident '==' Number ')' '{' '}'
# Semantic rule: relational operator must be '=='
# -----------------------------
class Parser:
    def __init__(self, src: str, trace: int = 1):
        self.lex = Lexico(src, trace)
        self.trace = self.lex.existsTrace()

    def error(self, code: int, extra: str = ""):
        line = self.lex.currentLine()
        messages = {
            1: "EXPECTED 'if'",
            2: "EXPECTED '('",
            3: "EXPECTED identifier",
            4: "EXPECTED relational operator '=='",
            5: "EXPECTED constant (number)",
            6: "EXPECTED ')'",
            7: "EXPECTED '{'",
            8: "EXPECTED '}'",
            9: "UNKNOWN SYMBOL/ORDER (semantic)",
            10: "EXTRA SYMBOLS AFTER IF STATEMENT",
        }
        msg = messages.get(code, "UNDECLARED ERROR")
        if extra:
            msg += f" | {extra}"
        raise SystemExit(f"LINE {line} SYNTAX/SEMANTIC ERROR: {msg}")

    def parse(self) -> bool:
        if self.trace: print("PARSER: <IF_STMT>")

        # 'if'
        t = self.lex.nextToken()
        if t != 'if':
            self.error(1)

        # '('
        if self.lex.nextToken() != '(':
            self.error(2)

        # identifier (variable)
        ident = self.lex.nextToken()
        if not (ident.isalpha() and ident.islower()):
            self.error(3, f"got '{ident}'")

        # relational operator '=='
        op = self.lex.nextToken()
        if op == '=':
            # semantic: single '=' is NOT allowed
            self.error(4, "found '=' (assignment) instead of '=='")
        if op != '==':
            self.error(4, f"got '{op}'")

        # number
        num = self.lex.nextToken()
        if not num.isdigit():
            self.error(5, f"got '{num}'")

        # ')'
        if self.lex.nextToken() != ')':
            self.error(6)

        # '{'
        if self.lex.nextToken() != '{':
            self.error(7)

        # '}'
        if self.lex.nextToken() != '}':
            self.error(8)

        # ensure no trailing garbage
        tail = self.lex.nextToken()
        if tail not in ('\0',):
            self.error(10, f"got '{tail}'")

        if self.trace: print("PARSER: IF statement is valid")
        return True


# -----------------------------
# Main
# -----------------------------
def main():
    path = input("Source file (.txt) path: ").strip()
    try:
        trace = int(input("Trace (0/1): ").strip())
    except Exception:
        trace = 1

    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()

    p = Parser(src, trace)
    ok = p.parse()
    if ok:
        print("VALID IF")


if __name__ == "__main__":
    main()
