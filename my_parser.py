from rply import ParserGenerator
from my_ast import Number, Sum, Sub, Mul, Div, Mod, Pow, Print, Assign, Identifier, If, While, ForLoop, Condition, String, List, ListAccess, ListAssign

class Parser():
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            ['NUMBER', 'MUESTRA', 'OPEN_PAREN', 'CLOSE_PAREN', 'SUM', 'SUB', 'MUL', 'DIV', 'MOD', 'POW',
             'ASIGNA', 'DOT', 'FIN', 'IDENTIFICADOR', 'SI', 'ENTONCES', 'FIN_SI', 'MIENTRAS', 'HACER', 'FIN_MIENTRAS',
             'CICLO', 'DESDE', 'HASTA', 'EJECUTAR', 'FIN_CICLO',
             'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE', 'STRING', 'OPEN_BRACKET', 'CLOSE_BRACKET', 'COMMA']
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
                result = [p[0]] + p[1]
            else:
                result = [p[0]]
            print(f'INSTRUCCION_LIST: {result}')  # Debugging output
            return result

        @self.pg.production('INSTRUCCION : ASIGNA_INSTRUCCION')
        @self.pg.production('INSTRUCCION : MUESTRA_INSTRUCCION')
        @self.pg.production('INSTRUCCION : SI_INSTRUCCION')
        @self.pg.production('INSTRUCCION : MIENTRAS_INSTRUCCION')
        @self.pg.production('INSTRUCCION : CICLO_INSTRUCCION')
        @self.pg.production('INSTRUCCION : LIST_ASSIGN_INSTRUCCION')
        def instruccion(p):
            return p[0]

        @self.pg.production('CICLO_INSTRUCCION : CICLO IDENTIFICADOR DESDE EXPRESION HASTA EXPRESION EJECUTAR INSTRUCCION_LIST FIN_CICLO')
        def ciclo_instruccion(p):
            result = ForLoop(self.builder, self.module, self.printf, p[1].getstr(), p[3], p[5], p[7])
            print(f'CICLO_INSTRUCCION: {result.body}')  # Debugging output
            return result

        @self.pg.production('ASIGNA_INSTRUCCION : IDENTIFICADOR ASIGNA EXPRESION DOT')
        def asigna_instruccion(p):
            return Assign(self.builder, self.module, p[0].getstr(), p[2])

        @self.pg.production('MUESTRA_INSTRUCCION : MUESTRA OPEN_PAREN EXPRESION CLOSE_PAREN DOT')
        def muestra_instruccion(p):
            return Print(self.builder, self.module, self.printf, p[2])

        @self.pg.production('SI_INSTRUCCION : SI OPEN_PAREN CONDICION CLOSE_PAREN ENTONCES INSTRUCCION_LIST FIN_SI')
        def si_instruccion(p):
            return If(self.builder, self.module, self.printf, p[2], p[5])

        @self.pg.production('MIENTRAS_INSTRUCCION : MIENTRAS OPEN_PAREN CONDICION CLOSE_PAREN HACER INSTRUCCION_LIST FIN_MIENTRAS')
        def mientras_instruccion(p):
            return While(self.builder, self.module, self.printf, p[2], p[5])

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
            if operator.gettokentype() == 'SUM':
                return Sum(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'SUB':
                return Sub(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'MOD':
                return Mod(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'POW':
                return Pow(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'MUL':
                return Mul(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'DIV':
                return Div(self.builder, self.module, left, right)

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
        def condicion(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            return Condition(self.builder, self.module, left, right, operator.gettokentype())

        @self.pg.error
        def error_handle(token):
            raise ValueError(f"Error en el token {token.gettokentype()} ({token.getstr()}) en la posición {token.getsourcepos().lineno}:{token.getsourcepos().colno}")

    def get_parser(self):
        return self.pg.build()
