import ply.lex as lex
import sys

# Reserved words 
reserved = {
    'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'unless' : 'UNLESS',
   'each' : 'EACH',
   'when' : 'WHEN',
   'default' : 'DEFAULT',
   'case' : 'CASE'
}

# Define the tokens for PugJS
tokens = (
    'ATTRIBUTES',
    'INDENT',
    'DEDENT',
    'CLASS',
    'ID',
    'TAG',
    'IDENTIFIER',
    'COMMA',
    'EQUALS',
    'STRING',
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
    'CASE',
    'ELSEIF',
    # falta dois pontos e |
)

# Define the states for pugjs
states = (
    ('ignorecomment', 'exclusive'),
    ('assign', 'exclusive'),
    ('attributes', 'exclusive'),
    ('interpolation', 'exclusive'),
    ('comment', 'exclusive'),
    ('block', 'exclusive'),
    ('conditional', 'exclusive'),
    ('iteration', 'exclusive'),
    ('code', 'exclusive')
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

    t.lexer.newline = True

    if previous_indentation == current_indentation:
        t.lexer.lineno += 1 
        return 
    
    elif previous_indentation > current_indentation:
        t.lexer.indent_stack.pop()
        if t.lexer.indent_stack[-1] > current_indentation:
            t.lexer.skip(-len(t.value))
        elif t.lexer.indent_stack[-1] < current_indentation:
            raise ValueError('Indentation error')
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

    t.lexer.newline = True
    
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


# Define a rule for the indentation in the code state
def t_code_indentation(t):
    r'\n[ \t]*'

    # get the indentation level
    current_indentation = indetation_level(t.value[1:])
    # get the previous indentation level
    previous_indentation = t.lexer.indent_stack[-1]

    t.lexer.newline = True
    
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

    t.lexer.newline = True

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

    t.lexer.newline = True

    if previous_indentation == current_indentation:
        t.lexer.begin('INITIAL')
        t.lexer
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
        # sempres dois espaços antes do texto do block


# Define a rule to enter the attributes state
def t_lparen(t):
    r'\('
    t.lexer.begin('attributes')


# Define a rule for the attributes
def t_attributes_ATTRIBUTES(t):
    r'[^\)\(]*[\(\)]'
    t.lexer.attributesBuffer += t.value
    if t.value[-1] == '(':
        t.lexer.parCount+=1
    elif t.value[-1] == ')':
        t.lexer.parCount-=1
        if t.lexer.parCount == -1:
            t.value = t.lexer.attributesBuffer[:-1]
            t.lexer.begin('INITIAL')
            t.lexer.attributesBuffer = ""
            t.lexer.parCount=0
            return t 


# Define a rule for the unbuffered comments
def t_ignorecomment(t):
    r'//-.*'
    t.lexer.begin('ignorecomment')


# Define a rule for the comments
def t_COMMENT(t):
    r'//.*'
    t.lexer.begin('comment')
    return t


# Define a rule for the BAR symbol
def t_BAR(t):
    r'\/'
    return t


# Define a rule for the EQUALS symbol
def t_EQUALS(t):
    r'\='
    t.lexer.push_state('assign')
    return t


# Define a rule for the JSCODE 
def t_JSCODE(t):
    r'\-.*'
    t.value = t.value[1:]
    t.lexer.begin('code')
    return t


# Define a rule for the STYLE 
def t_assign_STYLE(t):
    r'\{[^\}]*\}'
    t.value = t.value.replace(" ", "")
    t.value = t.value.replace(",", ";")
    t.value = t.value.replace("'", "")
    t.value = t.value.replace("\"", "")
    t.value = t.value[:-1] + ';}'
    t.lexer.pop_state()
    return t


# Define a rule for the JSCODE in assign state 
def t_assign_JSCODE(t):
    r'.+'
    t.lexer.pop_state()
    return t


#  Define a rule for the begin interpolation symbols
def t_BEGININTERP(t):
    r'\#\{'
    t.lexer.push_state('interpolation')
    return t


#  Define a rule for the STRING
def t_interpolation_STRING(t):
    r'\'[^\']*\'|"[^\"]*"'
    return t


#  Define a rule for the NUMBER
def t_interpolation_NUMBER(t):
    r'\d+'
    return t


#  Define a rule for the IDENTIFIER
def t_interpolation_IDENTIFIER(t):
    r'\w+'
    return t


#  Define a rule for the end interpolation symbol
def t_interpolation_ENDINTERP(t):
    r'\}'
    t.lexer.pop_state()
    return t


#  Define a rule for the JSCODE in iteration state
def t_iteration_JSCODE(t):
    r'(?<=(in\s)).*'
    t.lexer.begin('INITIAL')
    return t 


#  Define a rule for the COMA symbol
def t_iteration_COMMA(t):
    r','
    return t


#  Define a rule for the IN word
def t_iteration_IN(t):
    r'in\b'
    return t


#  Define a rule for the IDENTIFIER
def t_iteration_IDENTIFIER(t):
    r'\w+'
    return t


#  Define a rule for the CONDITION of conditional
def t_conditional_CONDITION(t):
    r'.+'
    t.lexer.begin('INITIAL')
    return t


#  Define a rule for the ELSEIF token
def t_ELSEIF(t):
    r'else[ ]if'
    t.lexer.begin('conditional')
    return t


# Define a rule for the TAG token
def t_TAG(t):
    r'[a-z][a-z0-9]*'
    t.type = reserved.get(t.value, 'TAG')
    
    match t.type:
        case 'UNLESS' | 'WHILE' | 'CASE' | 'WHEN' | 'IF':
            t.lexer.begin('conditional')
        case 'EACH':
            t.lexer.begin('iteration')
        case _:
            pass
    return t


# Define a rule for the ID token
def t_ID(t):
    r'\#\w+'
    if t.lexer.newline:
        t.lexer.skip(-len(t.value))
        t.type = 'TAG'
        t.value = 'div'
        t.lexer.newline = False
        return t
    
    t.value = t.value[1:]
    return t


# Define a rule for the CLASS token
def t_CLASS(t):
    r'\.\w+'
    if t.lexer.newline:
        t.lexer.skip(-len(t.value))
        t.type = 'TAG'
        t.value = 'div'
        t.lexer.newline = False
        return t
    
    t.value = t.value[1:]
    return t


# Define a rule for the DOT token
def t_DOT(t):
    r'\.'
    t.lexer.begin('block')
    return t
    

# Define a rule for the TEXT token
def t_TEXT(t):
    r'.+?\#\{|<.*?>|.+'
    if t.value.isspace():
        return
    return t


# Define a rule for the comment text 
def t_comment_TEXT(t):
    r'.+'
    return t


# Define a rule for the javascript code
def t_code_JSCODE(t):
    r'.+'
    return t


# Define a rule for the ignorecomment text
def t_ignorecomment_TEXT(t):
    r'.+'


# Define a rule for the block text
def t_block_TEXT(t):
    r'.+?\#\{|.+'
    return t


# Define a rule for the block BEFININTERP token
def t_block_BEGININTERP(t):
    r'\#\{'
    t.lexer.push_state('interpolation')
    return t


# Define an error handling function
def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


t_ignore = ''
t_assign_ignore = ' \t'
t_ignorecomment_ignore = ''
t_comment_ignore = ''
t_code_ignore = ''
t_attributes_ignore = ' \t\n'
t_interpolation_ignore = ' \t'
t_conditional_ignore = ' \t'
t_iteration_ignore = ' \t'


# Create the lexer
lexer = lex.lex()
lexer.indent_stack = [0]
lexer.parCount = 0
lexer.attributesBuffer = ""
lexer.newline = True
