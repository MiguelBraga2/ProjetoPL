import ply.yacc as yacc
from lex_parser import tokens
from tree import Tree

def p_tags(p):
    """
    tags : tags tag
         | tag
    """

    if len(p) == 3:
        p[0].append(p[2]) 
    else:
        p[0] = [ p[1] ]
    

def p_tag(p):
    """
    tag : TAG attributes content INDENT tags DEDENT 
        | TAG attributes content tags
        | TAG attributes content
        | TAG attributes BAR 
    """
    if len(p) == 7:
        p[0] = Tree('tag', '', p[1], p[5])

    elif len(p) == 5:
        p[0] = Tree('tag', '', p[1], p[4])
    elif p[3] != '/':
        pass
    else:
        pass


def p_attributes(p):
    """
    attributes : class id LPAREN pug_attributes RPAREN
               | class id 
    """
    if len(p) == 6:
        pass
    else:
        pass


def p_class(p):
    """           
    class : CLASS
          | 
    """
    if len(p) == 2:
        p[0] = Tree('class', '', p[1], [])
    else:
        pass

def p_id(p):
    """      
    id : ID
       | 
    """
    if len(p) == 2:
        p[0] = Tree('id', '', p[1], [])
    else:
        pass

def p_pug_attributes(p):
    """
    pug_attributes : pug_attributes sep pug_attribute
                   | pug_attribute
    """
    if len(p) == 4:
        pass
    else:
        pass

def p_sep(p):
    """               
    sep : COMMA
        |
    """
    if len(p) == 2:
        p[0] = Tree('comma', '', p[1], [])
    else:
        pass

def p_pug_attribute(p):
    """
    pug_attribute : ATTRIBUTENAME EQUALS STRING
                  | ATTRIBUTENAME EQUALS BOOLEAN
                  | ATTRIBUTENAME EQUALS NUMBER 
    """
    if p[3][0] == '"':
        p[0] = Tree('string', '', p[1], [])
    elif p[3] == 'true' or p[3] == 'false' :
        p[0] = Tree('boolean', '', p[1], [])
    else:
        p[0] = Tree('number', '', p[1], [])


def p_content(p):
    """           
    content : EQUALS interpolation
            | text
    """
    if len(p) == 3:
        pass
    else:
        pass

def p_interpolation(p):
    """
    interpolation : STRING
                  | VARIABLE
    """
    if p[1][0] == '"':
        p[0] = Tree('string', '', p[1], [])
    else:
        p[0] = Tree('variable', '', p[1], [])
    

def p_text(p):
    """
    text : text TEXT BEGININTERP interpolation ENDINTERP
         | text BEGININTERP interpolation ENDINTERP TEXT
         | 
    """
    if len(p) == 6:
        if p[3] == '#{':
            pass
        else:
            pass
    else:
        pass

parser = yacc.yacc(debug=True)

data = """
ul
  li Primeiro item
  li Segundo item

"""

r = parser.parse(data)

tree = Tree("raiz", "", None, r)

tree.print_tree() 
  
