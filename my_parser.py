from rply import ParserGenerator
from my_ast import Number, Sum, Sub, Mul, Div, Mod, Pow, Print, Assign, Identifier, If, While, For, Condition, String

class Parser():
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            ['NUMBER', 'MUESTRA', 'OPEN_PAREN', 'CLOSE_PAREN', 'SUM', 'SUB', 'MUL', 'DIV', 'MOD', 'POW',
             'ASIGNA', 'FIN', 'IDENTIFICADOR', 'SI', 'ENTONCES', 'FIN_SI', 'MIENTRAS', 'HACER', 'FIN_MIENTRAS',
             'DESDE', 'HASTA', 'INCREMENTO', 'FIN_DESDE', 'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE', 'STRING']
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
        @self.pg.production('INSTRUCCION : DESDE_INSTRUCCION')
        def instruccion(p):
            return p[0]

        @self.pg.production('ASIGNA_INSTRUCCION : IDENTIFICADOR ASIGNA EXPRESION FIN')
        def asigna_instruccion(p):
            return Assign(self.builder, self.module, p[0].getstr(), p[2])

        @self.pg.production('MUESTRA_INSTRUCCION : MUESTRA OPEN_PAREN EXPRESION CLOSE_PAREN FIN')
        def muestra_instruccion(p):
            return Print(self.builder, self.module, self.printf, p[2])

        @self.pg.production('SI_INSTRUCCION : SI OPEN_PAREN CONDICION CLOSE_PAREN ENTONCES INSTRUCCION_LIST FIN_SI')
        def si_instruccion(p):
            return If(self.builder, self.module, self.printf, p[2], p[5])

        @self.pg.production('MIENTRAS_INSTRUCCION : MIENTRAS OPEN_PAREN CONDICION CLOSE_PAREN HACER INSTRUCCION_LIST FIN_MIENTRAS')
        def mientras_instruccion(p):
            return While(self.builder, self.module, self.printf, p[2], p[5])

        @self.pg.production('DESDE_INSTRUCCION : DESDE IDENTIFICADOR ASIGNA EXPRESION HASTA EXPRESION INCREMENTO EXPRESION HACER INSTRUCCION_LIST FIN_DESDE')
        def desde_instruccion(p):
            var_name = p[1].getstr()
            var_start = p[3]
            var_end = p[5]
            var_step = p[7]
            body = p[9]
            return For(self.builder, self.module, self.printf, var_name, var_start, var_end, var_step, body)

        @self.pg.production('EXPRESION : EXPRESION SUM TERMINO')
        @self.pg.production('EXPRESION : EXPRESION SUB TERMINO')
        @self.pg.production('EXPRESION : EXPRESION MOD TERMINO')
        @self.pg.production('EXPRESION : EXPRESION POW TERMINO')
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

        @self.pg.production('EXPRESION : TERMINO')
        def expresion_termino(p):
            return p[0]

        @self.pg.production('TERMINO : TERMINO MUL FACTOR')
        @self.pg.production('TERMINO : TERMINO DIV FACTOR')
        def termino(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'MUL':
                return Mul(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'DIV':
                return Div(self.builder, self.module, left, right)

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
