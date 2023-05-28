import ply.lex as lex
import sys

from IndentationException import IndentationException
from UnexpectedToken import UnexpectedToken

# Reserved words 
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'unless': 'UNLESS',  # Negated if
    'each': 'EACH',
    'when': 'WHEN',
    'default': 'DEFAULT',
    'case': 'CASE',
}

tokens = (
    'ATTRIBUTES',  # Everything between ( and )
    'INDENT',  # For blocks indented
    'DEDENT',  # For removing indentation
    'CLASS',  # HTML classes
    'ID',  # HTML ids (1 max per tag)
    'TAG',
    'COMMA',
    'EQUALS',
    'BAR',
    'BEGININTERP',  # Valid for Javascript and Tag Interpolation
    'ENDINTERP',
    'DOT',
    'TEXT',
    'COMMENT',
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
    'NEWLINE',
    'DOCTYPE',
    'IDENTIFIER'
)

states = (
    ('ignorecomment', 'exclusive'),  # In this state, we don't want to read anything
    ('assign', 'exclusive'),  # Enables us to read JSCODE like reading TEXT (.*)
    ('attributes', 'exclusive'),  # Enables us to read everything until ']'
    ('interpolation', 'exclusive'),  # Simplify reading of tokens
    ('comment', 'exclusive'),
    ('block', 'exclusive'),
    ('conditional', 'exclusive'),  # To read condition as .+
    ('iteration', 'exclusive'),
    ('code', 'exclusive'),
    ('taginterpolation', 'inclusive')
)


# Function to get indentation level 
def indentation_level(line):
    count = 0
    for char in line:
        if char == ' ':
            count += 1
        elif char == '\t':
            count += 4
    return count

# Indentation is when a line starts with '\n' and a sequence of ' ' and '\t'

# Execute one of 5 actions:
# - keep code in the same indentation
# - indent
# - dedent and call itself again
# - dedent and return
# - error
def t_INITIAL_indentation(t):
    r'\n[ \t]*'

    # get the indentation level
    current_indentation = indentation_level(t.value[1:])
    # get the previous indentation level
    previous_indentation = t.lexer.indent_stack[-1]

    t.lexer.newline = True

    if previous_indentation == current_indentation: # - keep code in the same indentation
        t.lexer.lineno += 1
        return

    elif previous_indentation > current_indentation:
        aux = t.lexer.indent_stack[-1]
        t.lexer.indent_stack.pop()
        if t.lexer.indent_stack[-1] > current_indentation: # - dedent and call itself again
            t.lexer.skip(-len(t.value))
        elif t.lexer.indent_stack[-1] < current_indentation: # - error
            raise IndentationException(f'Inconsistent indentation. Expecting either {t.lexer.indent_stack[-1]} or {aux} spaces/tabs on line {t.lexer.lineno}.')
        else: # - dedent and return
            t.lexer.lineno += 1
        t.type = 'DEDENT'
        return t

    else: # - indent
        t.lexer.lineno += 1
        t.lexer.indent_stack.append(current_indentation)
        t.type = 'INDENT'
        return t
    
def t_ignorecomment_indentation(t):
    r'\n[ \t]*'

    # get the indentation level
    current_indentation = indentation_level(t.value[1:])
    # get the previous indentation level
    previous_indentation = t.lexer.indent_stack[-1]

    t.lexer.newline = True

    if previous_indentation == current_indentation:
        t.lexer.lineno += 1
        t.lexer.pop_state()
        return
    elif previous_indentation > current_indentation:
        t.lexer.skip(-len(t.value))
        t.lexer.pop_state()
        return
    else:
        t.lexer.lineno += 1
        return

def t_code_indentation(t):
    r'\n[ \t]*'

    # get the indentation level
    current_indentation = indentation_level(t.value[1:])
    # get the previous indentation level
    previous_indentation = t.lexer.indent_stack[-1]

    t.lexer.newline = True

    if previous_indentation == current_indentation:
        t.lexer.lineno += 1
        t.lexer.pop_state()
        return
    elif previous_indentation > current_indentation:
        t.lexer.skip(-len(t.value))
        t.lexer.pop_state()
        return
    else:
        t.lexer.lineno += 1
        return

def t_comment_indentation(t):
    r'\n[ \t]*'

    # get the indentation level
    current_indentation = indentation_level(t.value[1:])
    # get the previous indentation level
    previous_indentation = t.lexer.indent_stack[-1]

    t.lexer.newline = True

    if previous_indentation == current_indentation:
        t.lexer.pop_state()
        t.lexer.lineno += 1
        return
    elif previous_indentation > current_indentation:
        t.lexer.pop_state()
        t.lexer.skip(-len(t.value))
        return
    else:
        t.lexer.lineno += 1
        aux = current_indentation
        nc = 0

        for i in range(len(t.value) - 1):
            if t.value[-i - 1] == '\t':
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
def t_block_indentation(t):  # Rever
    r'\n[ \t]*'

    # get the indentation level
    current_indentation = indentation_level(t.value[1:])
    # get the previous indentation level
    previous_indentation = t.lexer.indent_stack[-1]

    t.lexer.newline = True

    if previous_indentation == current_indentation:
        t.lexer.pop_state()
        t.lexer.lineno += 1
        return
    elif previous_indentation > current_indentation:
        t.lexer.pop_state()
        t.lexer.skip(-len(t.value))
        return
    else:
        t.lexer.lineno += 1
        aux = current_indentation
        nc = 0

        for i in range(len(t.value) - 1):
            if t.value[-i - 1] == '\t':
                aux -= 4
            else:
                aux -= 1

            if aux == previous_indentation:
                t.lexer.skip(-nc)
                break
            else:
                nc += 1
        t.type = 'NEWLINE'
        return t
        # Para controlar os whitespaces
        # sempres dois espaços antes do texto do block


# How to enter the attributes state
def t_lparen(t):
    r'\('
    t.lexer.newline = False
    t.lexer.push_state('attributes')


# Attributes is everything between ( and )
# Can contain ( and ) in the middle
# So we need to have a counter for the number of parenthesis opened 
# and store the attributes in a buffer
def t_attributes_ATTRIBUTES(t):
    r'[^\)\(]*[\(\)]'
    t.lexer.attributesBuffer += t.value
    t.lexer.newline = False
    if t.value[-1] == '(':
        t.lexer.parCount += 1
    elif t.value[-1] == ')':
        t.lexer.parCount -= 1
        if t.lexer.parCount == -1:
            t.value = t.lexer.attributesBuffer[:-1]
            t.lexer.pop_state()
            t.lexer.attributesBuffer = ""
            t.lexer.parCount = 0
            return t


# Comments that will be ignored start with //-
def t_ignorecomment(t):
    r'//-.*'
    t.lexer.newline = False
    t.lexer.push_state('ignorecomment')


# Comments that pass to the HTML file start with //
def t_COMMENT(t):
    r'//.*'
    t.lexer.newline = False
    t.lexer.push_state('comment')
    return t

# For explicit self-closing tags 
def t_BAR(t):
    r'\/'
    t.lexer.newline = False
    return t


# For assignment of text
def t_EQUALS(t):
    r'\='
    t.lexer.newline = False
    t.lexer.push_state('assign')
    return t


# JSCODE is everything after a line starting with -
def t_JSCODE(t):
    r'\-.*'
    t.lexer.newline = False
    t.value = t.value[1:] # Remove the / starting the line
    if t.value.isspace() or t.value == "": # if the line with the - doesn't have anything it is a block of code
        t.lexer.push_state('code')
    return t

# When we are assigning to a tag, we want to read all code after it
# Can contain expressions, concatenation of variables, etc
def t_assign_JSCODE(t):
    r'.+'
    t.lexer.newline = False
    t.lexer.pop_state()
    return t


# Start of both tag and variable interpolation
def t_BEGININTERP(t):
    r'\#(\{|\[)'
    if t.value == '#{':
        t.lexer.push_state('interpolation')
        t.lexer.newline = False
    elif t.value == '#[':
        t.lexer.push_state('taginterpolation')
        t.lexer.newline = True # In this case we want this set to True, because we can start a new tag from here
    return t

def t_interpolation_JSCODE(t):
    r'[^\}]+'
    t.lexer.newline = False
    return t

# When we leave the interpolation
def t_interpolation_ENDINTERP(t):
    r'(\}|\])'
    t.lexer.newline = False
    t.lexer.pop_state()
    return t


# When we leave the tag interpolation
def t_taginterpolation_ENDINTERP(t):
    r'(\}|\])'
    t.lexer.newline = False
    t.lexer.pop_state()
    return t


# An expression to be iterated must have before the keyword 'in'
def t_iteration_JSCODE(t):
    r'(?<=(in\s)).*'
    t.lexer.pop_state()
    t.lexer.newline = False
    return t


# Normal comma (for iteration)
def t_iteration_COMMA(t):
    r','
    t.lexer.newline = False
    return t


# IN token (for iteration)
def t_iteration_IN(t):
    r'in\b'
    t.lexer.newline = False
    return t


# Iterator variable (for iteration)
def t_iteration_IDENTIFIER(t):
    r'\w+'
    t.lexer.newline = False
    return t


# In the conditional state, CONDITION can be read with .+
def t_conditional_CONDITION(t):
    r'[^\n:]+'
    t.lexer.pop_state()
    t.lexer.newline = False
    return t


# Else if token
# Enters conditional state
def t_ELSEIF(t):
    r'else[ ]if'
    t.lexer.push_state('conditional')
    t.lexer.newline = False
    return t

# DOCTYPE line 
def t_DOCTYPE(t):
    r'(?<=(\s|\[))doctype.*'
    return t


# A TAG must have before a space 
def t_TAG(t):
    r'(?<=\s)[A-Za-z]\w*'
    t.type = reserved.get(t.value, 'TAG') # We want to check for reserved keywords
    t.lexer.newline = False

    match t.type: # Enter the restricted states
        case 'UNLESS' | 'WHILE' | 'CASE' | 'WHEN' | 'IF':
            t.lexer.push_state('conditional')
        case 'EACH':
            t.lexer.push_state('iteration')
        case _:
            pass
    return t


# An id can have '_' , '-' and normal characters
def t_ID(t):
    r'\#[\w\-_]+'
    if t.lexer.newline: # If no tag is read, it is a div
        t.lexer.skip(-len(t.value))
        t.type = 'TAG'
        t.value = 'div'
        t.lexer.newline = False
        return t

    t.value = t.value[1:]
    return t


# Same logic as ID
def t_CLASS(t):
    r'\.[\w\-_]+'
    if t.lexer.newline:
        t.lexer.skip(-len(t.value))
        t.type = 'TAG'
        t.value = 'div'
        t.lexer.newline = False
        return t

    t.value = t.value[1:]
    return t


# Defines the beginning of a block
def t_DOT(t):
    r'\.'
    t.lexer.push_state('block')
    t.lexer.newline = False
    return t

# For block expansion
def t_doispontos(t):
    r'\:[ \t]*'
    t.type = 'INDENT' # We deal the inner tag as an indented tag
    t.lexer.newline = True
    t.lexer.indent_stack.append(t.lexer.indent_stack[-1]+2) # Must add the new indentation level
    return t

# Text can contain interpolation, so we need to check for that
# It can also be inside < and >, and can have no interpolation
def t_TEXT(t):
    r'.+?(?=\#(\{|\[))|<.*?>|.+'
    t.lexer.newline = False
    if t.value.isspace():
        return
    return t

# Begin of interpolation in the taginterpolation state
def t_taginterpolation_BEGININTERP(t):
    r'\#(\{|\[)'
    if t.value == '#{':
        t.lexer.push_state('interpolation')
        t.lexer.newline = False
    elif t.value == '#[':
        t.lexer.push_state('taginterpolation')
        t.lexer.newline = True
    return t

# ID inside taginterpolation (cannot have an endinterpolation token before)
def t_taginterpolation_ID(t):
    r'(?<!(\]|\}))\#[\w\-_]+'
    if t.lexer.newline:
        t.lexer.skip(-len(t.value))
        t.type = 'TAG'
        t.value = 'div'
        t.lexer.newline = False
        return t

    t.value = t.value[1:]
    return t

# CLASS inside taginterpolation (cannot have an endinterpolation token before)
def t_taginterpolation_CLASS(t):
    r'(?<!(\]|\}))\.[\w\-_]+'
    if t.lexer.newline:
        t.lexer.skip(-len(t.value))
        t.type = 'TAG'
        t.value = 'div'
        t.lexer.newline = False
        return t

    t.value = t.value[1:]
    return t

# Same for lparen (begin of attributes)
def t_taginterpolation_lparen(t):
    r'(?<!(\]|\}))\('
    t.lexer.newline = False
    t.lexer.push_state('attributes')

# Read a TAG inside taginterpolation (must be immediately after the BEGININTERP token)
def t_taginterpolation_TAG(t):
    r'(?<=\[)[A-Za-z]\w*'
    t.type = reserved.get(t.value, 'TAG')
    t.lexer.newline = False

    match t.type:
        case 'UNLESS' | 'WHILE' | 'CASE' | 'WHEN' | 'IF' | 'ELSE' | 'EACH' | 'DEFAULT':
            raise UnexpectedToken('Syntax Error: Unexpected token')
        case _:
            pass
    return t

# TEXT inside taginterpolation must be followed by BEGININTERP or ENDINTERP
def t_taginterpolation_TEXT(t):
    r'.+?((?=\#(\{|\[))|(?=\]))'
    t.lexer.newline = False
    if t.value.isspace():
        return
    return t


# A comment can be mode of multiple TEXT lines(it will be joined after)
def t_comment_TEXT(t):
    r'.+'
    t.lexer.newline = False
    return t


# Code can be mode of multiple TEXT lines
def t_code_TEXT(t):
    r'.+'
    t.lexer.newline = False
    return t


# Ignorecomments can be mode of multiple TEXT lines
def t_ignorecomment_TEXT(t):
    r'.+'
    t.lexer.newline = False


# When we begin interpolation inside a block (similar to the normal BEGININTERP)
def t_block_BEGININTERP(t):
    r'\#(\{|\[)'
    if t.value == '#{':
        t.lexer.push_state('interpolation')
        t.lexer.newline = False
    elif t.value == '#[':
        t.lexer.push_state('taginterpolation')
        t.lexer.newline = True
    return t


# TEXT inside a block can have 0 or more occurences of interpolation (both tag and variable)
def t_block_TEXT(t):
    r'.+?(?=(\#\{|\#\[))|.+'
    t.lexer.newline = False
    return t


# error handling function
def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Ignore these characters inside these states
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
