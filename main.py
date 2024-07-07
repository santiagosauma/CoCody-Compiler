from lexer import Lexer
from my_parser import Parser
from codegen import CodeGen

fname = "input.toy"
with open(fname) as f:
    text_input = f.read()

lexer = Lexer().get_lexer()

try:
    tokens = list(lexer.lex(text_input))
    for token in tokens:
        print(f"Token: {token.gettokentype()}, Valor: {token.getstr()}, Posición: {token.getsourcepos().lineno}:{token.getsourcepos().colno}")
except Exception as e:
    print(f"Error al procesar el archivo de entrada: {e}")
    print(f"Texto hasta el error: {text_input[:60]}")
    raise

codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf

pg = Parser(module, builder, printf)
pg.parse()
parser = pg.get_parser()
parsed_program = parser.parse(iter(tokens))

for stmt in parsed_program:
    print(f"Evaluando: {stmt}")
    stmt.eval()
    print(f"Evaluado: {stmt}")

codegen.create_ir()
codegen.save_ir("output.ll")

import os

# Generar el archivo de objeto con llc
os.system('llc -filetype=obj output.ll -o output.obj')

# Compilar el archivo de objeto con Clang
os.system('clang output.obj -o output.exe')

# Ejecutar el ejecutable generado
os.system('./output.exe')