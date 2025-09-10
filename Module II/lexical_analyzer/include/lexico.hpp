#ifndef LEXICO_HPP
#define LEXICO_HPP

#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>

#define TAM_BUFFER 100

class Lexico {
    const char* nombreFichero;
    FILE* entrada;
    int nl;
    int traza;
    char buffer[TAM_BUFFER];
    int pBuffer;

public:
    explicit Lexico(const char* NombreFichero, int una_traza = 0);
    ~Lexico();

    Lexico(const Lexico&) = delete;
    Lexico& operator=(const Lexico&) = delete;

    char siguienteToken(void);
    void devuelveToken(char token);
    int lineaActual(void) const { return nl; }
    int existeTraza(void) const { return traza ? 1 : 0; }
};

#endif // LEXICO_HPP
