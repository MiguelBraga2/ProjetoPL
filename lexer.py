import ply.lex as lex

# Lista de tokens
tokens = (
    'TAG',
    'TEXT',
    'INDENT',
    'DEDENT',
    'NEWLINE'
)

states = [
    ('insideTag', 'exclusive')
]

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Token para identação
def t_ANY_INDENT(t):
    r'\n[ \t]*'
    t.lexer.lineno += 1
    spaces = len(t.value) - 1
    indents = getattr(t.lexer, 'indents', [])
    indents.append(spaces)
    t.lexer.indents = indents
    t.lexer.begin('INITIAL')
    if len(indents) == 1:
        return t
    if spaces > indents[-2]:
        t.type = 'INDENT'
        return t
    

# Token para dedentação
def t_ANY_DEDENT(t):
    r'\n[ \t]*'
    t.lexer.lineno += 1
    spaces = len(t.value) - 1
    indents = getattr(t.lexer, 'indents', [])
    if spaces == indents[-1]:
        return t
    while len(indents) > 1 and spaces < indents[-2]:
        indents.pop()
        t.type = 'DEDENT'
        return t
    t.type = 'DEDENT'
    return t

def t_INITIAL_TAG(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.lexer.begin('insideTag')
    return t

# Token para texto
def t_insideTag_TEXT(t):
    r'[^\n]+'
    t.lexer.begin('INITIAL')
    return t

t_ignore = ' '

# Lidar com erros de token
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Criar o analisador léxico
lexer = lex.lex()

lexer.input('''
ul
''')

for tok in lexer:
    print(tok)