class Automata:
    def __init__(self):
        self.estado = 'inicio'
        self.identificador = []
        self.codigo_intermedio = []
        self.identificador_actual = ''
        self.contiene_caracter_prohibido = False
        self.es_primer_caracter = True
        self.caracteres_prohibidos = {"$", "-", "?", "\\", "/", "#", "%"}

    def procesar_caracter(self, caracter):
        if self.estado == 'inicio':
            if caracter.isalpha() or caracter == "_":
                self.identificador_actual += caracter
                self.estado = 'identificador' if caracter.isalpha() else 'posible_identificador'
                self.es_primer_caracter = False
            elif caracter.isdigit() or caracter in self.caracteres_prohibidos:
                self.contiene_caracter_prohibido = True
                self.estado = 'identificador'
                self.es_primer_caracter = False
            else:
                self.estado = 'fin'

        elif self.estado == 'posible_identificador':
            if caracter.isalnum():
                self.identificador_actual += caracter
                self.estado = 'identificador'
            else:
                self.identificador_actual = ''
                self.estado = 'fin'

        elif self.estado == 'identificador':
            if caracter.isalnum() or caracter == "_":
                self.identificador_actual += caracter
            elif caracter in self.caracteres_prohibidos:
                self.contiene_caracter_prohibido = True
            else:
                self.estado = 'fin'
                if not self.contiene_caracter_prohibido and self.identificador_actual != "_":
                    self.identificador.append(self.identificador_actual)
                    self.codigo_intermedio.append('IDENTIFICADOR:' + self.identificador_actual)
                self.identificador_actual = ''
                self.contiene_caracter_prohibido = False
                self.es_primer_caracter = True

        elif self.estado == 'fin':
            if not caracter.isspace():
                self.estado = 'inicio'
                self.procesar_caracter(caracter)

    def procesar_entrada(self, entrada):
        for caracter in entrada:
            if caracter.isalnum() or caracter == "_" or caracter.isspace() or caracter in self.caracteres_prohibidos:
                self.procesar_caracter(caracter)
        if self.estado == 'identificador' and not self.contiene_caracter_prohibido and self.identificador_actual != "_":
            self.identificador.append(self.identificador_actual)
            self.codigo_intermedio.append('IDENTIFICADOR:' + self.identificador_actual)

    def get_identificador(self):
        return self.identificador

    def get_codigo_intermedio(self):
        return self.codigo_intermedio


def main():
    entrada = "var1 var2 var_3 _var4 _ $var5 var/6 var7_ _"
    automata = Automata()
    automata.procesar_entrada(entrada)

    print("Identificadores encontrados:")
    print(automata.get_identificador())

    print("\nCódigo intermedio generado:")
    for line in automata.get_codigo_intermedio():
        print(line)


if __name__ == "__main__":
    main()