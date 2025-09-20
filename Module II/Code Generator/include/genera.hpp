#ifndef GENERA_HPP
#define GENERA_HPP

#include <iostream>  // cout, endl
#include <cstdlib>   // exit
#include <cstdio>    // FILE, fopen, fputs, fputc

class GeneraCodigo {
    const char* nombreFichero; // Nombre del fichero objeto de salida
    FILE* salida;              // Fichero objeto de salida

public:
    explicit GeneraCodigo(const char* unNombreFichero);
    ~GeneraCodigo();

    // Prohibimos copia/asignación (maneja FILE*)
    GeneraCodigo(const GeneraCodigo&) = delete;
    GeneraCodigo& operator=(const GeneraCodigo&) = delete;

    void code();

    // Notas:
    // - Se usan 'char' como en el enunciado (constante/dirección de 1 char).
    // - Si necesitas números mayores, cambia a 'int' o 'std::string'.
    void pushc(char constante);   // PUSHC <cte>
    void push(char direccion);    // PUSHA <dir>

    void load();                  // LOAD
    void store();                 // STORE
    void neg();                   // NEG
    void add();                   // ADD
    void mul();                   // MUL
    void div();                   // DIV
    void mod();                   // MOD

    void input(char direccion);   // INPUT <dir>
    void output(char direccion);  // OUTPUT <dir>

    void end();                   // END
};


#endif // GENERA_HPP
