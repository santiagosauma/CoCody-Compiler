# PARSER
from rply import ParserGenerator
from ai import Comentar, Traducir
from my_ast import Number, Sum, Sub, Mul, Div, Mod, Pow, Print, Assign, Identifier, If, While, ForLoop, Condition, String, List, ListAccess, ListAssign, LengthFunc, FunctionCall, Expression, Break

class Parser():
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            ['NUMBER', 'STRING', 'ASIGNA', 'SUM', 'SUB', 'MUL', 'DIV', 'MOD', 'POW',
            'OPEN_PAREN', 'CLOSE_PAREN', 'OPEN_BRACKET', 'CLOSE_BRACKET', 'COMMA', 'DOT', 
            'MUESTRA', 'SI', 'ENTONCES', 'FIN_SI', 'MIENTRAS', 'HACER', 'FIN_MIENTRAS',
            'CICLO', 'DESDE', 'HASTA', 'EJECUTAR', 'FIN_CICLO',
            'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE', 'AND', 'SINO', 'LENGTH', 'IDENTIFICADOR',
            'TRADUCIR', 'DE', 'A', 'EN', 'COMENTA', 'ROMPER']  # Añadir ROMPER aquí
        )
        self.module = module
        self.builder = builder
        self.printf = printf

    def parse(self):
        @self.pg.production('program : INSTRUCCION_LIST')
        def program(p):
            return p[0]

        @self.pg.production('INSTRUCCION_LIST : INSTRUCCION INSTRUCCION_LIST')
        @self.pg.production('INSTRUCCION_LIST : INSTRUCCION')
        def instruccion_list(p):
            if len(p) == 2:
                return [p[0]] + p[1]
            return [p[0]]

        @self.pg.production('INSTRUCCION : ASIGNA_INSTRUCCION')
        @self.pg.production('INSTRUCCION : MUESTRA_INSTRUCCION')
        @self.pg.production('INSTRUCCION : SI_INSTRUCCION')
        @self.pg.production('INSTRUCCION : MIENTRAS_INSTRUCCION')
        @self.pg.production('INSTRUCCION : CICLO_INSTRUCCION')
        @self.pg.production('INSTRUCCION : LIST_ASSIGN_INSTRUCCION')
        @self.pg.production('INSTRUCCION : TRADUCIR_INSTRUCCION')
        @self.pg.production('INSTRUCCION : COMENTA_INSTRUCCION')
        @self.pg.production('INSTRUCCION : ROMPER_INSTRUCCION')  # Añadir esta línea
        def instruccion(p):
            return p[0]

        @self.pg.production('CICLO_INSTRUCCION : CICLO IDENTIFICADOR DESDE EXPRESION HASTA EXPRESION EJECUTAR INSTRUCCION_LIST FIN_CICLO')
        def ciclo_instruccion(p):
            return ForLoop(self.builder, self.module, self.printf, p[1].getstr(), p[3], p[5], p[7])

        @self.pg.production('ASIGNA_INSTRUCCION : IDENTIFICADOR ASIGNA EXPRESION DOT')
        def asigna_instruccion(p):
            return Assign(self.builder, self.module, p[0].getstr(), p[2])

        @self.pg.production('MUESTRA_INSTRUCCION : MUESTRA OPEN_PAREN EXPRESION CLOSE_PAREN DOT')
        def muestra_instruccion(p):
            return Print(self.builder, self.module, self.printf, p[2])

        @self.pg.production('SI_INSTRUCCION : SI OPEN_PAREN CONDICION CLOSE_PAREN ENTONCES INSTRUCCION_LIST FIN_SI')
        @self.pg.production('SI_INSTRUCCION : SI OPEN_PAREN CONDICION CLOSE_PAREN ENTONCES INSTRUCCION_LIST SINO INSTRUCCION_LIST FIN_SI')
        def si_instruccion(p):
            condition = p[2]
            then_body = p[5]
            if len(p) == 9:
                else_body = p[7]
                return If(self.builder, self.module, self.printf, condition, then_body, else_body)
            return If(self.builder, self.module, self.printf, condition, then_body)

        @self.pg.production('MIENTRAS_INSTRUCCION : MIENTRAS OPEN_PAREN CONDICION CLOSE_PAREN HACER INSTRUCCION_LIST FIN_MIENTRAS')
        def mientras_instruccion(p):
            return While(self.builder, self.module, self.printf, p[2], p[5])

        @self.pg.production('TRADUCIR_INSTRUCCION : TRADUCIR DE STRING A STRING EN STRING DOT')
        def traducir_cody(p):
            nombre_archivo = f"""{p[4].getstr().strip('"')}.{p[6].getstr()}"""
            return Traducir(p[2].getstr(), nombre_archivo, p[6].getstr())

        @self.pg.production('COMENTA_INSTRUCCION : COMENTA STRING DOT')
        def comentar_cody(p):
            nombre_archivo = f"""{p[1].getstr().strip('"')}_commented.cody"""
            return Comentar(p[1].getstr(), nombre_archivo)

        @self.pg.production('ROMPER_INSTRUCCION : ROMPER DOT')
        def romper_instruccion(p):
            return Break(self.builder)

        @self.pg.production('EXPRESION : EXPRESION SUM TERMINO')
        @self.pg.production('EXPRESION : EXPRESION SUB TERMINO')
        @self.pg.production('EXPRESION : EXPRESION MOD TERMINO')
        @self.pg.production('EXPRESION : EXPRESION POW TERMINO')
        @self.pg.production('EXPRESION : EXPRESION MUL TERMINO')
        @self.pg.production('EXPRESION : EXPRESION DIV TERMINO')
        def expresion(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            return Expression(self.builder, self.module, left, operator.gettokentype(), right)

        @self.pg.production('EXPRESION : TERMINO')
        def expresion_termino(p):
            return p[0]

        @self.pg.production('TERMINO : FACTOR')
        def termino_factor(p):
            return p[0]

        @self.pg.production('FACTOR : OPEN_PAREN EXPRESION CLOSE_PAREN')
        def factor_expr(p):
            return p[1]

        @self.pg.production('FACTOR : NUMBER')
        def factor_num(p):
            return Number(self.builder, self.module, p[0].value)

        @self.pg.production('FACTOR : IDENTIFICADOR')
        def factor_identificador(p):
            return Identifier(self.builder, self.module, p[0].getstr())

        @self.pg.production('FACTOR : STRING')
        def factor_string(p):
            return String(self.builder, self.module, p[0].getstr())

        @self.pg.production('FACTOR : LIST')
        def factor_list(p):
            return p[0]

        @self.pg.production('FACTOR : IDENTIFICADOR OPEN_BRACKET EXPRESION CLOSE_BRACKET')
        def factor_list_access(p):
            return ListAccess(self.builder, self.module, p[0].getstr(), p[2])

        @self.pg.production('FACTOR : FUNCTION_CALL')
        def factor_function_call(p):
            return p[0]

        @self.pg.production('FUNCTION_CALL : LENGTH OPEN_PAREN IDENTIFICADOR CLOSE_PAREN')
        def function_call(p):
            return LengthFunc(self.builder, self.module, p[2].getstr())

        @self.pg.production('LIST : OPEN_BRACKET LIST_ELEMENTS CLOSE_BRACKET')
        def list(p):
            return List(p[1])

        @self.pg.production('LIST_ELEMENTS : EXPRESION COMMA LIST_ELEMENTS')
        @self.pg.production('LIST_ELEMENTS : EXPRESION')
        def list_elements(p):
            if len(p) == 3:
                return [p[0]] + p[2]
            return [p[0]]

        @self.pg.production('LIST_ASSIGN_INSTRUCCION : IDENTIFICADOR OPEN_BRACKET EXPRESION CLOSE_BRACKET ASIGNA EXPRESION DOT')
        def list_assign_instruccion(p):
            return ListAssign(self.builder, self.module, p[0].getstr(), p[2], p[5])

        @self.pg.production('CONDICION : EXPRESION EQ EXPRESION')
        @self.pg.production('CONDICION : EXPRESION NEQ EXPRESION')
        @self.pg.production('CONDICION : EXPRESION GT EXPRESION')
        @self.pg.production('CONDICION : EXPRESION LT EXPRESION')
        @self.pg.production('CONDICION : EXPRESION GTE EXPRESION')
        @self.pg.production('CONDICION : EXPRESION LTE EXPRESION')
        @self.pg.production('CONDICION : CONDICION AND CONDICION')
        def condicion(p):
            if len(p) == 3:
                left = p[0]
                right = p[2]
                return Condition(self.builder, self.module, left, right, p[1].gettokentype())
            else:
                left = p[0]
                right = p[2]
                operator = p[1]
                return Condition(self.builder, self.module, left, right, operator.gettokentype())

        @self.pg.error
        def error_handle(token):
            if token is None:
                raise ValueError("Unexpected end of input")
            raise ValueError(f"Syntax error: Unexpected token {token.gettokentype()} ('{token.getstr()}') at {token.getsourcepos()}")

    def get_parser(self):
        return self.pg.build()
