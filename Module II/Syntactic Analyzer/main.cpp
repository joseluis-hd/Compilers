#include "sintactico.hpp"

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "Uso: " << argv[0] << " <fuente.txt> <objeto.txt> [traza]\n";
        return 1;
    }
    int traza = (argc >= 4) ? 1 : 0;
    Sintactico sint(argv[1], argv[2], traza);
    return 0;
}
