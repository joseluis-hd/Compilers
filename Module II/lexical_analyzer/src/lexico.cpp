#include "lexico.hpp"
#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cctype>

using std::cout;
using std::endl;

Lexico::Lexico(const char* unNombreFichero, int una_traza)
    : nombreFichero(unNombreFichero), entrada(nullptr), nl(1), traza(una_traza ? 1 : 0), pBuffer(0) {

    entrada = std::fopen(unNombreFichero, "r");
    if (!entrada) {
        cout << "No se puede abrir el fichero " << unNombreFichero << endl;
        std::exit(-2);
    }
}

Lexico::~Lexico(void) {
    if (entrada) std::fclose(entrada);
}

char Lexico::siguienteToken(void) {
    int ic;
    char car;

    while (true) {
        if (pBuffer > 0) {
            car = buffer[--pBuffer];
            ic = static_cast<unsigned char>(car);
        } else {
            ic = std::getc(entrada);
            if (ic == EOF) return static_cast<char>(EOF);
            car = static_cast<char>(ic);
        }

        if (car == '\x0') continue;
        if (car == '\r') continue;
        if (car == '\n') { ++nl; continue; }
        if (car == ' ' || car == '\t') continue;
        break;
    }

    if (traza) cout << "ANALIZADOR LEXICO: Lee el token '" << car << "'" << endl;

    switch (car) {
        case 'M': case 'R': case 'W':
        case '=':
        case '(': case ')':
        case ';':
        case '{': case '}':
        case '.':
        case '+': case '-': case '*': case '/': case '&':
            return car;
        default: break;
    }

    if (std::islower(static_cast<unsigned char>(car))) return car; // ID
    if (std::isdigit(static_cast<unsigned char>(car))) return car; // NUM

    cout << "ERROR LEXICO: TOKEN DESCONOCIDO '" << car
         << "' en línea " << nl << endl;
    std::exit(-4);
    return car; // no se alcanza
}

void Lexico::devuelveToken(char token) {
    if (pBuffer >= TAM_BUFFER) {
        cout << "ERROR: DESBORDAMIENTO DEL BUFFER DEL ANALIZADOR LEXICO" << endl;
        std::exit(-5);
    }
    buffer[pBuffer++] = token;

    if (existeTraza())
        cout << "ANALIZADOR LEXICO: Recibe en buffer el token '"
             << token << "'" << endl;
}
