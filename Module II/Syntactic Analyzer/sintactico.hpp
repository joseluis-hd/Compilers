#ifndef SINTACTICO_HPP
#define SINTACTICO_HPP

#include <iostream>
#include <cstdlib>

// Cambia estos includes si tus headers se llaman distinto:
#include "lexico.hpp"   // o "lexico.h"
#include "genera.hpp"   // o "code_generator.hpp"

class Sintactico {
    // Reglas de la gramática
    void programa(void);
    void bloque(void);
    void sentencia(void);
    void otra_sentencia(void);
    void asignacion(void);
    void lectura(void);
    void escritura(void);
    void variable(void);
    void expresion(void);
    void termino(void);
    void mas_terminos(void);
    void factor(void);
    void mas_factores(void);
    void constante(void);
    void errores(int codigo);

    // Estados/servicios
    Lexico lexico;
    GeneraCodigo generaCodigo;

public:
    // Crea analizador con archivo fuente (lexico) y archivo objeto (genera)
    Sintactico(char* fuente, char* objeto, int traza);
    ~Sintactico(void);

    // Evitar copias (maneja FILE*)
    Sintactico(const Sintactico&) = delete;
    Sintactico& operator=(const Sintactico&) = delete;
};

#endif // SINTACTICO_HPP
