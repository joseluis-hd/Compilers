'''
José Luis Haro Díaz
6. Switch Analyzer
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
            tokens.append(tok)
            lines.append(line)

        while i < n:
            c = s[i]

            # newlines & spaces
            if c == '\n':
                line += 1
                i += 1
                continue
            if c.isspace():
                i += 1
                continue

            # identifiers / reserved words (letters and underscores)
            if c.isalpha() or c == '_':
                j = i + 1
                while j < n and (s[j].isalnum() or s[j] == '_'):
                    j += 1
                lex = s[i:j]
                low = lex.lower()
                if low in ('switch', 'case', 'break'):
                    push(low)         # normalize reserved words
                else:
                    push(lex)         # keep identifier lexeme
                i = j
                continue

            # numbers (multi-digit)
            if c.isdigit():
                j = i + 1
                while j < n and s[j].isdigit():
                    j += 1
                push(s[i:j])
                i = j
                continue

            # symbols
            if c in '(){}:;=':
                push(c)
                i += 1
                continue

            # unknown single char → still tokenized; parser will reject it
            push(c)
            i += 1

        return tokens, lines

    def nextToken(self) -> str:
        if self._buffer:
            tok, lin = self._buffer.pop()
            self._current_line = lin
            if self.trace:
                print(f"LEXER: (buffer) -> '{tok}'")
            return tok

        if self.pos >= len(self.tokens):
            self._current_line = self._lines[-1] if self._lines else 1
            return '\0'  # EOF sentinel

        tok = self.tokens[self.pos]
        self._current_line = self._lines[self.pos]
        self.pos += 1
        if self.trace:
            print(f"LEXER: token='{tok}' (line {self._current_line})")
        return tok

    def ungetToken(self, token: str):
        self._buffer.append((token, self._current_line))
        if self.trace:
            print(f"LEXER: unget '{token}' (line {self._current_line})")


# -----------------------------
# Parser (with simple semantics)
# Target grammar (single or multiple case-clauses):
#   Switch   -> 'switch' '(' Ident ')' '{' CaseList '}'
#   CaseList -> CaseClause (CaseClause)*           ; at least one case
#   CaseClause -> 'case' ':' Instruction 'break' ';'
#   Instruction -> Ident | Ident '=' Number        ; minimal instruction model
#
# Notes:
# - Semantic rule: 'break' must appear before ';' in each case-clause.
# - Ident: letter/underscore followed by letters/digits/underscore.
# - Number: digits only.
# -----------------------------
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

    def error(self, code: int, extra: str = ""):
        line = self.lex.currentLine()
        messages = {
            1: "EXPECTED 'switch'",
            2: "EXPECTED '('",
            3: "EXPECTED identifier",
            4: "EXPECTED ')'",
            5: "EXPECTED '{'",
            6: "EXPECTED 'case'",
            7: "EXPECTED ':'",
            8: "EXPECTED instruction (identifier or 'id = number')",
            9: "EXPECTED 'break'",
            10: "EXPECTED ';'",
            11: "EXPECTED '}'",
            12: "EXTRA SYMBOLS AFTER SWITCH",
        }
        msg = messages.get(code, "UNDECLARED ERROR")
        if extra:
            msg += f" | {extra}"
        raise SystemExit(f"LINE {line} SYNTAX/SEMANTIC ERROR: {msg}")

    # entry
    def parse(self) -> bool:
        if self.trace:
            print("PARSER: <SWITCH>")
        self.switch_stmt()
        # ensure EOF
        tail = self.lex.nextToken()
        if tail != '\0':
            self.error(12, f"got '{tail}'")
        if self.trace:
            print("PARSER: Switch statement is valid")
        print("VALID SWITCH")
        return True

    # Switch -> 'switch' '(' Ident ')' '{' CaseList '}'
    def switch_stmt(self):
        if self.lex.nextToken() != 'switch':
            self.error(1)
        if self.lex.nextToken() != '(':
            self.error(2)

        ident = self.lex.nextToken()
        if not self._is_ident(ident):
            self.error(3, f"got '{ident}'")

        if self.lex.nextToken() != ')':
            self.error(4)
        if self.lex.nextToken() != '{':
            self.error(5)

        self.case_list()

        if self.lex.nextToken() != '}':
            self.error(11)

    # CaseList -> CaseClause (CaseClause)*
    def case_list(self):
        self.case_clause()
        while True:
            t = self.lex.nextToken()
            if t == 'case':
                self.lex.ungetToken(t)
                self.case_clause()
            else:
                self.lex.ungetToken(t)
                break

    # CaseClause -> 'case' ':' Instruction 'break' ';'
    def case_clause(self):
        t = self.lex.nextToken()
        if t != 'case':
            self.error(6, f"got '{t}'")

        if self.lex.nextToken() != ':':
            self.error(7)

        self.instruction()

        if self.lex.nextToken() != 'break':
            self.error(9)
        if self.lex.nextToken() != ';':
            self.error(10)

    # Instruction -> Ident | Ident '=' Number
    def instruction(self):
        left = self.lex.nextToken()
        if not self._is_ident(left):
            self.error(8, f"got '{left}'")

        look = self.lex.nextToken()
        if look == '=':
            num = self.lex.nextToken()
            if not self._is_number(num):
                self.error(8, f"expected number after '=', got '{num}'")
            # instruction parsed as "id = number"
            return
        else:
            # single identifier instruction
            self.lex.ungetToken(look)
            return


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
