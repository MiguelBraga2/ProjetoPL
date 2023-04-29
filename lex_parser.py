import ply.lex as lex

# Define the tokens for PugJS
tokens = (
    'INDENT',
    'DEDENT',
    'CLASS',
    'ID',
    'TAG',
    'IDENTIFIER',
    'ATTRIBUTENAME',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'EQUALS',
    'BOOLEAN',
    'STRING',
    'IGNORECOMMENT',
    'BAR',
    'BEGININTERP',
    'ENDINTERP',
    'DOT',
    'TEXT',
    'COMMENT',
    'NUMBER',
    'JSCODE',
    'IF',
    'ELSE',
    'UNLESS',
    'CONDITION',
    'WHILE',
    'EACH',
    'IN',
    'WHEN',
    'DEFAULT',
    'CASE'
    # falta dois pontos e |
)


states = (
    ('ignorecomment', 'exclusive'),
    ('assign', 'exclusive'),
    ('attributes', 'exclusive'),
    ('interpolation', 'exclusive'),
    ('comment', 'exclusive'),
    ('block', 'exclusive'),
    ('conditional', 'exclusive'),
    ('iteration', 'exclusive'),
)

# Function to get indentation level 
def indetation_level(line):
    count = 0
    for char in line:
        if char == ' ':
            count += 1
        elif char == '\t':
            count += 4
    return count


# Define a rule for the indentation
def t_INITIAL_indentation(t):
    r'\n[ \t]*'

    # get the indentation level
    current_indentation = indetation_level(t.value[1:])
    # get the previous indentation level
    previous_indentation = t.lexer.indent_stack[-1]

    if previous_indentation == current_indentation:
        t.lexer.lineno += 1 
        return 
    
    elif previous_indentation > current_indentation:
        t.lexer.indent_stack.pop()
        if t.lexer.indent_stack[-1] > current_indentation:
            t.lexer.skip(-len(t.value))
        elif t.lexer.indent_stack[-1] < current_indentation:
            raise ValueError('Indententation error')
        else:
            t.lexer.lineno += 1 
        t.type = 'DEDENT'
        return t
    
    else:
        t.lexer.lineno += 1 
        t.lexer.indent_stack.append(current_indentation)
        t.type = 'INDENT'
        return t


# Define a rule for the indentation in the ignorecomment state
def t_ignorecomment_indentation(t):
    r'\n[ \t]*'

    # get the indentation level
    current_indentation = indetation_level(t.value[1:])
    # get the previous indentation level
    previous_indentation = t.lexer.indent_stack[-1]
    
    if previous_indentation == current_indentation:
        t.lexer.lineno += 1
        t.lexer.begin('INITIAL')
        return 
    elif previous_indentation > current_indentation: 
        t.lexer.skip(-len(t.value))
        t.lexer.begin('INITIAL')
        return
    else:
        t.lexer.lineno += 1
        return


# Define a rule for the indentation in the comment state
def t_comment_indentation(t):
    r'\n[ \t]*'

    # get the indentation level
    current_indentation = indetation_level(t.value[1:])
    # get the previous indentation level
    previous_indentation = t.lexer.indent_stack[-1]

    if previous_indentation == current_indentation:
        t.lexer.begin('INITIAL')
        t.lexer.lineno += 1
        return 
    elif previous_indentation > current_indentation:
        t.lexer.begin('INITIAL')
        t.lexer.skip(-len(t.value))
        return 
    else:
        t.lexer.lineno += 1
        aux = current_indentation
        nc = 0

        for i in range(len(t.value)-1):
            if t.value[-i-1] == '\t':
                aux -= 4
            else:
                aux -= 1
            
            if aux == previous_indentation:
                t.lexer.skip(-nc)
                return
            else:
                nc += 1
        # Para controlar os whitespaces



# Define a rule for the indentation in the block state
def t_block_indentation(t): # Rever
    r'\n[ \t]*'

    # get the indentation level
    current_indentation = indetation_level(t.value[1:])
    # get the previous indentation level
    previous_indentation = t.lexer.indent_stack[-1]

    if previous_indentation == current_indentation:
        t.lexer.begin('INITIAL')
        t.lexer.lineno += 1
        return 
    elif previous_indentation > current_indentation:
        t.lexer.begin('INITIAL')
        t.lexer.skip(-len(t.value))
        return 
    else:
        t.lexer.lineno += 1
        # sempres dois espaços antes do texto do block


def t_LPAREN(t):
    r'\('
    t.lexer.push_state('attributes')
    return t


def t_attributes_ATTRIBUTENAME(t):
    r'[a-z]+'
    return t


def t_attributes_EQUALS(t):
    r'\='
    t.lexer.push_state('assign')
    return t


def t_attributes_COMMA(t):
    r','
    return t


def t_attributes_RPAREN(t):
    r'\)'
    t.lexer.pop_state()
    return t


# Define a rule for the unbuffered comments
def t_IGNORECOMMENT(t):
    r'//-.*'
    t.lexer.begin('ignorecomment')


def t_COMMENT(t):
    r'//.*'
    t.lexer.begin('comment')
    return t


def t_BAR(t):
    r'\/'
    return t


# Define a rule for the EQUALS symbol
def t_EQUALS(t):
    r'\='
    t.lexer.push_state('assign')
    return t


def t_JSCODE(t):
    r'\-.*'
    t.value = t.value[1:]
    return t


# ASSIGN
def t_assign_BOOLEAN(t):
    r'(true|else)'
    t.lexer.pop_state()
    return t

def t_assign_NUMBER(t):
    r'\d+'
    t.lexer.pop_state()
    return t

def t_assign_IDENTIFIER(t):
    r'\w+'
    t.lexer.pop_state()
    return t

def t_assign_STYLE(t):
    r'\{[^\}]*\}'
    t.value = t.value.replace(" ", "")
    t.value = t.value.replace(",", ";")
    t.value = t.value.replace("'", "")
    t.value = t.value.replace("\"", "")
    t.value = t.value[:-1] + ';}'
    t.lexer.pop_state()
    return t

def t_assign_STRING(t):
    r'\'[^\']*\'|"[^\"]*"'
    t.lexer.pop_state()
    return t


# INTERPOLATION
def t_BEGININTERP(t):
    r'\#\{'
    t.lexer.push_state('interpolation')
    return t


def t_interpolation_STRING(t):
    r'\'[^\']*\'|"[^\"]*"'
    return t

def t_interpolation_NUMBER(t):
    r'\d+'
    return t

def t_interpolation_IDENTIFIER(t):
    r'\w+'
    return t

def t_interpolation_ENDINTERP(t):
    r'\}'
    t.lexer.pop_state()
    return t


# ITERATION
def t_EACH(t):
    r'each\b'
    t.lexer.begin('iteration')
    return t

def t_iteration_JSCODE(t):
    r'(?<=(in\s)).*'
    t.lexer.begin('INITIAL')
    return t 

def t_iteration_COMMA(t):
    r','
    return t

def t_iteration_IN(t):
    r'in\b'
    return t

def t_iteration_IDENTIFIER(t):
    r'\w+'
    return t

def t_IF(t):
    r'(?<=else)\sif\b|if\b'
    t.lexer.begin('conditional')
    return t

def t_CASE(t):
    r'case\b'
    t.lexer.begin('conditional')
    return t

def t_WHEN(t):
    r'when\b'
    t.lexer.begin('conditional')
    return t

def t_DEFAULT(t):
    r'default\b'
    return t

def t_WHILE(t):
    r'while\b'
    t.lexer.begin('conditional')
    return t


def t_conditional_CONDITION(t):
    r'.+'
    t.lexer.begin('INITIAL')
    return t


def t_ELSE(t):
    r'else\b'
    return t

def t_UNLESS(t):
    r'unless\b'
    t.lexer.begin('conditional')
    return t


# Define a rule for the TAG token
def t_TAG(t):
    r'[a-z][a-z0-9]*'
    return t


# Define a rule for the ID token
def t_ID(t):
    r'\#\w+'
    t.value = t.value[1:]
    return t


# Define a rule for the CLASS token
def t_CLASS(t):
    r'\.\w+'
    t.value = t.value[1:]
    return t


def t_DOT(t):
    r'\.'
    t.lexer.begin('block')
    return t
    

def t_TEXT(t):
    r'((?<!\s)[ \t]+[^\n\#]+((?!(\#\{))\#[^\n\#]+)*|<.*>|(?<=})[^\n\#]+((?!(\#\{))\#[^\n\#]+)*)'
    if t.value.isspace():
        return
    return t


def t_comment_TEXT(t):
    r'.+'
    return t


def t_ignorecomment_TEXT(t):
    r'.+'


def t_block_TEXT(t):
    r'[^\n\#]+((?!(\#\{))\#[^\n\#]+)*'
    return t


def t_block_BEGININTERP(t):
    r'\#\{'
    t.lexer.push_state('interpolation')
    return t


def t_whitespaces(t):
    r'[ \t]+'
    pass


# Define an error handling function
def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


t_ignore = ''
t_assign_ignore = ' \t'
t_ignorecomment_ignore = ''
t_comment_ignore = ''
t_attributes_ignore = ' \t\n'
t_interpolation_ignore = ' \t'
t_conditional_ignore = ' \t'
t_iteration_ignore = ' \t'


# Create the lexer
lexer = lex.lex()
lexer.indent_stack = [0]

data = """
each val in [1,3,4,5]
  p ola 
""" 

lexer.input(data)

for tok in lexer:
    print(tok)