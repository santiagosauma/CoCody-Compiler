# CoCody

CoCody is a simple programming language designed to teach the basics of programming. It’s built with Python and uses `rply` for lexical and syntactic analysis and `llvmlite` for code generation.

## Description

CoCody allows users to write programs with a simple and clear syntax. It supports variables, arithmetic operators, conditional structures, and loops. It also allows printing results to the console.

## Syntax, Grammar, Lexicon

### Lexicon

CoCody recognizes the following tokens:

- `IDENTIFIER`: `[a-zA-Z_][a-zA-Z0-9_]*`
- `NUMBER`: `\d+`
- `STRING`: `"[^"]*"`
- `ASSIGN`: `<-`
- `ADD`: `\+`
- `SUBTRACT`: `\-`
- `MULTIPLY`: `\*`
- `DIVIDE`: `\/`
- `MODULUS`: `%`
- `EQUAL`: `==`
- `NOT_EQUAL`: `!=`
- `GREATER_THAN`: `>`
- `LESS_THAN`: `<`
- `GREATER_OR_EQUAL`: `>=`
- `LESS_OR_EQUAL`: `<=`
- `PRINT`: `print`
- `IF`: `if`
- `THEN`: `THEN`
- `END_IF`: `END_IF`
- `WHILE`: `while`
- `DO`: `DO`
- `END_WHILE`: `END_WHILE`
- `END`: `END`
- `OPEN_PAREN`: `\(`
- `CLOSE_PAREN`: `\)`

### Grammar

```yml
program : INSTRUCTION_LIST

INSTRUCTION_LIST : INSTRUCTION INSTRUCTION_LIST
                 | INSTRUCTION

INSTRUCTION : ASSIGN_INSTRUCTION
            | PRINT_INSTRUCTION
            | IF_INSTRUCTION
            | WHILE_INSTRUCTION

ASSIGN_INSTRUCTION : IDENTIFIER ASSIGN EXPRESSION END

PRINT_INSTRUCTION : PRINT OPEN_PAREN EXPRESSION CLOSE_PAREN END

IF_INSTRUCTION : IF OPEN_PAREN CONDITION CLOSE_PAREN THEN INSTRUCTION_LIST END_IF

WHILE_INSTRUCTION : WHILE OPEN_PAREN CONDITION CLOSE_PAREN DO INSTRUCTION_LIST END_WHILE

EXPRESSION : EXPRESSION ADD TERM
           | EXPRESSION SUBTRACT TERM
           | EXPRESSION MODULUS TERM
           | TERM

TERM : TERM MULTIPLY FACTOR
     | TERM DIVIDE FACTOR
     | FACTOR

FACTOR : OPEN_PAREN EXPRESSION CLOSE_PAREN
       | NUMBER
       | IDENTIFIER
       | STRING

CONDITION : EXPRESSION EQUAL EXPRESSION
          | EXPRESSION NOT_EQUAL EXPRESSION
          | EXPRESSION GREATER_THAN EXPRESSION
          | EXPRESSION LESS_THAN EXPRESSION
          | EXPRESSION GREATER_OR_EQUAL EXPRESSION
          | EXPRESSION LESS_OR_EQUAL EXPRESSION
```

## Requirements

- Python 3.9 or higher
- pip (Python package manager)
- Anaconda (for environment management)
- LLVM (Low-Level Virtual Machine)

## Installation

1. To install CoCody, clone the repository and run the following command:

```bash
git clone https://github.com/santiagosauma/CoCody-Compiler.git
cd CoCody-Compiler
```

2. Install LLVM from the following repository.
   - For Windows: `clang+llvm-18.1.8-x86_64-pc-windows-msvc.tar.xz`

```bash
https://github.com/llvm/llvm-project/releases/tag/llvmorg-18.1.8
```

3. Add LLVM's bin folder to the system PATH.
   - Example: `C:\Program Files\LLVM\bin`

4. Create an Anaconda environment with Python 3.8 and activate it:
   - Open Anaconda Prompt to execute the following commands.

```bash
conda create --name compilador_py python=3.8
conda activate compilador_py
code .
pip install -r requirements.txt
```

5. To execute the compiler, run the following command:
   - AI Example:

```bash
run_cody.bat Cases\AI_Cases\Translation.cody
```

   - Algorithms Example:

```bash
run_cody.bat Cases\Algorithms\fibonacci.cody
```

## Functions

### Assignment

Assign a value to a variable:
```yml
variable <- value END
```
Example:
```yml
x <- 10 END 
```

### Print

Print the value of a variable or expression:
```yml
print(value or expression) END
```
Example:
```yml
print(x) END
```

### Arithmetic Operations

Perform operations between numbers or variables:
```yml
result <- arithmetic_expression END
```
Examples:

```yml
y <- x + 5 END
z <- y * 2 END
```

### Conditionals

If structure to evaluate a condition:
```yml
if (condition) THEN
  instructions
END_IF
```
Example:
```yml
if (x == 10) THEN
  print(x) END
END_IF
```

### While Loop

While loop to execute instructions as long as a condition is met:
```yml
while (condition) DO
  instructions
END_WHILE
```
Example:
```yml
while (x < 10) DO
  x <- x + 1 END
  print(x) END
END_WHILE
```

## Example Programs

### Example 1: Assignment and Print
```yml
x <- 10 END
print(x) END
```

### Example 2: Arithmetic Operations
```yml
x <- 5 END
y <- x + 3 END
z <- y * 2 END
print(z) END
```

### Example 3: Simple Conditional
```yml
x <- 10 END
if (x == 10) THEN
  print(x) END
END_IF
```

### Example 4: While Loop
```yml
x <- 0 END
while (x < 5) DO
  x <- x + 1 END
  print(x) END
END_WHILE
```

### Example 5: Combined Example
```yml
x <- 0 END
while (x < 10) DO
  x <- x + 1 END
  if (x % 2 == 0) THEN
    print(x) END
  END_IF
END_WHILE
print("End of loop") END
```