'''
José Luis Haro Díaz
7. For Analyzer
'''

from typing import List, Tuple, Optional

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
            tokens.append(tok)
            lines.append(line)

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
                if low in ('for', 'int'):
                    push(low)
                else:
                    push(lex)   # keep exact identifier
                i = j
                continue

            # numbers (multi-digit)
            if c.isdigit():
                j = i + 1
                while j < n and s[j].isdigit():
                    j += 1
                push(s[i:j]); i = j; continue

            # two-char operators: ++, --, <=, >=, ==, !=
            if i + 1 < n:
                pair = s[i:i+2]
                if pair in ('++', '--', '<=', '>=', '==', '!='):
                    push(pair); i += 2; continue

            # single-char operators/symbols
            if c in '();{}=<>:,':
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


# -----------------------------
# Parser (syntax + simple semantics)
#
# Accepted patterns (as per assignment notes):
#   A) for ( cond1 ; cond2 ; cond3 ) { ... }          (standard order)
#   B) for ( cond3 ; cond2 ; cond1 ) { ... }          (reversed order)
#   C) ( cond1 ; cond2 ; cond3 ) for { ... }          (parens-first then 'for')
#
# Where:
#   cond1 := [ 'int' ] Ident '=' Number
#   cond2 := Ident RelOp Number         (RelOp in <, <=, >, >=, ==, !=)
#   cond3 := Ident ('++' | '--')
#
# Block { ... } may be empty; we only verify '{' ... '}' enclosure.
# -----------------------------
class Parser:
    def __init__(self, src: str, trace: int = 1):
        self.lex = Lexico(src, trace)
        self.trace = self.lex.existsTrace()

    # Utilities
    @staticmethod
    def _is_ident(x: str) -> bool:
        return len(x) > 0 and (x[0].isalpha() or x[0] == '_') and all(ch.isalnum() or ch == '_' for ch in x)
    @staticmethod
    def _is_number(x: str) -> bool:
        return len(x) > 0 and x.isdigit()
    @staticmethod
    def _is_relop(x: str) -> bool:
        return x in ('<','<=','>','>=','==','!=')

    def error(self, code: int, extra: str = ""):
        line = self.lex.currentLine()
        messages = {
            1: "EXPECTED 'for'",
            2: "EXPECTED '('",
            3: "EXPECTED ')'",
            4: "EXPECTED '{'",
            5: "EXPECTED '}'",
            6: "EXPECTED condition",
            7: "EXPECTED ';' between conditions",
            8: "EXPECTED identifier",
            9: "EXPECTED number",
            10:"EXPECTED '=' in init condition",
            11:"EXPECTED '++' or '--' in step condition",
            12:"UNSUPPORTED ORDER OF CONDITIONS",
            13:"EXTRA SYMBOLS AFTER FOR",
        }
        msg = messages.get(code, "UNDECLARED ERROR")
        if extra:
            msg += f" | {extra}"
        raise SystemExit(f"LINE {line} SYNTAX/SEMANTIC ERROR: {msg}")

    # Entry
    def parse(self) -> bool:
        if self.trace:
            print("PARSER: <FOR>")
        # Try pattern A/B starting with 'for', else try pattern C starting with '('
        t = self.lex.nextToken()
        if t == 'for':
            self._parse_for_paren_block(allow_reverse=True)
        elif t == '(':
            # pattern C: (c1;c2;c3) for { }
            self.lex.ungetToken(t)
            self._parse_paren_then_for()
        else:
            self.error(1, f"got '{t}'")

        # EOF
        tail = self.lex.nextToken()
        if tail != '\0':
            self.error(13, f"got '{tail}'")

        if self.trace:
            print("PARSER: For statement is valid")
        print("VALID FOR")
        return True

    # Pattern A/B: for ( ... ) { ... }
    def _parse_for_paren_block(self, allow_reverse: bool):
        if self.lex.nextToken() != '(':
            self.error(2)
        kinds = self._parse_three_conditions()
        # kinds is a tuple like ('c1','c2','c3') or ('c3','c2','c1')
        if kinds not in (('c1','c2','c3'), ('c3','c2','c1')) if allow_reverse else kinds != ('c1','c2','c3'):
            self.error(12, f"order={kinds}")
        if self.lex.nextToken() != ')':
            self.error(3)
        if self.lex.nextToken() != '{':
            self.error(4)
        self._skip_block_instructions()
        if self.lex.nextToken() != '}':
            self.error(5)

    # Pattern C: ( c1;c2;c3 ) for { ... }
    def _parse_paren_then_for(self):
        if self.lex.nextToken() != '(':
            self.error(2)
        kinds = self._parse_three_conditions()
        if kinds != ('c1','c2','c3'):
            self.error(12, f"order={kinds} (expected c1;c2;c3)")
        if self.lex.nextToken() != ')':
            self.error(3)
        if self.lex.nextToken() != 'for':
            self.error(1)
        if self.lex.nextToken() != '{':
            self.error(4)
        self._skip_block_instructions()
        if self.lex.nextToken() != '}':
            self.error(5)

    # Parse cond ; cond ; cond   → returns tuple of kinds ('c1','c2','c3' permuted)
    def _parse_three_conditions(self) -> Tuple[str, str, str]:
        k1 = self._parse_condition_kind()
        if self.lex.nextToken() != ';':
            self.error(7)
        k2 = self._parse_condition_kind()
        if self.lex.nextToken() != ';':
            self.error(7)
        k3 = self._parse_condition_kind()
        return (k1, k2, k3)

    # Classify and consume one condition (c1, c2, or c3)
    def _parse_condition_kind(self) -> str:
        if self.trace:
            print("PARSER: <COND>")
        # We need to look ahead to decide which cond it is.
        t1 = self.lex.nextToken()
        if t1 == 'int':
            # Must be: int Ident = Number  → c1
            ident = self.lex.nextToken()
            if not self._is_ident(ident):
                self.error(8, f"got '{ident}' after 'int'")
            eq = self.lex.nextToken()
            if eq != '=':
                self.error(10, f"got '{eq}'")
            num = self.lex.nextToken()
            if not self._is_number(num):
                self.error(9, f"got '{num}'")
            return 'c1'

        # If first token is an identifier, it could be c1 (without 'int'), c2 or c3
        if self._is_ident(t1):
            t2 = self.lex.nextToken()
            if t2 == '=':
                # c1: ident = number
                num = self.lex.nextToken()
                if not self._is_number(num):
                    self.error(9, f"got '{num}'")
                return 'c1'
            if self._is_relop(t2):
                # c2: ident relop number
                num = self.lex.nextToken()
                if not self._is_number(num):
                    self.error(9, f"got '{num}'")
                return 'c2'
            if t2 in ('++', '--'):
                # c3: ident ++  / ident --
                return 'c3'
            # If none matched, push back t2 and t1 then error
            self.lex.ungetToken(t2)
            self.lex.ungetToken(t1)
            self.error(6, "unrecognized condition pattern")

        # Unknown start → error
        self.lex.ungetToken(t1)
        self.error(6, f"got '{t1}'")

    # We don't evaluate block instructions; we just skip until matching '}'
    # but since grammar requires immediate '}', we only allow empty or any tokens until '}' on same nesting.
    def _skip_block_instructions(self):
        if self.trace:
            print("PARSER: <BLOCK_BODY> (skipping until matching '}')")
        # For this assignment, we accept any tokens until the next '}' at same nesting.
        # However, we don't consume '}' here (caller will).
        # If you want to require empty block, just return.
        depth = 0
        while True:
            t = self.lex.nextToken()
            if t == '\0':
                self.error(5, "unexpected EOF looking for '}'")
            if t == '{':
                depth += 1
            elif t == '}':
                if depth == 0:
                    # Put back the '}' for caller to consume
                    self.lex.ungetToken(t)
                    return
                depth -= 1
            # otherwise keep skipping


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

    Parser(src, trace).parse()


if __name__ == "__main__":
    main()
