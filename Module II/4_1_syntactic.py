'''
José Luis Haro Díaz
4.1 Syntactic
'''

from typing import List, Optional

# -----------------------------
# Lexer
# -----------------------------
class Lexico:
    def __init__(self, fuente: str, traza: int):
        self.fuente = fuente
        self.traza = 1 if traza else 0
        self.tokens, self._lineas = self.tokenizar(fuente) 
        self.pos = 0
        self._linea_actual = 1
        self._buffer: List[str] = []  #LIFO

    def existeTraza(self) -> int:
        return self.traza

    def lineaActual(self) -> int:
        return self._linea_actual

    def tokenizar(self, fuente: str):
        i = 0
        n = len(fuente)
        tokens: List[str] = []
        lineas: List[int] = [] 
        linea = 1

        def push(tok: str):
            tokens.append(tok)
            lineas.append(linea)

        while i < n:
            c = fuente[i]

            if c == '\n':
                linea += 1
                i += 1
                continue

            if c.isspace():
                i += 1
                continue

            if c.isalpha():
                j = i + 1
                while j < n and fuente[j].isalpha():
                    j += 1
                lex = fuente[i:j]
                push(lex)
                i = j
                continue

            if c.isdigit():
                j = i + 1
                while j < n and fuente[j].isdigit():
                    j += 1
                num = fuente[i:j]
                push(num)
                i = j
                continue

            if c in '{}();=+-*/%':
                push(c)
                i += 1
                continue

            push(c)
            i += 1

        return tokens, lineas

    def siguienteToken(self) -> str:
        if self._buffer:
            tok, lin = self._buffer.pop()
            self._linea_actual = lin
            if self.traza:
                print(f"LEXICO: (buffer) -> '{tok}'")
            return tok

        if self.pos >= len(self.tokens):
            self._linea_actual = self._lineas[-1] if self._lineas else 1
            return '\0'

        tok = self.tokens[self.pos]
        self._linea_actual = self._lineas[self.pos]
        self.pos += 1

        if self.traza:
            print(f"LEXICO: token='{tok}' (linea {self._linea_actual})")
        return tok

    def devuelveToken(self, token: str):
        lin = self._linea_actual
        self._buffer.append((token, lin))
        if self.traza:
            print(f"LEXICO: devuelve '{token}' a buffer (linea {lin})")


# ==========================
# GENERA CODIGO
# ==========================
class GeneraCodigo:
    def __init__(self, archivo_objeto: Optional[str] = None):
        self.path = archivo_objeto
        self._fh = open(self.path, 'w', encoding='utf-8') if self.path else None

    # Helpers de salida
    def _out(self, s: str):
        print(s)
        if self._fh:
            self._fh.write(s + '\n')

    # Instrucciones
    def code(self):
        self._out(".CODE")

    def end(self):
        self._out("END")
        if self._fh:
            self._fh.close()
            self._fh = None

    def pusha(self, token: str):
        # dirección (identificador)
        self._out(f"PUSHA {token}")

    def store(self):
        self._out("STORE")

    def load(self):
        self._out("LOAD")

    def input(self, token: str):
        self._out(f"INPUT {token}")

    def output(self, token: str):
        self._out(f"OUTPUT {token}")

    def pushc(self, token: str):
        # constante numérica (puede ser multi-dígito)
        self._out(f"PUSHC {token}")

    def add(self):
        self._out("ADD")

    def neg(self):
        self._out("NEG")

    def mul(self):
        self._out("MUL")

    def div(self):
        self._out("DIV")

    def mod(self):
        self._out("MOD")


# ==========================
# SYNTACTIC
# ==========================
class Sintactico:
    def __init__(self, fuente: str, objeto: Optional[str], traza: int):
        self.lexico = Lexico(fuente, traza)
        self.generaCodigo = GeneraCodigo(objeto)
        if self.lexico.existeTraza():
            print("INICIO DE ANALISIS SINTACTICO")
        self.programa()

        if self.lexico.existeTraza():
            print("FIN DE ANALISIS SINTACTICO")
            print("FIN DE COMPILACION")

    # ---- utilidades de error ----
    def errores(self, codigo: int):
        print(f"LINEA {self.lexico.lineaActual()} ERROR SINTACTICO {codigo}", end='')
        mensajes = {
            1: " :ESPERABA UN ;",
            2: " :ESPERABA UNA }",
            3: " :ESPERABA UN =",
            4: " :ESPERABA UN )",
            5: " :ESPERABA UN IDENTIFICADOR",
            6: " :INSTRUCCION DESCONOCIDA",
            7: " :ESPERABA UNA CONSTANTE",
            8: " :ESPERABA UNA M DE MAIN",
            9: " :ESPERABA UNA {"
        }
        print(mensajes.get(codigo, " :NO DOCUMENTADO"))
        raise SystemExit(-(codigo + 100))

    # ---- gramática ----
    def programa(self):
        if self.lexico.existeTraza():
            print("ANALISIS SINTACTICO: <PROGRAMA>")
        token = self.lexico.siguienteToken()
        if token != 'M':
            self.errores(8)
        self.generaCodigo.code()

        token = self.lexico.siguienteToken()
        if token != '{':
            self.errores(9)

        self.bloque()

        token = self.lexico.siguienteToken()
        if token == '}':
            self.generaCodigo.end()
        else:
            self.errores(2)

    def bloque(self):
        if self.lexico.existeTraza():
            print("ANALISIS SINTACTICO: <BLOQUE>")
        self.sentencia()
        self.otra_sentencia()

    def otra_sentencia(self):
        token = self.lexico.siguienteToken()
        if token == ';':
            self.sentencia()
            self.otra_sentencia()
        else:
            self.lexico.devuelveToken(token)  # <vacio>

    def sentencia(self):
        if self.lexico.existeTraza():
            print("ANALISIS SINTACTICO: <SENTENCIA>")

        token = self.lexico.siguienteToken()

        if token == '}':
            self.lexico.devuelveToken(token)
            return

        if self._es_identificador(token):
            self.lexico.devuelveToken(token)
            self.asignacion()
            return

        if token == 'R':
            self.lectura()
            return
        if token == 'W':
            self.escritura()
            return

        self.errores(6)

    def asignacion(self):
        if self.lexico.existeTraza():
            print("ANALISIS SINTACTICO: <ASIGNACION>")

        self.variable()  # PUSHA id

        token = self.lexico.siguienteToken()
        if token != '=':
            self.errores(3)

        self.expresion()
        self.generaCodigo.store()

    def variable(self):
        if self.lexico.existeTraza():
            print("ANALISIS SINTACTICO: <VARIABLE>")
        token = self.lexico.siguienteToken()
        if self._es_identificador(token):
            self.generaCodigo.pusha(token)
        else:
            self.errores(5)

    def expresion(self):
        if self.lexico.existeTraza():
            print("ANALISIS SINTACTICO: <EXPRESION>")
        self.termino()
        self.mas_terminos()

    def termino(self):
        if self.lexico.existeTraza():
            print("ANALISIS SINTACTICO: <TERMINO>")
        self.factor()
        self.mas_factores()

    def mas_terminos(self):
        token = self.lexico.siguienteToken()
        if token == '+':
            self.termino()
            self.generaCodigo.add()
            self.mas_terminos()
        elif token == '-':
            self.termino()
            self.generaCodigo.neg()  # a - b = a + (-b)
            self.generaCodigo.add()
            self.mas_terminos()
        else:
            self.lexico.devuelveToken(token)  # <vacio>

    def factor(self):
        if self.lexico.existeTraza():
            print("ANALISIS SINTACTICO: <FACTOR>")
        token = self.lexico.siguienteToken()

        # constante
        if token.isdigit():
            self.lexico.devuelveToken(token)
            self.constante()
            return

        # (expresion)
        if token == '(':
            self.expresion()
            token = self.lexico.siguienteToken()
            if token != ')':
                self.errores(4)
            return

        # variable
        self.lexico.devuelveToken(token)
        self.variable()
        self.generaCodigo.load()

    def mas_factores(self):
        token = self.lexico.siguienteToken()
        if token == '*':
            self.factor()
            self.generaCodigo.mul()
            self.mas_factores()
        elif token == '/':
            self.factor()
            self.generaCodigo.div()
            self.mas_factores()
        elif token == '%':
            self.factor()
            self.generaCodigo.mod()
            self.mas_factores()
        else:
            self.lexico.devuelveToken(token)  # <vacio>

    def lectura(self):
        token = self.lexico.siguienteToken()
        if self.lexico.existeTraza():
            print(f"ANALISIS SINTACTICO: <LECTURA> {token}")
        if not self._es_identificador(token):
            self.errores(5)
        self.generaCodigo.input(token)

    def escritura(self):
        token = self.lexico.siguienteToken()
        if self.lexico.existeTraza():
            print(f"ANALISIS SINTACTICO: <ESCRITURA> {token}")
        if not self._es_identificador(token):
            self.errores(5)
        self.generaCodigo.output(token)

    def constante(self):
        if self.lexico.existeTraza():
            print("ANALISIS SINTACTICO: <CONSTANTE>")
        token = self.lexico.siguienteToken()
        if token.isdigit():
            self.generaCodigo.pushc(token)
        else:
            self.errores(7)

    # ---- helpers ----
    @staticmethod
    def _es_identificador(tok: str) -> bool:
        return len(tok) >= 1 and tok.isalpha() and tok.islower()


# -----------------------------
# Main
# -----------------------------
def main():

    #C:\Users\josel\Documents\GitHub\Compilers\Module II\test\test.txt
    #C:\Users\josel\Documents\GitHub\Compilers\Module II\test\objeto.txt

    archivo_fuente = input("Ruta del archivo fuente (.txt): ").strip()
    archivo_objeto = input("Ruta del archivo objeto a generar (.obj/.txt): ").strip()
    try:
        traza = int(input("Trace (0/1): ").strip())
    except Exception:
        traza = 1

    with open(archivo_fuente, 'r', encoding='utf-8') as f:
        fuente = f.read()

    Sintactico(fuente, archivo_objeto, traza)


if __name__ == "__main__":
    main()
