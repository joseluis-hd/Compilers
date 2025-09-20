#ifndef CODE_GENERATOR_HPP
#define CODE_GENERATOR_HPP

#include <iostream>  //cout, endl
#include <cstdlib>   //exit
#include <cstdio>    //FILE, fopen, fputs, fputc

class GeneraCodigo
{
    const char* nombreFichero;
    FILE* salida;

public:
    explicit GeneraCodigo(const char* unNombreFichero);
    ~GeneraCodigo();

    GeneraCodigo(const GeneraCodigo&) = delete;
    GeneraCodigo& operator=(const GeneraCodigo&) = delete;

    void code();

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

#endif // CODE_GENERATOR_HPP
