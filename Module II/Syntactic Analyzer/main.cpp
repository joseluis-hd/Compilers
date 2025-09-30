#include <iostream>
#include "sintactico.hpp"

int main(int argc, char* argv[]) {
    const char* fuente = (argc >= 2) ? argv[1] : "test.txt";
    const char* objeto = (argc >= 3) ? argv[2] : "objeto.txt";
    int traza = (argc >= 4) ? 1 : 0;

    std::cout << "Fuente: " << fuente << "\nObjeto: " << objeto << "\nTraza: " << traza << "\n";
    Sintactico sint(const_cast<char*>(fuente), const_cast<char*>(objeto), traza);
    return 0;
}
