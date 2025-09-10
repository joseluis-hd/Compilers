#include "lexico.hpp"
#include <iostream>
#include <cctype>  // islower, isdigit

using namespace std;

static const char* categoria(char t) {
    if (t == 'M' || t == 'R' || t == 'W') return "RESERVADA";
    if (t == '=' || t == '(' || t == ')' || t == ';' || t == '{' || t == '}'
        || t == '.') return "SIMBOLO";
    if (t == '+' || t == '-' || t == '*' || t == '/' || t == '&') return "OPERADOR";
    if (islower(static_cast<unsigned char>(t))) return "ID";
    if (isdigit(static_cast<unsigned char>(t))) return "NUM";
    if (t == EOF) return "EOF";
    return "DESCONOCIDO";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Uso: " << argv[0] << " <programa.txt> [traza]" << endl;
        return 1;
    }

    const char* fichero = argv[1];
    int traza = (argc >= 3) ? 1 : 0;

    Lexico lex((char*)fichero, traza);

    cout << "== ANALISIS LEXICO ==" << endl;

    while (true) {
        char token = lex.siguienteToken();
        if (token == EOF) {
            cout << "[EOF]" << endl;
            break;
        }
        cout << "Token: '" << token << "'  "
             << "Tipo: " << categoria(token)
             << "  (linea " << lex.lineaActual() << ")" << endl;

        if (token == '.') {
            cout << "[FIN DE PROGRAMA POR '.']" << endl;
            break;
        }
    }

    return 0;
}
