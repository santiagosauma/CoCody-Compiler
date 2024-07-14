from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        self.lexer.add('TRADUCIR', r'TRADUCIR')
        self.lexer.add('DE', r'DE')
        self.lexer.add('A', r'A')
        self.lexer.add('MUESTRA', r'muestra')
        self.lexer.add('SI', r'si')
        self.lexer.add('ENTONCES', r'ENTONCES')
        self.lexer.add('EN', r'EN')
        self.lexer.add('FIN_SI', r'FIN_SI')
        self.lexer.add('MIENTRAS', r'mientras')
        self.lexer.add('HACER', r'HACER')
        self.lexer.add('FIN_MIENTRAS', r'FIN_MIENTRAS')
        self.lexer.add('ASIGNA', r'<-')
        self.lexer.add('FIN', r'FIN')
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        self.lexer.add('OPEN_BRACKET', r'\[')
        self.lexer.add('CLOSE_BRACKET', r'\]')
        self.lexer.add('COMMA', r',')  # Token for comma
        self.lexer.add('POW', r'\*\*')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')
        self.lexer.add('MOD', r'%')
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('EQ', r'==')
        self.lexer.add('NEQ', r'!=')
        self.lexer.add('GT', r'>')
        self.lexer.add('LT', r'<')
        self.lexer.add('GTE', r'>=')
        self.lexer.add('LTE', r'<=')
        self.lexer.add('NUMBER', r'\d+')
        self.lexer.add('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*')
        self.lexer.add('STRING', r'"[^"]*"')
        # self.lexer.add('LENGUAJE', r'[a-zA-Z]+')
        self.lexer.ignore(r'\s+')

        self.lexer.ignore('\s+')
        self.lexer.ignore(r'\s+')


    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
