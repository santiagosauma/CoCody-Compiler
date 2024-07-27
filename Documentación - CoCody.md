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

## Requisitos

- Python 3.9 o superior
- pip (el gestor de paquetes de Python)
- Anaconda (para la gestión de entornos)
- LLVM (Low-Level Virtual Machine)

## Instalación

1. Para instalar CoCody, se debe clonar el repositorio y ejecutar el siguiente comando:

```bash
git clone https://github.com/santiagosauma/CoCody-Compiler.git
cd CoCody-Compiler
```
2. Se debe instalar LLVM dle siguiente repositorio. 
- Para Windows: clang+llvm-18.1.8-x86_64-pc-windows-msvc.tar.xz
```bash
https://github.com/llvm/llvm-project/releases/tag/llvmorg-18.1.8
```
3. Agregar la carpeta bin de LLVM al PATH del sistema.
   - Ejemplo: C:\Program Files\LLVM\bin
4. Crear un entorno de Anaconda con Python 3.8 y activarlo:
- Se debe estar en Anaconda Prompt para ejecutar los siguientes comandos.
```bash
conda create --name compilador_py python=3.8
``` 
- Desde el prompt de Anaconda se debe mover a la carpeta donde se clonó el repositorio Cody.
```bash
conda activate compilador_py
code .
pip install -r requirements.txt
```
5. Para ejecutar el compilador, se debe correr el siguiente comando:
- Ejemplo de caso IA:
```bash
run_cody.bat Casos\CasosIA\Traduccion.cody
```
- Ejemplo Algoritmos:
```bash
run_cody.bat Casos\Algoritmos\fibonacci.cody
```

## Funciones

### Asignación

Asignar un valor a una variable:
```
variable <- valor FIN
```
Ejemplo:
```
x <- 10 FIN 
```

### Impresión
Imprimir el valor de una variable o una expresión:
```
muestra(valor o expresión) FIN
```
Ejemplo:
```
muestra(x) FIN
```

### Operaciones Aritméticas
Realizar operaciones entre números o variables:
```
resultado <- expresión_aritmética FIN
```

Ejemplos:

```
y <- x + 5 FIN
z <- y * 2 FIN
```

### Condicionales
Estructura if para evaluar una condición:

```
si (condición) ENTONCES
  instrucciones
FIN_SI
```

Ejemplo:
```
si (x == 10) ENTONCES
  muestra(x) FIN
FIN_SI
```
### Ciclo While
Ciclo while para ejecutar instrucciones mientras se cumpla una condición:

```
mientras (condición) HACER
  instrucciones
FIN_MIENTRAS
```

Ejemplo:
```
mientras (x < 10) HACER
  x <- x + 1 FIN
  muestra(x) FIN
FIN_MIENTRAS
```

## Ejemplos de funcionamiento

### Ejemplo 1: Asignación e Impresión
```
x <- 10 FIN
muestra(x) FIN
```

### Ejemplo 2: Operaciones Aritméticas
```
x <- 5 FIN
y <- x + 3 FIN
z <- y * 2 FIN
muestra(z) FIN
```

### Ejemplo 3: Condicional Simple
```
x <- 10 FIN
si (x == 10) ENTONCES
  muestra(x) FIN
FIN_SI
```

### Ejemplo 4: Ciclo While
```
x <- 0 FIN
mientras (x < 5) HACER
  x <- x + 1 FIN
  muestra(x) FIN
FIN_MIENTRAS
```

### Ejemplo 5: Combinación Completa
```
x <- 0 FIN
mientras (x < 10) HACER
  x <- x + 1 FIN
  si (x % 2 == 0) ENTONCES
    muestra(x) FIN
  FIN_SI
FIN_MIENTRAS
muestra("Fin del ciclo") FIN
```