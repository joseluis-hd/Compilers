#include "genera.hpp"

int main()
{
    GeneraCodigo gen("test.txt");

    ///Cabecera
    gen.code();

    /// Ej. 1: Leer dos variables x, y; calcular r = x + y; y mostrar r.
    gen.input('x');        // INPUT x   (leer a x)
    gen.input('y');        // INPUT y   (leer a y)

    gen.push('x');         // PUSHA x
    gen.load();            // LOAD      (apila valor de x)
    gen.push('y');         // PUSHA y
    gen.load();            // LOAD      (apila valor de y)
    gen.add();             // ADD       (r = x + y en el tope de la pila)
    gen.push('r');         // PUSHA r
    gen.store();           // STORE     (r := tope)

    gen.output('r');       // OUTPUT r  (mostrar r)

    /// Ej.2: z = (a * b) / c      (con valores le�dos)
    gen.input('a');        // INPUT a
    gen.input('b');        // INPUT b
    gen.input('c');        // INPUT c

    gen.push('a');         // PUSHA a
    gen.load();            // LOAD
    gen.push('b');         // PUSHA b
    gen.load();            // LOAD
    gen.mul();             // MUL       (a*b)

    gen.push('c');         // PUSHA c
    gen.load();            // LOAD
    gen.div();             // DIV       ((a*b)/c)

    gen.push('z');         // PUSHA z
    gen.store();           // STORE     (z := (a*b)/c)
    gen.output('z');       // OUTPUT z

    ///Ej. 3: t = (-x) mod y       (usar NEG y MOD)
    gen.push('x');         // PUSHA x
    gen.load();            // LOAD
    gen.neg();             // NEG       (-x)

    gen.push('y');         // PUSHA y
    gen.load();            // LOAD
    gen.mod();             // MOD       ((-x) mod y)

    gen.push('t');         // PUSHA t
    gen.store();           // STORE     (t := (-x) mod y)
    gen.output('t');       // OUTPUT t

    /// Ej. 4: Demostraci�n de PUSHC/STORE/OUTPUT con una constante: k= 5
    gen.pushc('5');        // PUSHC 5
    gen.push('k');         // PUSHA k
    gen.store();           // STORE     (k := 5)
    gen.output('k');       // OUTPUT k

    gen.end();             // END

    return 0;
}