import ply.lex as lex

# Define the tokens for PugJS
tokens = (
    'TAG',
    'ID',
    'CLASS',
    'TEXT',
    'COMMENT',
    'EQUALS',
    'STRING',
    'INDENT',
    'DEDENT'
)

# Palavras reservadas e simbolos terminais '(' ')' '.' e atributos

# Define regular expressions for each token
t_TAG = r'[a-z][a-z0-9]*'
t_CLASS = r'\.\w+'
t_EQUALS = r'='
t_STRING = r'\'[^\']*\'|"[^"]*"'
t_ignore_COMMENT = r'\/\/-.*'
t_ignore = '\t\r'


# Define a rule for the indentation
def t_indentation(t):
    r'\n[ \t]*'
    t.lexer.lineno += 1
    indent_level = len(t.value) -1
    if t.lexer.indent_stack[-1] == 0 and indent_level != 0:
        t.lexer.indent_stack.append(indent_level)
        t.type = 'INDENT'
        return t
    elif t.lexer.indent_stack[-1] == 0 and indent_level == 0:
        return
    elif t.lexer.indent_stack[-1] == indent_level:
        return 
    elif t.lexer.indent_stack[-1] > indent_level:
        while t.lexer.indent_stack[-1] > indent_level:
            t.lexer.indent_stack.pop()
        t.type = 'DEDENT'
        return t
    else:
        t.lexer.indent_stack.append(indent_level)
        t.type = 'INDENT'
        return t

def t_ID(t):
    r'\#\w+'
    return t

# Define a rule for the TEXT token
def t_TEXT(t):
    r'(?<!\s)s*.+'
    t.value = t.value.strip()
    return t

# Define an error handling function
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Create the lexer
lexer = lex.lex()
lexer.indent_stack = [0]

# Test the lexer
data = '''
ul
  li OLAAAAAAA
  li manos
  li xau
'''

lexer.input(data)

for token in lexer:
    print(token)

