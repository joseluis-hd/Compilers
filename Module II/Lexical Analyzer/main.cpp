#include "lexico.hpp"
#include <iostream>
#include <string>
#include <cctype>

///Ruta para test: C:\Users\josel\Documents\GitHub\Compilers\Module II\Lexical Analyzer\test.txt

static const char* categoria(char t)
{
    if (t=='M'||t=='R'||t=='W') return "RESERVADA";
    if (t=='='||t=='('||t==')'||t==';'||t=='{'||t=='}'||t=='.') return "SIMBOLO";
    if (t=='+'||t=='-'||t=='*'||t=='/'||t=='&') return "OPERADOR";
    if (std::islower((unsigned char)t)) return "ID";
    if (std::isdigit((unsigned char)t)) return "NUM";
    if (t==EOF) return "EOF";
    return "DESCONOCIDO";
}

int main(int argc, char* argv[])
{
    std::string ruta;
    int traza = 0;

    if (argc < 2)
    {
        std::cout << "Ruta del archivo a analizar: ";
        std::getline(std::cin, ruta);
    } else
    {
        ruta = argv[1];
        if (argc >= 3) traza = 1;
    }

    Lexico lex(ruta.c_str(), traza);

    std::cout << "============== ANALISIS LEXICO ==============\n";
    while (true)
    {
        char token = lex.siguienteToken();
        if (token == EOF)
        {
            std::cout << "[EOF]\n"; break;
        }
        std::cout << "Token: '" << token << "'  "
                  << "Tipo: " << categoria(token)
                  << "  (linea " << lex.lineaActual() << ")\n";
        if (token == '.')
        {
            std::cout << "[FIN DE PROGRAMA POR: '.']\n"; break;
        }
    }
    return 0;
}