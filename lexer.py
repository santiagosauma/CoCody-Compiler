# LEXER
from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Palabras clave
        self.lexer.add('TRADUCIR', r'TRADUCIR')
        self.lexer.add('DE', r'DE')
        self.lexer.add('A', r'A')
        self.lexer.add('LENGTH', r'length')
        self.lexer.add('MUESTRA', r'muestra')
        self.lexer.add('SI', r'si')
        self.lexer.add('ENTONCES', r'ENTONCES')
        self.lexer.add('EN', r'EN')
        self.lexer.add('FIN_SI', r'FIN_SI')
        self.lexer.add('MIENTRAS', r'mientras')
        self.lexer.add('HACER', r'HACER')
        self.lexer.add('FIN_MIENTRAS', r'FIN_MIENTRAS')
        self.lexer.add('SINO', r'SiNo')
        self.lexer.add('ASIGNA', r'<-')
        self.lexer.add('CICLO', r'ciclo')
        self.lexer.add('DESDE', r'desde')
        self.lexer.add('HASTA', r'hasta')
        self.lexer.add('EJECUTAR', r'ejecutar')
        self.lexer.add('FIN_CICLO', r'fin_ciclo')
        self.lexer.add('COMENTA', r'COMENTA')
        self.lexer.add('ROMPER', r'romper')

        # Símbolos y operadores
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        self.lexer.add('OPEN_BRACKET', r'\[')
        self.lexer.add('CLOSE_BRACKET', r'\]')
        self.lexer.add('COMMA', r',')
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
        self.lexer.add('AND', r'&&')
        self.lexer.add('DOT', r'\.')

        # Tipos de datos
        self.lexer.add('NUMBER', r'\d+')
        self.lexer.add('STRING', r'"[^"]*"')
        self.lexer.add('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*')

        # Comentarios
        self.lexer.ignore(r'#.*')

        # Ignorar espacios en blanco
        self.lexer.ignore(r'\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
