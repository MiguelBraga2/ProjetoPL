import ply.lex as lex

# Define the tokens for PugJS
tokens = (
    'IF',
    'IN',
    'ID',
    'FOR',
    'TAG',
    'DOT',
    'ELSE',
    'WHEN',
    'DEFAULT',
    'DIGIT',
    'COMMA',
    'PARENL',
    'PARENR',
    'VARIABLE',
    'UNLESS',
    'BAR',
    'CASE',
    'MIXIN',
    'WHILE',
    'EACH',
    'TEXT',
    'CLASS',
    'STRING',
    'INDENT',
    'DEDENT',
    'DOCTYPE',
    'COMMENT',
    'ATTRIBUTE',
    'IGNORECOMMENT',
    'INTERPOLATION',
    'WHITESPACES'
)


states = (
    ('block', 'exclusive'),
    ('ignorecomment', 'exclusive'),
    ('comment', 'exclusive')
)


# Define regular expressions for each token
t_TAG = r'[a-z][a-z0-9]*'
t_STRING = r'\'[^\']*\'|"[^"]*"'
t_ANY_ignore = '\t\r'


# Define a rule for the attributes
def t_ATTRIBUTE(t):
    r'\(\s*\w+\s*=\s*(\'[^\']*\'|"[^"]*")(\s*,?\s*\w+\s*=\s*(\'[^\']*\'|"[^"]*"))*\s*\)'
    t.value = t.value.replace(',','')
    t.value = t.value.replace('\'','"')
    t.value = t.value[1:len(t.value)-1]
    return t

# Define a rule for the indentation
def t_INITIAL_indentation(t):
    r'\n[ \t]*'
    t.lexer.lineno += 1
    indent_level = len(t.value) -1
    if t.lexer.indent_stack[-1] == 0 and indent_level != 0:
        t.lexer.indent_stack.append(indent_level)
        t.type = 'INDENT'
        return t
    elif t.lexer.indent_stack[-1] == indent_level:
        return 
    elif t.lexer.indent_stack[-1] > indent_level:
        t.lexer.indent_stack.pop()
        if t.lexer.indent_stack[-1] > indent_level:
            t.lexer.skip(-indent_level-1)
        t.type = 'DEDENT'
        return t
    else:
        t.lexer.indent_stack.append(indent_level)
        t.type = 'INDENT'
        return t

def t_IGNORECOMMENT(t):
    r'//-.*'
    t.lexer.begin('ignorecomment')

def t_COMMENT(t):
    r'//.*'
    t.lexer.begin('comment')
    return t

def t_INTERPOLATION(t):
    r'\#\{.*\}'
    t.value = t.value[2:len(t.value)-1]
    return t

def t_DOCTYPE(t):
    r'doctype'
    return t

def t_ID(t):
    r'\#\w+'
    t.value = t.value[1:]
    return t

def t_CLASS(t):
    r'\.\w+'
    t.value = t.value[1:]
    return t

def t_DOT(t):
    r'\.'
    t.lexer.begin('block')
    return t

def t_MIXIN(t): 
    r'mixin'
    return t

def t_IF(t):
    r'(if|(?<=(else))\s+if)'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_FOR(t):
    r'for'
    return t

def t_EACH(t):
    r'each'
    return t

def t_IN(t):
    r'in'
    return t

def t_UNLESS(t):
    r'unless'
    return t

def t_WHEN(t):
    r'when'
    return t
    
def t_DEFAULT(t):
    r'default'
    return t

def t_CASE(t):
    r'case'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_BAR(t):
    r'\/'
    return t

# Define a rule for the variable token
def t_VARIABLE(t):
    r'(\=\s+.+|(?<=(if))\s+[^\s]+|(?<=(else))\s+[^\s]+)'
    t.value = t.value[1:]
    t.value = t.value.strip()
    return t

# Define a rule for the TEXT token
def t_TEXT(t):
    r'((?<!\s)s*[^(\#\{)\n]+|<.*>)'
    if t.value.isspace():
        return
    return t

def t_DIGIT(t):
    r'\d+'
    return t

def t_COMMA(t):
    r'\,'
    return t

def t_PARENL(t):
    r'\['
    return t

def t_PARENR(t):
    r'\]'
    return t

# Define a rule for the indentation in the comment state
def t_comment_indentation(t):
    r'\n[ \t]*'
    t.lexer.lineno += 1
    indent_level = len(t.value) - 1
    if t.lexer.indent_stack[-1] >= indent_level:
        t.lexer.begin('INITIAL')
        if t.lexer.indent_stack[-1] == indent_level:
            return 
        else:
            while t.lexer.indent_stack[-1] > indent_level:
                t.lexer.indent_stack.pop()
            t.type = 'DEDENT'
            return t
    else:
        white_spaces = indent_level - t.lexer.indent_stack[-1] - 1
        aux = ''
        for i in range(white_spaces):
            aux += t.value[indent_level + i] 
            t.type = 'WHITESPACES'
            t.value = aux
            return t
    
# Define a rule for the indentation in the block state
def t_block_indentation(t): # Rever
    r'\n[ \t]*'
    t.lexer.lineno += 1
    indent_level = len(t.value) -1
    if t.lexer.indent_stack[-1] >= indent_level:
        while t.lexer.indent_stack[-1] > indent_level:
            t.lexer.indent_stack.pop()
        t.lexer.begin('INITIAL')
        t.type = 'DEDENT'
        return t
    else:
        return

# Define a rule for the indentation in the comment state
def t_ignorecomment_indentation(t):
    r'\n[ \t]*'
    t.lexer.lineno += 1
    indent_level = len(t.value) -1
    if t.lexer.indent_stack[-1] >= indent_level:
        t.lexer.begin('INITIAL')
        if t.lexer.indent_stack[-1] == indent_level:
            return 
        else:
            if t.lexer.indent_stack[-1] > indent_level:
                t.lexer.skip(-indent_level-1)
            t.type = 'DEDENT'
            return t
    else:
        return

def t_block_TEXT(t):
    r'.+'
    return t

def t_comment_TEXT(t):
    r'.+'
    return t

def t_ignorecomment_TEXT(t):
    r'.+'

# Define an error handling function
def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Create the lexer
lexer = lex.lex()
lexer.indent_stack = [0]

# Test the lexer
data =  '''
ul
  li OLAAAAAAA
    li ola
ul
  li massa
'''

lexer.input(data)

for token in lexer:
    print(token)

