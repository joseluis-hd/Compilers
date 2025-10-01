#ifndef SINTACTICO_HPP
#define SINTACTICO_HPP

#include <iostream>
#include <cstdlib>

#include "lexico.hpp"   
#include "genera.hpp"  

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

    // Componentes
    Lexico lexico;
    GeneraCodigo generaCodigo;

public:
    Sintactico(char* fuente, char* objeto, int traza);
    ~Sintactico(void);

    // Evitar copias (maneja FILE*)
    Sintactico(const Sintactico&) = delete;
    Sintactico& operator=(const Sintactico&) = delete;
};

#endif // SINTACTICO_HPP
