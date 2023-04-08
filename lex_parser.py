import ply.lex as lex

# Define the tokens for PugJS
tokens = (
    'ID',
    'TAG',
    'DOT',
    'TEXT',
    'CLASS',
    'EQUALS',
    'STRING',
    'INDENT',
    'DEDENT',
    'COMMENT',
    'ATTRIBUTE',
    'IGNORECOMMENT',
    'INTERPOLATION'
)

#'DOCTYPE',
# COMMA, RPAREN, LPAREN?
#'IF',
#'ELSE',
#'FOR',
#'EACH',
#'IN',
#'BLOCK'

states = (
    ('block', 'exclusive'),
    ('comment', 'exclusive')
)

# Palavras reservadas e simbolos terminais '(' ')' '.' e atributos

# Define regular expressions for each token
t_TAG = r'[a-z][a-z0-9]*'
t_STRING = r'\'[^\']*\'|"[^"]*"'
t_ignore = '\t\r'


# Define a rule for the attributes
def t_ATTRIBUTE(t):
    r'\(\s*\w+\s*=\s*(\'[^\']*\'|"[^"]*")(\s*,?\s*\w+\s*=\s*(\'[^\']*\'|"[^"]*"))*\s*\)'
    t.value = t.value.replace(',','')
    t.value = t.value.replace('\'','"')
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

def t_IGNORECOMMENT(t):
    r'//-.*'
    if len(t.value) - 3 == 0: 
        t.lexer.begin('comment')

def t_COMMENT(t):
    r'//.*'
    if len(t.value) - 2 == 0: 
        t.lexer.begin('block')
    return t

def t_INTERPOLATION(t):
    r'\#\{\w+\}'
    return t

def t_ID(t):
    r'\#\w+'
    return t

def t_CLASS(t):
    r'\.\w+'
    return t

def t_DOT(t):
    r'\.'
    t.lexer.begin('block')
    return t

def t_EQUALS(t): 
    r'='
    return t

# Define a rule for the TEXT token
def t_TEXT(t):
    r'(?<!\s)s*[^(\#\{)\n]+'
    t.value = t.value.strip()
    return t

# Define a rule for the indentation in the block state
def t_comment_block_indentation(t):
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
    
def t_block_TEXT(t):
    r'.+'
    return t

def t_comment_TEXT(t):
    r'.+'

# Define an error handling function
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Create the lexer
lexer = lex.lex()
lexer.indent_stack = [0]

# Test the lexer
data = '''
html(lang="en")
  head
    title= pageTitle
      script(type='text/javascript').
        if (foo) bar(1 + 5)
  body
    //
      isto é um comentário em bloco
      para aparecer no html
    //-
      isto é um comentário em bloco
      para não aparecer no html
    h1 Pug - node template engine
      #container.col
        if youAreUsingPug
          p You are #{amazing}
        else
          p Get on it!
        p.
          Pug is a terse and simple templating language with a
          strong focus on performance and powerful features
'''

lexer.input(data)

for token in lexer:
    print(token)

