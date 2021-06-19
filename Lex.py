import ply.lex as lex

# 保留关键字
reserved = {
    # A
    'and': 'AND',
    'as': 'AS',
    'any': 'ANY',

    # B
    'by': 'BY',

    # C
    'char': 'CHAR',
    'check': 'CHECK',
    'create': 'CREATE',
    # 'COMMA':'COMMA','comma':'COMMA',

    # D
    'database': 'DATABASE',
    'databases': 'DATABASES',
    'dec': 'DEC',
    'default': 'DEFAULT',
    'delete': 'DELETE',
    'describe': 'DESCRIBE',
    'distinct': 'DISTINCT',
    'double': 'DOUBLE',
    'drop': 'DROP',
    # 'DIVIDE':'DIVIDE','divide':'DIVIDE',
    # 'DEQUAL':'DEQUAL','dequal':'DEQUAL',

    # E
    'escaped': 'ESCAPED',
    'exists': 'EXISTS',
    'exit': 'EXIT',
    'escape': 'ESCAPE',
    # 'EQUAL':'EQUAL','equal':'EQUAL',

    # F
    'false': 'FALSE',
    'float': 'FLOAT',
    'foreign': 'FOREIGN',
    'from': 'FROM',

    # G
    'grant': 'GRANT',
    'group': 'GROUP',
    # 'GREATEREQUAL':'GREATEREQUAL','greaterequal':'GREATEREQUAL',
    # 'GREATER':'GREATER','greater':'GREATER',

    # H
    'having': 'HAVING',

    # I
    'in': 'IN',
    'insert': 'INSERT',
    'int': 'INT',
    'is': 'IS',
    'into': 'INTO',

    # J
    'join': 'JOIN',

    # K
    'key': 'KEY',

    # L
    'long': 'LONG',
    'like': 'LIKE',
    # 'LESSEQUAL':'LESSEQUAL','lessequal':'LESSEQUAL',
    # 'LESS':'LESS','less':'LESS',

    # M
    'mod': 'MOD',
    # 'MINUS':'MINUS','minus':'MINUS',

    # N
    'not': 'NOT',

    # O
    'on': 'ON',
    'or': 'OR',
    'order': 'ORDER',

    # P
    # 'PLUS':'PLUS','plus':'PLUS',

    # S
    'select': 'SELECT',
    'set': 'SET',
    'show': 'SHOW',
    "STRING": "STRING",
    # 'SEMICOLON':'SEMICOLON', 'semicolon':'SEMICOLON',

    # T
    'table': 'TABLE',
    'to': 'TO',
    'true': 'TRUE',
    # 'TIMES':'TIMES','times':'TIMES',

    # U
    'union': 'UNION',
    'unique': 'UNIQUE',
    'update': 'UPDATE',
    'use': 'USE',

    # V
    'values': 'VALUES',
    'VARCHAR': 'VARCHAR',

    # W
    'where': 'WHERE',

}


tokens = ['ID', 'NUM', 'SEMICOLON','COMMA', 'LPAREN', 'RPAREN',
          # 'PLUS', 'MINUS', 'DIVIDE', 'TIMES',
          'LE', 'GE', 'DE',
          # 'EQ','LT','GT',
          'QUOTE', 'DQUOTE', 'ID_NUM'] \
         + list(reserved.values())

# literals = [ '(', ')', ',', ';', '.', '+', '-', '*', '/' ]
literals = '=()*<>\'",'
# t_PLUS = r'\+'
# t_MINUS = r'-'
# t_TIMES = r'\*'
# t_DIVIDE = r'/'
# t_EQ = r'='
# t_LT = r'<'
# t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_DE = r'!='
t_SEMICOLON = ';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_QUOTE = r'\''
t_DQUOTE = r'"'
t_ID_NUM = r'''['"][0-9][a-zA-Z_0-9]*["']'''

t_ignore = '\t\r '


def t_NextLine(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


def t_NUM(t):
    r'[+-]?\d+(\.\d+)?((E|e)[+-]?\d+)?'
    t.value = float(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    if t.type != 'ID':
        t.value = t.value.lower()
    return t


def t_error(t):
    print('不合法字符: %s' % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

if __name__ == '__main__':
    # lexer.input('use fyf;')

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: break  # No more input
        print(tok)
