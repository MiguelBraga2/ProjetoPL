import ply.yacc as yacc
from lex_parser import tokens
from tree import Tree

def p_tags(p):
    """
    tags : tags tag
         | tag
    """

    if len(p) == 3:
        p[0] = p[1].addSubTree(p[2])
    else:
        p[0] = Tree('tags', '', '', [p[1]])


def p_tag(p):
    """
    tag : TAG attributes content INDENT tags DEDENT 
        | TAG attributes content 
        | TAG attributes BAR
    """
    if len(p) == 7:
        p[0] = Tree('tag1', '', '', [Tree('TAG', '', p[1], []), p[2], p[3], Tree('INDENT', '', p[4], []), p[5], Tree('DEDENT', '', p[6], [])])
    elif p[3] != '/':
        p[0] = Tree('tag2', '', '', [Tree('TAG', '', p[1], []), p[2], p[3]])
    elif p[3] == '/':
        p[0] = Tree('tag3', '', '', [Tree('TAG', '', p[1], []), p[2], Tree('BAR', '', p[3], [])])


def p_attributes(p):
    """
    attributes : class id LPAREN pug_attributes RPAREN
               | class id 
    """
    if len(p) == 6:
        p[0] = Tree('attributes', '', '', [p[1], p[2], p[4]]) # parêntesis não precisos
    else:
        p[0] = Tree('attributes', '', '', [p[1], p[2]])


def p_class(p):
    """           
    class : class CLASS 
          | 
    """
    if len(p) == 3:
        p[0] = p[1].addSubTree(Tree('CLASS', '', p[2], []))
    else:
        p[0] = Tree('class', '', '', [])

def p_id(p):
    """      
    id : ID
       | 
    """
    if len(p) == 2:
        p[0] = Tree('ID', '', p[1], [])
    else:
        p[0] = Tree('id', '', '', [])

def p_pug_attributes(p):
    """
    pug_attributes : pug_attributes sep pug_attribute
                   | pug_attribute
    """
    if len(p) == 4:
        p[0] = p[1].addSubTree(Tree('pug_sep_attribute', '', '', [p[2], p[3]]))
    else:
        p[0] = Tree('pug_attributes', '', '', [p[1]])

def p_sep(p):
    """               
    sep : COMMA
        |
    """
    if len(p) == 2:
        p[0] = Tree('COMMA', '', p[1], [])
    else:
        p[0] = Tree('sep', '', '', '')

def p_pug_attribute(p):
    """
    pug_attribute : ATTRIBUTENAME EQUALS STRING
                  | ATTRIBUTENAME EQUALS BOOLEAN
                  | ATTRIBUTENAME EQUALS NUMBER 
    """
    if p[3][0] == '"':
        p[0] = Tree('pug_attribute', '', '', [Tree('ATTRIBUTENAME', '', p[1], []), Tree('EQUALS', '', p[2], []), Tree('STRING', '', p[3], []) ])
    elif p[3] == 'true' or p[3] == 'false' :
        p[0] = Tree('pug_attribute', '', '', [Tree('ATTRIBUTENAME', '', p[1], []), Tree('EQUALS', '', p[2], []), Tree('BOOLEAN', '', p[3], []) ])
    else:
        p[0] = Tree('pug_attribute', '', '', [Tree('ATTRIBUTENAME', '', p[1], []), Tree('EQUALS', '', p[2], []), Tree('NUMBER', '', p[3], []) ])


def p_content(p):
    """           
    content : EQUALS interpolation
            | text
    """
    if len(p) == 3:
        p[0] = Tree('content1', '', '', [Tree('EQUALS', '', p[1], []), p[2]])
    elif len(p) == 2:
        p[0] = Tree('content2', '', '', [p[1]])

def p_interpolation(p):
    """
    interpolation : STRING
                  | VARIABLE
    """
    if p[1][0] == '"':
        p[0] = Tree('interpolation1', '', p[1], [])
    else:
        p[0] = Tree('interpolation2', '', p[1], [])
    

def p_text(p):
    """
    text : text TEXT BEGININTERP interpolation ENDINTERP
         | text BEGININTERP interpolation ENDINTERP TEXT
         | text TEXT
         | 
    """
    if len(p) == 6:
        if p[3] == '#{':
            p[0] = p[1].addSubTree(Tree('text1', '', '', [Tree('TEXT', '', p[2], []), Tree('BEGININTERP', '', p[3], []), p[4], Tree('ENDINTERP', '', p[5], [])]))
        else:
            p[0] = p[1].addSubTree(Tree('text2', '', '', [Tree('BEGININTERP', '', p[2], []), p[3], Tree('ENDINTERP', '', p[4], []), Tree('TEXT', '', p[5], [])]))
    elif len(p) == 3:
        p[0] = p[1].addSubTree(Tree('TEXT', '', p[2], []))
    else:
        p[0] = Tree('text', '', '', [])

parser = yacc.yacc(debug=True)

data = """
p.class1#teste(teste = 'teste' testeaux = 'teste2')
    p ola
        p ole
    p
    p(teste='teste')
"""

tree = parser.parse(data)

print(tree.to_html())
  
