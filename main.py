import sys

from rply import LexingError
from lexer import Lexer
from my_parser import Parser
from codegen import CodeGen

def debug_ir(module):
    print("Generated LLVM IR:")
    print(str(module))

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo.cody>")
        sys.exit(1)

    archivo_input = sys.argv[1]

    with open(archivo_input, 'r') as f:
        text_input = f.read()
    print("Texto del archivo:\n", text_input)

    lexer = Lexer().get_lexer()
    tokens = []
    try:
        for token in lexer.lex(text_input):
            tokens.append(token)
            print(f'Token: {token.gettokentype()}, Valor: {token.getstr()}, Posición: {token.getsourcepos().lineno}:{token.getsourcepos().colno}')
    except LexingError as e:
        print(f"Error léxico en posición {e.source_pos.idx}, línea {e.source_pos.lineno}, columna {e.source_pos.colno}")
        print(f"Texto problemático: {text_input[e.source_pos.idx:e.source_pos.idx+10]}")
        raise e

    codegen = CodeGen()
    module = codegen.module
    builder = codegen.builder
    printf = codegen.printf

    pg = Parser(module, builder, printf)
    pg.parse()
    parser = pg.get_parser()

    try:
        parsed_program = parser.parse(iter(tokens))
    except ValueError as e:
        print(f"Error during parsing: {e}")
        sys.exit(1)

    context = {}
    for stmt in parsed_program:
        stmt.eval(context)

    codegen.create_ir()
    debug_ir(module)
    codegen.save_ir("output.ll")

    import os

    os.system('llc -filetype=obj output.ll -o output.obj')
    os.system('clang output.obj -o output.exe')
    os.system('output.exe')

if __name__ == '__main__':
    main()
