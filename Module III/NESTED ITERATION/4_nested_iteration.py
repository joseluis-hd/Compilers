'''
José Luis Haro Díaz
8. Nested Iteration – while with nested if (Python, OOP)
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

            # identifiers / reserved words
            if c.isalpha() or c == '_':
                j = i + 1
                while j < n and (s[j].isalnum() or s[j] == '_'):
                    j += 1
                lex = s[i:j]
                low = lex.lower()
                if low in ('while', 'if'):
                    push(low)
                else:
                    push(lex)
                i = j
                continue

            # numbers (multi-digit)
            if c.isdigit():
                j = i + 1
                while j < n and s[j].isdigit():
                    j += 1
                push(s[i:j]); i = j; continue

            # two-char operators
            if i + 1 < n:
                pair = s[i:i+2]
                if pair in ('<=', '>=', '==', '!='):
                    push(pair); i += 2; continue

            # single-char operators / symbols
            if c in '(){};<>=:+-*/%':
                push(c); i += 1; continue

            # unknown char → still a token (parser will reject)
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
            1: "EXPECTED 'while'",
            2: "EXPECTED '('",
            3: "EXPECTED ')'",
            4: "EXPECTED '{'",
            5: "EXPECTED '}'",
            6: "EXPECTED identifier",
            7: "EXPECTED relational operator",
            8: "EXPECTED number",
            9: "EXPECTED 'if' inside while block",
            10: "EXTRA SYMBOLS AFTER STRUCTURE",
        }
        msg = messages.get(code, "UNDECLARED ERROR")
        if extra:
            msg += f" | {extra}"
        raise SystemExit(f"LINE {line} SYNTAX/SEMANTIC ERROR: {msg}")

    # ---- entry point ----
    def parse(self) -> bool:
        if self.trace:
            print("PARSER: <WHILE_IF>")
        self.while_stmt()
        # EOF only
        tail = self.lex.nextToken()
        if tail != '\0':
            self.error(10, f"got '{tail}'")
        if self.trace:
            print("PARSER: Structure is valid")
        print("VALID WHILE-IF")
        return True

    # while '(' Cond ')' '{' Inner '}' 
    def while_stmt(self):
        if self.lex.nextToken() != 'while':
            self.error(1)
        if self.lex.nextToken() != '(':
            self.error(2)
        self.cond()
        if self.lex.nextToken() != ')':
            self.error(3)
        if self.lex.nextToken() != '{':
            self.error(4)

        self.inner_if_required()

        if self.lex.nextToken() != '}':
            self.error(5)

    # require exactly one nested if-structure inside while block
    def inner_if_required(self):
        # We accept optional stray tokens before 'if', but the assignment examples
        # imply the if should be present. We'll look ahead until 'if' or '}'.
        depth = 0
        while True:
            t = self.lex.nextToken()
            if t == '\0':
                self.error(5, "unexpected EOF while looking for nested 'if'")
            if t == '{':
                depth += 1
            elif t == '}':
                if depth == 0:
                    # we reached end of while-block without finding 'if'
                    self.lex.ungetToken('}')
                    self.error(9)
                depth -= 1
            elif t == 'if':
                # put it back and parse the if
                self.lex.ungetToken(t)
                self.if_stmt()
                return
            # else: keep scanning tokens until 'if' or '}' at current level

    # if '(' Cond ')' '{' Block '}'
    def if_stmt(self):
        if self.lex.nextToken() != 'if':
            self.error(9)
        if self.lex.nextToken() != '(':
            self.error(2)
        self.cond()
        if self.lex.nextToken() != ')':
            self.error(3)
        if self.lex.nextToken() != '{':
            self.error(4)
        self._skip_block_body()   # don't consume the closing '}'
        if self.lex.nextToken() != '}':
            self.error(5)

    # Cond -> Ident RelOp Number
    def cond(self):
        ident = self.lex.nextToken()
        if not self._is_ident(ident):
            self.error(6, f"got '{ident}'")
        op = self.lex.nextToken()
        if not self._is_relop(op):
            self.error(7, f"got '{op}'")
        num = self.lex.nextToken()
        if not self._is_number(num):
            self.error(8, f"got '{num}'")

    # Skip any tokens until the matching '}' at the same nesting level
    def _skip_block_body(self):
        if self.trace:
            print("PARSER: <BLOCK_BODY> (skipping until matching '}')")
        depth = 0
        while True:
            t = self.lex.nextToken()
            if t == '\0':
                self.error(5, "unexpected EOF looking for '}'")
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
