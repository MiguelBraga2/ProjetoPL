import ply.yacc as yacc
from lex_parser import tokens,lexer
from tree import Tree

def p_lines(p):
    """
    lines : lines line
          | line
    """
    if len(p) == 3: # lines (line1 line2 ...)
        p[0] = p[1].addSubTree(p[2])
    else:
        p[0] = Tree(type='lines', trees=[p[1]])


def p_line(p):
    """
    line : tagline
         | code
         | comment
         | conditional
         | iteration
         | switch
    """
    p[0] = Tree(type='line', trees=[p[1]]) 


def p_line_doctype(p):
    """
    line : DOCTYPE
    """
    p[0] = Tree(type='line', trees=[Tree(type='DOCTYPE', value=p[1])])


def p_code(p):
    """
    code : code_lines
         | code_lines INDENT lines DEDENT
    """
    if len(p) == 2: 
        p[0] = Tree(type='code1', trees=[p[1]])
    else:
        p[0] = Tree(type='code2', trees=[p[1], Tree(type='INDENT', value=p[2]), p[3]])
    
def p_code_lines(p):
    """
    code_lines : JSCODE 
               | JSCODE code_text 
    """
    if len(p) == 2: 
        p[0] = Tree(type='code_lines1', trees=[Tree(type='JSCODE', value=p[1])])
    else:
        p[0] = Tree(type='code_lines2', trees=[Tree(type='JSCODE', value=p[1]), p[2]])

def p_code_text(p):
    """
    code_text : TEXT 
              | code_text TEXT 
    """
    if len(p) == 2: 
        p[0] = Tree(type='code_text', trees=[Tree(type='TEXT', value=p[1])])
    else:
        p[0] = p[1].addSubTree(Tree(type='TEXT', value=p[2]))


# SWITCH CASE
def p_switch(p):
    """
    switch : CASE CONDITION INDENT casesdefault DEDENT
    """
    p[0] = Tree(type='switch', trees=[Tree(type='CONDITION', value=p[2]), Tree(type='INDENT', value=p[3]), p[4]])

def p_casesdefault(p):
    """
    casesdefault : cases DEFAULT INDENT lines DEDENT
                 | cases
                 | DEFAULT INDENT lines DEDENT
    """
    if len(p) == 6:
        p[0] = Tree(type='casesdefault1', trees=[p[1], p[4]])
    elif len(p) == 2:
        p[0] = Tree(type='casesdefault2', trees=[p[1]])
    else:
        p[0] = Tree(type='casesdefault3', trees=[p[3]])

def p_cases(p):
    """
    cases : cases case 
          | case 
    """
    if len(p) == 3:
        p[0] = p[1].addSubTree(p[2])
    else:   
        p[0] = Tree(type='cases', trees=[p[1]])


def p_case(p): 
    """    
    case : WHEN CONDITION INDENT lines DEDENT
         | WHEN CONDITION
    """
    if len(p) == 6:
        p[0] = Tree(type='case', trees=[Tree(type='CONDITION', value=p[2]), p[4]])
    else:
        p[0] = Tree(type='case', trees=[Tree(type='CONDITION', value=p[2])])


# COMMENT
def p_comment(p):
    """
    comment : COMMENT comment_text
            | COMMENT
    """
    if len(p) == 3: # COMMENT comment_text (Multiple-line comments)
        p[0] = Tree(type='comment1', trees=[Tree(type='COMMENT', value=p[1]), p[2]])
    elif len(p) == 2: # COMMENT
        p[0] = Tree(type='comment2', trees=[Tree(type='COMMENT', value=p[1])])

def p_comment_text(p):
    """
    comment_text : comment_text TEXT
                 | TEXT  
    """
    if len(p) == 3: # comment_text TEXT
        p[0] = p[1].addSubTree(Tree(type='TEXT', value=p[2]))
    elif len(p) == 2: # TEXT
        p[0] = Tree('comment_text', '', [Tree(type='TEXT', value=p[1])])


# CONDITIONAL
def p_conditional(p):
    """
    conditional : conditional_begin conditional_middle conditional_final
                | conditional_begin conditional_final
                | conditional_begin conditional_middle
                | conditional_begin
    """

    if len(p) == 4:
        p[0] = Tree(type='conditional1', trees=[p[1], p[2], p[3]])    
    elif len(p) == 3:
        p[0] = Tree(type='conditional2', trees=[p[1], p[2]])
    else:
        p[0] = Tree(type='conditional3', trees=[p[1]])
        
def p_conditional_begin(p):
    """
    conditional_begin : IF CONDITION INDENT lines DEDENT
                      | IF CONDITION
                      | UNLESS CONDITION INDENT lines DEDENT 
                      | UNLESS CONDITION
    """
    if len(p) == 6 and p[1] == 'if':
        p[0] = Tree(type='conditional_begin1', trees=[Tree(type='CONDITION', value=p[2]), Tree(type='INDENT', value=p[3]), p[4]])
    elif len(p) == 3 and p[1] == 'if':
        p[0] = Tree(type='conditional_begin2', trees=[Tree(type='CONDITION', value=p[2])])
    elif len(p) == 6:
        p[0] = Tree(type='conditional_begin3', trees=[Tree(type='CONDITION', value=p[2]), Tree(type='INDENT', value=p[3]), p[4]])
    else:
        p[0] = Tree(type='conditional_begin4', trees=[Tree(type='CONDITION', value=p[2])])

def p_conditional_middle(p):
    """
    conditional_middle : conditional_middle ELSEIF CONDITION INDENT lines DEDENT 
                       | conditional_middle ELSEIF CONDITION
                       | ELSEIF CONDITION INDENT lines DEDENT 
                       | ELSEIF CONDITION
    """
    if len(p) == 8:
        p[0] = p[1].addSubTree(Tree(type='CONDITION', value=p[4] , trees=[Tree(type='INDENT', value=p[5]), p[6]]))
    elif len(p) == 5:
        p[0].addSubTree(Tree(type='CONDITION', value=p[4]))
    elif len(p) == 7:
        p[0] = Tree(type='conditional_middle', trees=[Tree(type='CONDITION', value=p[3] , trees=[Tree(type='INDENT', value=p[4]), p[5]])])
    else:
        p[0] = Tree(type='conditional_middle', trees=[Tree(type='CONDITION', value=p[3])])

def p_conditional_final(p):
    """
    conditional_final : ELSE INDENT lines DEDENT
                      | ELSE 
    """
    if len(p) == 5:
        p[0] = Tree(type='conditional_final1', trees=[Tree(type='INDENT', value=p[2]), p[3]])
    else:
        p[0] = Tree(type='conditional_final2')


# ITERATION
def p_iteration(p):
    """
    iteration : EACH IDENTIFIER IN JSCODE INDENT lines DEDENT
              | EACH IDENTIFIER COMMA IDENTIFIER IN JSCODE INDENT lines DEDENT
              | WHILE CONDITION INDENT lines DEDENT
    """
    if len(p) == 8:
        p[0] = Tree(type='iteration1', trees=[Tree(type='IDENTIFIER', value=p[2]), Tree(type='JSCODE', value=p[4]), Tree(type='INDENT', value=p[5]), p[6]])
    elif len(p) == 10:
        p[0] = Tree(type='iteration2', trees=[Tree(type='IDENTIFIER', value=p[2]), Tree(type='IDENTIFIER', value=p[4]), Tree(type='JSCODE', value=p[6]), Tree(type='INDENT', value=p[7]), p[8]])
    else:
        p[0] = Tree(type='iteration3', trees=[Tree(type='CONDITION', value=p[2]), Tree(type='INDENT', value=p[3]), p[4], Tree(type='DEDENT', value=p[5])]) 


# TAGS
def p_tagline(p):
    """
    tagline : tag content INDENT lines DEDENT 
            | tag INDENT lines DEDENT 
            | tag content
            | tag BAR
            | tag DOT NEWLINE block_text
            | tag
    """
    if len(p) == 6: # tag content INDENT lines DEDENT
        p[0] = Tree(type='tagline1', trees=[p[1], p[2], Tree(type='INDENT', value=p[3]), p[4]])
    elif len(p) == 5: # tag INDENT lines DEDENT
        if p[2] == '.': # tag DOT NEWLINE text
            p[0] = Tree(type='tagline5', trees=[p[1], p[4]])
        else: # tag INDENT lines DEDENT
            p[0] = Tree(type='tagline2', trees=[p[1], Tree(type='INDENT', value=p[2]), p[3]])
    elif len(p) == 3:
        if p[2] == '/': # tag BAR
            p[0] = Tree(type='tagline4', trees=[p[1], Tree(type='BAR', value=p[2])])
        else: # tag content
            p[0] = Tree(type='tagline3', trees=[p[1], p[2]])
    else: # tag
        p[0] = Tree(type='tagline6', trees=[p[1]])

def p_tag_tag(p):
    """
    tag : TAG attributes
        | TAG 
    """
    if len(p) == 3:
        p[0] = Tree(type='tag1', trees=[Tree(type='TAG', value=p[1]), p[2]])
    else:
        p[0] = Tree(type='tag2', trees=[Tree(type='TAG', value=p[1])])
    
def p_attributes(p):
    """
    attributes : attribute_list ID attribute_list
               | attribute_list ID
               | attribute_list
               | ID attribute_list
               | ID
    """
    if len(p) == 4:
        p[0] = Tree(type='attributes1', trees=[p[1], Tree(type='ID', value=p[2]) , p[3]])
    elif len(p) == 3:
        if type(p[1]) == str:
            p[0] = Tree(type='attributes2', trees=[Tree(type='ID', value=p[1]) , p[2]])
        else:
            p[0] = Tree(type='attributes3', trees=[p[1], Tree(type='ID', value=p[2])])
    else:
        if type(p[1]) == str:
            p[0] = Tree(type='attributes4', trees=[Tree(type='ID', value=p[1])])
        else:
            p[0] = Tree(type='attributes5', trees=[p[1]])           

def p_attributes_list(p):
    """
    attribute_list : attribute_list attribute  
                   | attribute
    """ 
    if len(p) == 3:
        p[0] = p[1].addSubTree(p[2])
    else:
        p[0] = Tree(type='attribute_list', trees=[p[1]])   

def p_attribute_class(p):
    """
    attribute : CLASS
    """
    p[0] = Tree(type='CLASS', value=p[1])

def p_attribute_attributes(p):
    """
    attribute : ATTRIBUTES
    """
    p[0] = Tree(type='ATTRIBUTES', value=p[1])

def p_content(p):
    """           
    content : EQUALS JSCODE
            | text
    """
    if len(p) == 3: # EQUALS interpolation
        p[0] = Tree(type='content1', trees=[Tree(type='JSCODE', value=p[2])])
    elif len(p) == 2: # text
        p[0] = Tree(type='content2', trees=[p[1]])

def p_interpolation(p):
    """
    interpolation : JSCODE
    """
    p[0] = Tree(type='interpolation1', trees=[Tree(type='JSCODE', value=p[1])])
    """if p[1][0] == '"': # STRING
        p[0] = Tree(type='interpolation1', trees=[Tree(type='STRING', value=p[1][1:-1])])
    elif p[1][0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']: # NUMBER
        p[0] = Tree(type='interpolation3', trees=[Tree(type='NUMBER', value=p[1])])
    else: # IDENTIFIER
        p[0] = Tree(type='interpolation2', trees=[Tree(type='IDENTIFIER', value=p[1])])"""
    
def p_interp(p):
    """
    interp : interpolation
           | tagline
    """
    p[0] = p[1]

def p_block_text(p):
    """
    block_text : block_text BEGININTERP interp ENDINTERP
               | block_text TEXT
               | block_text NEWLINE
               | BEGININTERP interp ENDINTERP
               | TEXT
    """
    if len(p) == 5: # text BEGININTERP interp ENDINTERP
        p[0] = p[1].addSubTree(p[3])
    elif len(p) == 3: # text TEXT
        if p[2][0] != '\n':
            p[0] = p[1].addSubTree(Tree(type='TEXT', value=p[2]))
        else:
            p[0] = p[1].addSubTree(Tree(type='NEWLINE', value=''))
    elif len(p) == 4: # BEGININTERP interp ENDINTERP
        p[0] = Tree(type='text', trees=[p[2]])
    else: # TEXT
        p[0] = Tree(type='text', trees=[Tree(type='TEXT', value=p[1])])

def p_text(p):
    """
    text : text BEGININTERP interp ENDINTERP
         | text TEXT
         | BEGININTERP interp ENDINTERP
         | TEXT
    """
    if len(p) == 5: # text BEGININTERP interp ENDINTERP
        p[0] = p[1].addSubTree(p[3])
    elif len(p) == 3: # text TEXT
        p[0] = p[1].addSubTree(Tree(type='TEXT', value=p[2]))
    elif len(p) == 4: # BEGININTERP interp ENDINTERP
        p[0] = Tree(type='text', trees=[p[2]])
    else: # TEXT
        p[0] = Tree(type='text', trees=[Tree(type='TEXT', value=p[1])])

def p_error(p):
    if p:
        print(f"Erro de sintaxe na entrada '{p.value}' na linha {p.lineno}, coluna {encontra_coluna(p)}")
    else:
        print("Erro de sintaxe no final da entrada")

def encontra_coluna(token):
    linha_inicio = lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - linha_inicio) + 1


parser = yacc.yacc(debug=True)
