#include "sintactico.hpp"
using std::cout;
using std::endl;

Sintactico::Sintactico(char* fuente, char* objeto, int traza)
    : lexico(fuente, traza), generaCodigo(objeto) {
    if (lexico.existeTraza())
        cout << "INICIO DE ANALISIS SINTACTICO" << endl;
    programa();
}

/********************************************************************/
Sintactico::~Sintactico(void) {
    if (lexico.existeTraza()) {
        cout << "FIN DE ANALISIS SINTACTICO" << endl;
        cout << "FIN DE COMPILACION" << endl;
    }
}

/********************************************************************/
void Sintactico::programa(void) {
    char token;
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <PROGRAMA>" << endl;

    token = lexico.siguienteToken();
    if (token == 'M') generaCodigo.code();
    else errores(8);

    token = lexico.siguienteToken();
    if (token != '{') errores(9);

    bloque();

    token = lexico.siguienteToken();
    if (token == '}') {
        generaCodigo.end();
    } else errores(2);
}

/************************************************************************/
void Sintactico::bloque(void) {
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <BLOQUE>" << endl;
    sentencia();
    otra_sentencia();
}

/***************************************************************************/
void Sintactico::otra_sentencia(void) {
    char token;
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <OTRA_SENTENCIA>" << endl;

    token = lexico.siguienteToken();
    if (token == ';') {
        sentencia();
        otra_sentencia();
    } else {
        lexico.devuelveToken(token); // <vacio>
    }
}

/***************************************************************************/
void Sintactico::sentencia(void) {
    char token;
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <SENTENCIA>" << endl;

    token = lexico.siguienteToken();
    if ((token >= 'a') && (token <= 'z')) {
        lexico.devuelveToken(token);
        asignacion();
    } else if (token == 'R') {
        lectura();
    } else if (token == 'W') {
        escritura();
    } else {
        errores(6);
    }
}

/***************************************************************************/
void Sintactico::asignacion() {
    char token;
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <ASIGNACION>" << endl;

    variable();

    token = lexico.siguienteToken();
    if (token != '=') errores(3);

    expresion();
    generaCodigo.store();
}

/***************************************************************************/
void Sintactico::variable(void) {
    char token;
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <VARIABLE>" << endl;

    token = lexico.siguienteToken();
    if ((token >= 'a') && (token <= 'z')) {
        generaCodigo.push(token);
    } else errores(5);
}

/**************************************************************************/
void Sintactico::expresion(void) {
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <EXPRESION>" << endl;
    termino();
    mas_terminos();
}

/***************************************************************************/
void Sintactico::termino(void) {
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <TERMINO>" << endl;
    factor();
    mas_factores();
}

/**************************************************************************/
void Sintactico::mas_terminos(void) {
    char token;
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <MAS_TERMINOS>" << endl;

    token = lexico.siguienteToken();
    if (token == '+') {
        termino();
        generaCodigo.add();
        mas_terminos();
    } else if (token == '-') {
        termino();
        // Implementación de resta como NEG + ADD
        generaCodigo.neg();
        generaCodigo.add();
        mas_terminos();
    } else {
        lexico.devuelveToken(token); // <vacio>
    }
}

/*********************************************************************/
void Sintactico::factor(void) {
    char token;
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <FACTOR>" << endl;

    token = lexico.siguienteToken();
    if ((token >= '0') && (token <= '9')) {
        lexico.devuelveToken(token);
        constante();
    } else if (token == '(') {
        expresion();
        token = lexico.siguienteToken();
        if (token != ')') errores(4);
    } else {
        lexico.devuelveToken(token);
        variable();
        generaCodigo.load();
    }
}

/*********************************************************************/
void Sintactico::mas_factores(void) {
    char token;
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <MAS_FACTORES>" << endl;

    token = lexico.siguienteToken();
    switch (token) {
        case '*':
            factor();
            generaCodigo.mul();
            mas_factores();
            break;
        case '/':
            factor();
            generaCodigo.div();
            mas_factores();
            break;
        case '%':
            factor();
            generaCodigo.mod();
            mas_factores();
            break;
        default:
            lexico.devuelveToken(token);
            break;
    }
}

/*********************************************************************/
void Sintactico::lectura(void) {
    char token = lexico.siguienteToken();
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <LECTURA> " << token << endl;

    if ((token < 'a') || (token > 'z')) errores(5);
    generaCodigo.input(token);
}

/**********************************************************************/
void Sintactico::escritura(void) {
    char token = lexico.siguienteToken();
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <ESCRITURA> " << token << endl;

    if ((token < 'a') || (token > 'z')) errores(5);
    generaCodigo.output(token);
}

/**********************************************************************/
void Sintactico::constante(void) {
    char token;
    if (lexico.existeTraza())
        cout << "ANALISIS SINTACTICO: <CONSTANTE>" << endl;

    token = lexico.siguienteToken();
    if ((token >= '0') && (token <= '9')) {
        generaCodigo.pushc(token);
    } else errores(7);
}

/***************************************************************************/
void Sintactico::errores(int codigo) {
    cout << "LINEA " << lexico.lineaActual();
    cout << " ERROR SINTACTICO " << codigo;
    switch (codigo) {
        case 1: cout << " :ESPERABA UN ;" << endl; break;
        case 2: cout << " :ESPERABA UNA }" << endl; break;
        case 3: cout << " :ESPERABA UN =" << endl; break;
        case 4: cout << " :ESPERABA UN )" << endl; break;
        case 5: cout << " :ESPERABA UN IDENTIFICADOR" << endl; break;
        case 6: cout << " :INSTRUCCION DESCONOCIDA" << endl; break;
        case 7: cout << " :ESPERABA UNA CONSTANTE" << endl; break;
        case 8: cout << " :ESPERABA UNA M DE MAIN" << endl; break;
        case 9: cout << " :ESPERABA UNA {" << endl; break;
        default:
            cout << " :NO DOCUMENTADO" << endl; break;
    }
    std::exit(-(codigo + 100));
}
