from rply import ParserGenerator
from my_ast import Number, Sum, Sub, Mul, Div, Mod, Pow, Print, Assign, Identifier, If, While, Condition, String, FuncDef, FuncCall, Return

class Parser():
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            ['NUMBER', 'MUESTRA', 'OPEN_PAREN', 'CLOSE_PAREN', 'SUM', 'SUB', 'MUL', 'DIV', 'MOD', 'POW',
             'ASIGNA', 'FIN', 'IDENTIFICADOR', 'SI', 'ENTONCES', 'FIN_SI', 'MIENTRAS', 'HACER', 'FIN_MIENTRAS',
             'EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE', 'STRING', 'FUNC', 'RETORNA', 'COMMA']
        )
        self.module = module
        self.builder = builder
        self.printf = printf
        self.local_vars = {}

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
        @self.pg.production('INSTRUCCION : FUNCION_INSTRUCCION')
        @self.pg.production('INSTRUCCION : RETURN_INSTRUCCION')
        def instruccion(p):
            return p[0]

        @self.pg.production('ASIGNA_INSTRUCCION : IDENTIFICADOR ASIGNA EXPRESION FIN')
        def asigna_instruccion(p):
            return Assign(self.builder, self.module, p[0].getstr(), p[2], self.local_vars)

        @self.pg.production('MUESTRA_INSTRUCCION : MUESTRA OPEN_PAREN EXPRESION CLOSE_PAREN FIN')
        def muestra_instruccion(p):
            return Print(self.builder, self.module, self.printf, p[2], self.local_vars)

        @self.pg.production('SI_INSTRUCCION : SI OPEN_PAREN CONDICION CLOSE_PAREN ENTONCES INSTRUCCION_LIST FIN_SI')
        def si_instruccion(p):
            return If(self.builder, self.module, self.printf, p[2], p[5], self.local_vars)

        @self.pg.production('MIENTRAS_INSTRUCCION : MIENTRAS OPEN_PAREN CONDICION CLOSE_PAREN HACER INSTRUCCION_LIST FIN_MIENTRAS')
        def mientras_instruccion(p):
            return While(self.builder, self.module, self.printf, p[2], p[5], self.local_vars)

        @self.pg.production('FUNCION_INSTRUCCION : FUNC IDENTIFICADOR OPEN_PAREN PARAM_LIST CLOSE_PAREN INSTRUCCION_LIST FIN')
        def funcion_instruccion(p):
            return FuncDef(self.builder, self.module, p[1].getstr(), p[3], p[5])

        @self.pg.production('PARAM_LIST : IDENTIFICADOR COMMA PARAM_LIST')
        @self.pg.production('PARAM_LIST : IDENTIFICADOR')
        def param_list(p):
            if len(p) == 3:
                return [p[0].getstr()] + p[2]
            return [p[0].getstr()]

        @self.pg.production('RETURN_INSTRUCCION : RETORNA EXPRESION FIN')
        def return_instruccion(p):
            return Return(self.builder, self.module, p[1], self.local_vars)

        @self.pg.production('EXPRESION : IDENTIFICADOR OPEN_PAREN ARG_LIST CLOSE_PAREN')
        def funcion_llamada(p):
            return FuncCall(self.builder, self.module, p[0].getstr(), p[2], self.local_vars)

        @self.pg.production('ARG_LIST : EXPRESION COMMA ARG_LIST')
        @self.pg.production('ARG_LIST : EXPRESION')
        def arg_list(p):
            if len(p) == 3:
                return [p[0]] + p[2]
            return [p[0]]

        @self.pg.production('EXPRESION : EXPRESION SUM TERMINO')
        @self.pg.production('EXPRESION : EXPRESION SUB TERMINO')
        @self.pg.production('EXPRESION : EXPRESION MOD TERMINO')
        @self.pg.production('EXPRESION : EXPRESION POW TERMINO')
        def expresion(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'SUM':
                return Sum(self.builder, self.module, left, right, self.local_vars)
            elif operator.gettokentype() == 'SUB':
                return Sub(self.builder, self.module, left, right, self.local_vars)
            elif operator.gettokentype() == 'MOD':
                return Mod(self.builder, self.module, left, right, self.local_vars)
            elif operator.gettokentype() == 'POW':
                return Pow(self.builder, self.module, left, right, self.local_vars)

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
                return Mul(self.builder, self.module, left, right, self.local_vars)
            elif operator.gettokentype() == 'DIV':
                return Div(self.builder, self.module, left, right, self.local_vars)

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
            return Identifier(self.builder, self.module, p[0].getstr(), self.local_vars)

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
            return Condition(self.builder, self.module, left, right, operator.gettokentype(), self.local_vars)

        @self.pg.error
        def error_handle(token):
            raise ValueError(f"Error en el token {token.gettokentype()} ({token.getstr()}) en la posición {token.getsourcepos().lineno}:{token.getsourcepos().colno}")

    def get_parser(self):
        return self.pg.build()
