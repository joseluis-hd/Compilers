#include "genera.hpp"

int main()
{
    GeneraCodigo gen("test.txt");

    gen.code();
    gen.pushc('5');    // constante 5
    gen.push('x');     // dirección 'x'
    gen.load();        // LOAD
    gen.add();         // ADD
    gen.output('x');   // OUTPUT x
    gen.end();

    return 0;
}
