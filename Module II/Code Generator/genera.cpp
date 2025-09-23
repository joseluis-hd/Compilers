#include "genera.hpp"

using std::cout;
using std::endl;

GeneraCodigo::GeneraCodigo(const char* unNombreFichero) : nombreFichero(unNombreFichero), salida(nullptr)
    {
        salida = std::fopen(unNombreFichero, "w");
        if (!salida)
            {
                cout << "No se puede crear el fichero" << unNombreFichero << endl;
        std::exit(-3);
    }
}

GeneraCodigo::~GeneraCodigo()
{
    if (salida) std::fclose(salida);
}

void GeneraCodigo::code()
{
    cout << ".CODE" << endl;
    std::fputs(".CODE\n", salida);
}

void GeneraCodigo::pushc(char constante)
{
    cout << "PUSHC " << constante << endl;
    std::fputs("PUSHC ", salida);
    std::fputc(constante, salida);
    std::fputc('\n', salida);
}

void GeneraCodigo::push(char direccion)
{
    cout << "PUSHA " << direccion << endl;
    std::fputs("PUSHA ", salida);
    std::fputc(direccion, salida);
    std::fputc('\n', salida);
}

void GeneraCodigo::load()
{
    cout << "LOAD" << endl;
    std::fputs("LOAD\n", salida);
}

void GeneraCodigo::store()
{
    cout << "STORE" << endl;
    std::fputs("STORE\n", salida);
}

void GeneraCodigo::neg()
{
    cout << "NEG" << endl;
    std::fputs("NEG\n", salida);
}

void GeneraCodigo::add()
{
    cout << "ADD" << endl;
    std::fputs("ADD\n", salida);
}

void GeneraCodigo::mul()
{
    cout << "MUL" << endl;
    std::fputs("MUL\n", salida);
}

void GeneraCodigo::div()
{
    cout << "DIV" << endl;
    std::fputs("DIV\n", salida);
}

void GeneraCodigo::mod()
{
    cout << "MOD" << endl;
    std::fputs("MOD\n", salida);
}

void GeneraCodigo::input(char direccion)
{
    cout << "INPUT " << direccion << endl;
    std::fputs("INPUT ", salida);
    std::fputc(direccion, salida);
    std::fputc('\n', salida);
}

void GeneraCodigo::output(char direccion)
{
    cout << "OUTPUT " << direccion << endl;
    std::fputs("OUTPUT ", salida);
    std::fputc(direccion, salida);
    std::fputc('\n', salida);
}

void GeneraCodigo::end()
{
    cout << "END" << endl;
    std::fputs("END\n", salida);
}