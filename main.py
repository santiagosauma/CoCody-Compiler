import sys
from lexer import Lexer
from my_parser import Parser
from codegen import CodeGen

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo.cody>")
        sys.exit(1)

    archivo_input = sys.argv[1]

    with open(archivo_input, 'r') as f:
        text_input = f.read()

    lexer = Lexer().get_lexer()
    tokens = list(lexer.lex(text_input))

    # Imprimir los tokens generados para depuración
    for token in tokens:
        print(f"Token: {token.gettokentype()}, Valor: {token.getstr()}, Posición: {token.getsourcepos().lineno}:{token.getsourcepos().colno}")

    codegen = CodeGen()
    module = codegen.module
    builder = codegen.builder
    printf = codegen.printf

    pg = Parser(module, builder, printf)
    pg.parse()
    parser = pg.get_parser()
    parsed_program = parser.parse(iter(tokens))

    for stmt in parsed_program:
        stmt.eval()

    codegen.create_ir()
    codegen.save_ir("output.ll")

    import os

    os.system('llc -filetype=obj output.ll -o output.obj')

    os.system('clang output.obj -o output.exe')

    os.system('output.exe')

if __name__ == '__main__':
    main()
