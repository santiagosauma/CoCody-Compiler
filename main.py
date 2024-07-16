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

    # Imprimir tokens generados
    for token in tokens:
        print(f'Token: {token.gettokentype()}, Valor: {token.getstr()}, Posición: {token.getsourcepos().lineno}:{token.getsourcepos().colno}')

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

    # Context to store variables
    context = {}

    # Evaluate the parsed program
    for stmt in parsed_program:
        stmt.eval(context)

    # Create IR and save it
    codegen.create_ir()
    codegen.save_ir("output.ll")

    import os

    os.system('llc -filetype=obj output.ll -o output.obj')
    os.system('clang output.obj -o output.exe')
    os.system('output.exe')

if __name__ == '__main__':
    main()
