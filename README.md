# CoCody

CoCody es un lenguaje de programación simple diseñado para enseñar los conceptos básicos de la programación. Está construido con Python y utiliza `rply` para el análisis léxico y sintáctico, y `llvmlite` para la generación de código. 

## Descripción

CoCody permite a los usuarios escribir programas con una sintaxis sencilla y clara. Soporta variables, operadores aritméticos, estructuras condicionales y bucles. También permite la impresión de resultados en la consola.

## Sintaxis, Gramática, Léxico

### Léxico

CoCody reconoce los siguientes tokens:

- `IDENTIFICADOR`: `[a-zA-Z_][a-zA-Z0-9_]*`
- `NUMBER`: `\d+`
- `STRING`: `"[^"]*"`
- `ASIGNA`: `<-`
- `SUM`: `\+`
- `SUB`: `\-`
- `MUL`: `\*`
- `DIV`: `\/`
- `MOD`: `%`
- `EQ`: `==`
- `NEQ`: `!=`
- `GT`: `>`
- `LT`: `<`
- `GTE`: `>=`
- `LTE`: `<=`
- `MUESTRA`: `muestra`
- `SI`: `si`
- `ENTONCES`: `ENTONCES`
- `FIN_SI`: `FIN_SI`
- `MIENTRAS`: `mientras`
- `HACER`: `HACER`
- `FIN_MIENTRAS`: `FIN_MIENTRAS`
- `FIN`: `FIN`
- `OPEN_PAREN`: `\(`
- `CLOSE_PAREN`: `\)`

### Gramática

```yaml
program : INSTRUCCION_LIST

INSTRUCCION_LIST : INSTRUCCION INSTRUCCION_LIST
                 | INSTRUCCION

INSTRUCCION : ASIGNA_INSTRUCCION
            | MUESTRA_INSTRUCCION
            | SI_INSTRUCCION
            | MIENTRAS_INSTRUCCION

ASIGNA_INSTRUCCION : IDENTIFICADOR ASIGNA EXPRESION FIN

MUESTRA_INSTRUCCION : MUESTRA OPEN_PAREN EXPRESION CLOSE_PAREN FIN

SI_INSTRUCCION : SI OPEN_PAREN CONDICION CLOSE_PAREN ENTONCES INSTRUCCION_LIST FIN_SI

MIENTRAS_INSTRUCCION : MIENTRAS OPEN_PAREN CONDICION CLOSE_PAREN HACER INSTRUCCION_LIST FIN_MIENTRAS

EXPRESION : EXPRESION SUM TERMINO
          | EXPRESION SUB TERMINO
          | EXPRESION MOD TERMINO
          | TERMINO

TERMINO : TERMINO MUL FACTOR
        | TERMINO DIV FACTOR
        | FACTOR

FACTOR : OPEN_PAREN EXPRESION CLOSE_PAREN
       | NUMBER
       | IDENTIFICADOR
       | STRING

CONDICION : EXPRESION EQ EXPRESION
          | EXPRESION NEQ EXPRESION
          | EXPRESION GT EXPRESION
          | EXPRESION LT EXPRESION
          | EXPRESION GTE EXPRESION
          | EXPRESION LTE EXPRESION
```