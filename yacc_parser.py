import ply.yacc as yacc
from lex_parser import tokens, data
from tree import Tree, context

def p_lines(p):
    """
    lines : lines line
          | line
    """
    if len(p) == 3: # lines (line1 line2 ...)
        p[0] = p[1].addSubTree(p[2])
    else:
        p[0] = Tree('lines', '', [p[1]])


def p_line(p):
    """
    line : tagline
         | JSCODE
         | comment
         | conditional
         | iteration
         | switch
    """
    if isinstance(p[1], Tree):
        if p[1].type.startswith('tagline'): # tagline
            p[0] = Tree('line1', '', [p[1]]) 
        elif p[1].type.startswith('comment'): # comment
            p[0] = Tree('line3', '', [p[1]])
        elif p[1].type.startswith('conditional'): # conditional
            p[0] = Tree('line4', '', [p[1]])
        elif p[1].type.startswith('iteration'): # iteration
            p[0] = Tree('line5', '', [p[1]])
        elif p[1].type == ('switch'): # case
            p[0] = Tree('line6', '', [p[1]]) 
    elif isinstance(p[1], str): # JSCODE 
        p[0] = Tree('line2', '', [Tree('JSCODE', p[1], [])])


# SWITCH CASE
def p_switch(p):
    """
    switch : CASE CONDITION INDENT casesdefault DEDENT
    """
    p[0] = Tree('switch', '', [Tree('CONDITION', p[2], []), Tree('INDENT', p[3], []), p[4]])

def p_casesdefault(p):
    """
    casesdefault : cases DEFAULT INDENT lines DEDENT
                 | cases
                 | DEFAULT INDENT lines DEDENT
    """
    if len(p) == 6:
        p[0] = Tree('casesdefault1', '', [ p[1], p[4] ])
    elif len(p) == 2:
        p[0] = Tree('casesdefault2', '', [ p[1] ])
    else:
        p[0] = Tree('casesdefault3', '', [ p[3] ])

def p_cases(p):
    """
    cases : cases case 
          | case 
    """
    if len(p) == 3:
        p[0] = p[1].addSubTree(p[2])
    else:   
        p[0] = Tree('cases', '', [ p[1] ])

def p_case(p): 
    """    
    case : WHEN CONDITION INDENT lines DEDENT
    """
    p[0] = Tree('case', '', [Tree('CONDITION', p[2], []), p[4]])


# COMMENT
def p_comment(p):
    """
    comment : COMMENT comment_text
            | COMMENT
    """
    if len(p) == 3: # COMMENT comment_text (Multiple-line comments)
        p[0] = Tree('comment1', '', [Tree('COMMENT', p[1], []), p[2]])
    elif len(p) == 2: # COMMENT
        p[0] = Tree('comment2', '', [Tree('COMMENT', p[1], [])])

def p_comment_text(p):
    """
    comment_text : comment_text TEXT
                 | TEXT  
    """
    if len(p) == 3: # comment_text TEXT
        p[0] = p[1].addSubTree(Tree('TEXT', p[2], []))
    elif len(p) == 2: # TEXT
        p[0] = Tree('comment_text', '', [Tree('TEXT', p[1], [])])


# CONDITIONAL
def p_conditional(p):
    """
    conditional : conditional_begin conditional_middle conditional_final
                | conditional_begin conditional_final
                | conditional_begin conditional_middle
                | conditional_begin
    """

    if len(p) == 4:
        p[0] = Tree('conditional1', '', [p[1], p[2], p[3]])    
    elif len(p) == 3:
        p[0] = Tree('conditional2', '', [p[1], p[2]])
    else:
        p[0] = Tree('conditional3', '', [p[1]])
        
def p_conditional_begin(p):
    """
    conditional_begin : IF CONDITION INDENT lines DEDENT
                      | IF CONDITION
                      | UNLESS CONDITION INDENT lines DEDENT 
                      | UNLESS CONDITION
    """
    if len(p) == 6 and p[1] == 'if':
        p[0] = Tree('conditional_begin1', '', [Tree('CONDITION', p[2], []), Tree('INDENT', p[3], []), p[4], Tree('DEDENT', p[5], [])])
    elif len(p) == 3 and p[1] == 'if':
        p[0] = Tree('conditional_begin2', '', [Tree('CONDITION', p[2], []) ])
    elif len(p) == 6:
        p[0] = Tree('conditional_begin3', '', [Tree('CONDITION', p[2], []), Tree('INDENT', p[3], []), p[4], Tree('DEDENT', p[5], [])])
    else:
        p[0] = Tree('conditional_begin4', '', [Tree('CONDITION', p[2], []) ])

def p_conditional_middle(p):
    """
    conditional_middle : conditional_middle ELSE IF CONDITION INDENT lines DEDENT 
                       | conditional_middle ELSE IF CONDITION
                       | ELSE IF CONDITION INDENT lines DEDENT 
                       | ELSE IF CONDITION
    """
    if len(p) == 8:
        p[0] = p[1].addSubTree(Tree('CONDITION', p[4] , [Tree('INDENT', p[5], []), p[6], Tree('DEDENT', p[7], [])]) )
    elif len(p) == 5:
        p[0].addSubTree(Tree('CONDITION', p[4] , []))
    elif len(p) == 7:
        p[0] = Tree('conditional_middle', '', [Tree('CONDITION', p[3] , [Tree('INDENT', p[4], []), p[5], Tree('DEDENT', p[6], [])]) ] )
    else:
        p[0] = Tree('conditional_middle', '', [Tree('CONDITION', p[3] , [])] )

def p_conditional_final(p):
    """
    conditional_final : ELSE INDENT lines DEDENT
                      | ELSE 
    """
    if len(p) == 5:
        p[0] = Tree('conditional_final1', '', [Tree('INDENT', p[2], []), p[3], Tree('DEDENT', p[4], [])])
    else:
        p[0] = Tree('conditional_final2', '', [])


# ITERATION
def p_iteration(p):
    """
    iteration : EACH IDENTIFIER IN JSCODE INDENT lines DEDENT
    """
    if len(p) == 8: # iteration : EACH IDENTIFIER IN JSCODE INDENT lines DEDENT
        context.execute('x=' + p[4])
        e = context.eval('x')

        r = Tree('iteration', '', [])

        for val in e:
            string = p[1] + '=' + val
            context.execute(p[1] + '=' + val)
            r.addSubTree(p[6])
        
        p[0] = r

def p_tagline(p):
    """
    tagline : tag content INDENT lines DEDENT 
            | tag INDENT lines DEDENT 
            | tag content 
            | tag BAR
            | tag DOT text
            | tag
    """
    if len(p) == 6: # tag content INDENT lines DEDENT
        p[0] = Tree('tagline1', '', [p[1], p[2], Tree('INDENT', p[3], []), p[4], Tree('DEDENT', p[5], [])])
    elif len(p) == 5: # tag INDENT lines DEDENT
        p[0] = Tree('tagline2', '', [p[1], Tree('INDENT', p[2], []), p[3], Tree('DEDENT', p[4], [])])
    elif len(p) == 3: 
        if p[2] == '/': # tag BAR
            p[0] = Tree('tagline4', '', [p[1], Tree('BAR', p[2], [])])
        else: # tag content
            p[0] = Tree('tagline3', '', [p[1], p[2]])
    elif len(p) == 4: # tag DOT text
        p[0] = Tree('tagline5', '', [p[1], p[3]])
    else: # tag
        p[0] = Tree('tagline6', '', [p[1]])

def p_tag(p):
    """
    tag : class_id_attributes LPAREN pug_attributes RPAREN 
        | TAG attributes 
        | class_id_attributes
        | TAG
    """
    if len(p) == 5: # class_id_attributes LPAREN pug_attributes RPAREN
        p[0] = Tree('tag1', '', [p[1], Tree('LPAREN', p[2], []), p[3], Tree('RPAREN', p[4], [])])
    elif len(p) == 3: # TAG attributes
        p[0] = Tree('tag2', '', [Tree('TAG', p[1], []), p[2]])
    elif isinstance(p[1], Tree): # class_id_attributes
        p[0] = Tree('tag3', '', [p[1]])
    else: # TAG
        p[0] = Tree('tag4', '', [Tree('TAG', p[1], [])])

def p_attributes(p):
    """
    attributes : class_id_attributes LPAREN pug_attributes RPAREN 
               | LPAREN pug_attributes RPAREN
               | class_id_attributes
    """
    if len(p) == 5: # class_id_attributes LPAREN pug_attributes RPAREN 
        p[0] = Tree('attributes1', '', [p[1], Tree('LPAREN', p[2], []), p[3], Tree('RPAREN', p[4], [])])
    elif len(p) == 4: # LPAREN pug_attributes RPAREN
        p[0] = Tree('attributes2', '', [Tree('LPAREN', p[1], []), p[2], Tree('RPAREN', p[3], [])])
    else: # class_id_attributes
        p[0] = Tree('attributes3', '', [p[1]])

def p_class_id_attributes(p):
    """
    class_id_attributes : class ID CLASS
                        | class ID 
                        | ID class
                        | ID
                        | class
    """
    if len(p) == 4: # class ID CLASS
        p[0] = Tree('class_id_attributes1', '', [p[1], Tree('ID', p[2], []), Tree('CLASS', p[3], [])])
    elif len(p) == 3: 
        if isinstance(p[1], Tree): # class ID
            p[0] = Tree('class_id_attributes2', '', [p[1], Tree('ID', p[2], [])])
        else: # ID class
            p[0] = Tree('class_id_attributes3', '', [Tree('ID', p[1], []), p[2]])
    elif len(p) == 2:
        if isinstance(p[1], str): # ID
            p[0] = Tree('class_id_attributes4', '', [Tree('ID', p[1], [])])
        else: # class
            p[0] = Tree('class_id_attributes5', '', [p[1]])
        

def p_class(p):
    """           
    class : class CLASS 
          | CLASS
    """
    if len(p) == 3: # class CLASS
        p[0] = p[1].addSubTree(Tree('CLASS', p[2], []))
    else: # CLASS
        p[0] = Tree('class', '', [Tree('CLASS', p[1], [])])


def p_pug_attributes(p):
    """
    pug_attributes : pug_attributes COMMA pug_attribute
                   | pug_attributes pug_attribute
                   | pug_attribute
    """
    if len(p) == 4: # pug_attributes COMMA pug_attribute
        p[0] = p[1].addSubTree(p[3])
    elif len(p) == 3: # pug_attributes pug_attribute
        p[0] = p[1].addSubTree(p[2])
    else: # pug_attribute
        p[0] = Tree('pug_attributes', '', [p[1]])


def p_pug_attribute(p):
    """               
    pug_attribute : ATTRIBUTENAME EQUALS attribute_value
    """
    p[0] = Tree('pug_attribute1', '', [Tree('ATTRIBUTENAME', p[1], []), Tree('EQUALS', p[2], []), p[3]])


def p_attribute_value(p):
    """
    attribute_value : STRING
                    | BOOLEAN
                    | NUMBER
    """
    if p[1][0] == '"': # STRING
        p[0] = Tree('attribute_value1', '', [Tree('STRING', p[1], [])])
    elif p[1] == 'true' or p[1] == 'false' : # BOOLEAN
        p[0] = Tree('attribute_value2', '', [Tree('BOOLEAN', p[1], [])])
    else: # NUMBER
        p[0] = Tree('attribute_value3', '', [Tree('NUMBER', p[1], [])])


def p_content(p):
    """           
    content : EQUALS interpolation
            | text
    """
    if len(p) == 3: # EQUALS interpolation
        p[0] = Tree('content1', '', [Tree('EQUALS', p[1], []), p[2]])
    elif len(p) == 2: # text
        p[0] = Tree('content2', '', [p[1]])

def p_interpolation(p):
    """
    interpolation : STRING
                  | IDENTIFIER
                  | NUMBER
    """
    if p[1][0] == '"': # STRING
        p[0] = Tree('interpolation1', '', [Tree('STRING', p[1][1:-1], [])])
    elif p[1][0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']: # NUMBER
        p[0] = Tree('interpolation3', '', [Tree('NUMBER', p[1], [])])
    else: # IDENTIFIER
        try:
            val = context.eval(p[1])
        except:
            val = ""
        p[0] = Tree('interpolation2', '', [Tree('IDENTIFIER', val, [])])
    

def p_text(p):
    """
    text : text BEGININTERP interpolation ENDINTERP
         | text TEXT
         | BEGININTERP interpolation ENDINTERP
         | TEXT
    """
    if len(p) == 5: # text BEGININTERP interpolation ENDINTERP
        p[0] = p[1].addSubTree(Tree('TEXT', str(p[2].trees[0].value), []))
    elif len(p) == 3: # text TEXT
        p[0] = p[1].addSubTree(Tree('TEXT', p[2], []))
    elif len(p) == 4: # BEGININTERP interpolation ENDINTERP
        p[0] = Tree('text', '', [Tree('TEXT', str(p[2].trees[0].value), [])])
    else: # TEXT
        p[0] = Tree('text', '', [Tree('TEXT', p[1], [])])

def p_error(p):
    print("Erro sintático")


parser = yacc.yacc(debug=True)

tree = parser.parse(data)


string = tree.to_html()
string = string[1:]
print(string)
