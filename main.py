from lexer import Lexer
from my_parser import Parser
from codegen import CodeGen

fname = "input.toy"
with open(fname) as f:
    text_input = f.read()

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf

pg = Parser(module, builder, printf)
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()

codegen.create_ir()
codegen.save_ir("output.ll")

import os

# Generar el archivo de objeto con llc
os.system('llc -filetype=obj output.ll -o output.obj')

# Compilar el archivo de objeto con Clang
os.system('clang output.obj -o output.exe')

# Ejecutar el ejecutable generado
os.system('./output.exe')
